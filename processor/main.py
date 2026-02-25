#!/usr/bin/env python
import os
import sys
import json
import time
import pika
import psycopg
from text2speech import tts
from text2speech import Voice


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "content-droid"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )


def mark_processing(video_id: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE videos
                SET status = 'PROCESSING',
                    started_at = COALESCE(started_at, NOW()),
                    updated_at = NOW()
                WHERE id = %s
                """,
                (video_id,),
            )


def mark_complete(video_id: str, download_location: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE videos
                SET status = 'COMPLETE',
                    storage_key = %s,
                    progress = 100,
                    completed_at = NOW(),
                    updated_at = NOW()
                WHERE id = %s
                """,
                (download_location, video_id),
            )


def mark_failed(video_id: str, error_message: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE videos
                SET status = 'FAILED',
                    error_message = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (error_message[:2000], video_id),
            )


def main():
    queue_name = os.getenv("RABBITMQ_QUEUE_NAME", "videos")
    rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")
    output_dir = os.getenv("VIDEO_OUTPUT_DIR", "/app/videos")
    download_base_url = os.getenv("DOWNLOAD_BASE_URL", "").rstrip("/")

    os.makedirs(output_dir, exist_ok=True)

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbit_host)
            )
            break
        except Exception as exc:
            print(f" [!] RabbitMQ unavailable ({exc}), retrying in 3s...")
            time.sleep(3)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        payload = json.loads(body.decode())
        text = payload["prompt"]
        id = payload["id"]

        try:
            mark_processing(id)

            output_path = os.path.join(output_dir, f"{id}.mp4")
            tts(text, Voice.US_MALE_1, output_file_path=output_path)

            if download_base_url:
                download_location = f"{download_base_url}/{id}.mp4"
            else:
                download_location = output_path

            mark_complete(id, download_location)

            print(f" [x] Generated Video: {id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            try:
                mark_failed(id, str(exc))
            except Exception as mark_exc:
                print(f" [!] Failed to mark FAILED for {id}: {mark_exc}")
            print(f" [!] Generation failed for {id}: {exc}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
