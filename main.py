import argparse
import logging
import os
from collections import deque
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI
from apscheduler.schedulers.blocking import BlockingScheduler
from fastapi.responses import JSONResponse

from dailytextgeneration import generate_message, get_time_of_day
from elevenlabs_tts import text_to_voice
from senddm import send_voice


logger = logging.getLogger(__name__)
app = FastAPI(title="Premagent", version="1.0.0")
pipeline_events = deque(maxlen=500)


def _utc_now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _record_event(event: Dict[str, Any]) -> None:
    pipeline_events.appendleft(event)


def _latest_event_response() -> Dict[str, Any]:
    latest = pipeline_events[0] if pipeline_events else None
    return {
        "ok": True,
        "has_logs": latest is not None,
        "latest": latest,
        "count": len(pipeline_events),
    }


def run_pipeline(trigger: str = "scheduler") -> Dict[str, Any]:
    audio_path = None
    message = None
    time_of_day = None
    event: Dict[str, Any] = {
        "timestamp": _utc_now_iso(),
        "trigger": trigger,
        "status": "error",
        "time_of_day": None,
        "message": None,
        "audio_file": None,
        "error": None,
    }

    try:
        time_of_day = get_time_of_day()
        logger.info("Running pipeline for time_of_day=%s", time_of_day)
        event["time_of_day"] = time_of_day

        message = generate_message(time_of_day=time_of_day)
        logger.info("Message generated successfully")
        event["message"] = message

        audio_path = text_to_voice(message)
        logger.info("Audio generated: %s", audio_path)
        event["audio_file"] = audio_path

        send_voice(audio_path)
        logger.info("Voice note sent")
        event["status"] = "sent"
    except Exception as exc:
        event["error"] = str(exc)
        logger.exception("Pipeline job failed")
    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info("Cleaned up temp audio file: %s", audio_path)
                event["audio_file_deleted"] = True
            except OSError:
                logger.exception("Failed to remove temp audio file: %s", audio_path)
                event["audio_file_deleted"] = False

    _record_event(event)
    return event


@app.get("/api/health")
def healthcheck() -> Dict[str, Any]:
    return {"ok": True, "service": "swala-uptime", "timestamp": _utc_now_iso()}


@app.get("/api/logs")
def get_logs(limit: int = 50) -> Dict[str, Any]:
    safe_limit = max(1, min(limit, 500))
    return {
        "ok": True,
        "count": len(pipeline_events),
        "logs": list(pipeline_events)[:safe_limit],
    }


@app.post("/api/send")
def send_now() -> JSONResponse:
    result = run_pipeline(trigger="api")
    status_code = 200 if result.get("status") == "sent" else 500
    return JSONResponse(content={"ok": status_code == 200, "result": result}, status_code=status_code)


def build_scheduler() -> BlockingScheduler:
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")

    run_times = [(8, 0), (13, 0), (19, 0), (22, 0)]
    for hour, minute in run_times:
        scheduler.add_job(run_pipeline, "cron", hour=hour, minute=minute, kwargs={"trigger": "scheduler"})

    scheduled_labels = [f"{hour:02d}:{minute:02d}" for hour, minute in run_times]
    logger.info("Configured IST schedules: %s", ", ".join(scheduled_labels))

    return scheduler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run scheduled daily message voice pipeline")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the full pipeline once immediately and exit",
    )
    parser.add_argument(
        "--print-latest-log",
        action="store_true",
        help="Print latest in-memory pipeline event as JSON-compatible dict and exit",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    args = parse_args()

    if args.test:
        logger.info("Running in --test mode")
        result = run_pipeline(trigger="test")
        logger.info("Test result: %s", result)
        return

    if args.print_latest_log:
        logger.info("Latest event: %s", _latest_event_response())
        return

    scheduler = build_scheduler()
    logger.info("Starting BlockingScheduler")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received, stopping scheduler gracefully")
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
    

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}