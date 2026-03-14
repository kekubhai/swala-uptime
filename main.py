import argparse
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler

from dailytextgeneration import generate_message, get_time_of_day
from elevenlabs_tts import text_to_voice
from senddm import send_voice


logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    audio_path = None

    try:
        time_of_day = get_time_of_day()
        logger.info("Running pipeline for time_of_day=%s", time_of_day)

        message = generate_message(time_of_day=time_of_day)
        logger.info("Message generated successfully")

        audio_path = text_to_voice(message)
        logger.info("Audio generated: %s", audio_path)

        send_voice(audio_path)
        logger.info("Voice note sent")
    except Exception:
        logger.exception("Pipeline job failed")
    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info("Cleaned up temp audio file: %s", audio_path)
            except OSError:
                logger.exception("Failed to remove temp audio file: %s", audio_path)


def build_scheduler() -> BlockingScheduler:
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")

    run_times = [(8, 0), (13, 0), (19, 0), (22, 0)]
    for hour, minute in run_times:
        scheduler.add_job(run_pipeline, "cron", hour=hour, minute=minute)

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
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    args = parse_args()

    if args.test:
        logger.info("Running in --test mode")
        run_pipeline()
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

