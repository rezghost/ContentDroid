#!/usr/bin/env python
import os
import sys
import json
import time
from datetime import datetime, timezone
import pika
from google.cloud import storage
from text2speech import tts
from text2speech import Voice
from google.cloud.sql.connector import Connector, IPTypes
import pg8000


connector = Connector(refresh_strategy="LAZY")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")
dbname = os.getenv("POSTGRES_DB", "content-droid")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
instance_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME", "")


def log(message: str):
    now = datetime.now(timezone.utc).isoformat()
    print(f"[{now}] {message}", flush=True)

def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=user,
        password=password,
        db=dbname,
        ip_type=IPTypes.PUBLIC,
    )
    return conn


def mark_processing(video_id: str):
    with getconn() as conn:
        cur = conn.cursor()
        try:
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
            conn.commit()
        finally:
            cur.close()


def mark_complete(video_id: str, download_location: str):
    with getconn() as conn:
        cur = conn.cursor()
        try:
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
            conn.commit()
        finally:
            cur.close()


def mark_failed(video_id: str, error_message: str):
    with getconn() as conn:
        cur = conn.cursor()
        try:
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
            conn.commit()
        finally:
            cur.close()

def upload_to_bucket(id, file_path: str) -> str:
    bucket_name = os.getenv("GCS_BUCKET_NAME", "ctdroid_video_bucket")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable is not set")

    client = storage.Client()
    object_key = f"videos/{id}.mp4"
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    blob.upload_from_filename(file_path, content_type="video/mp4")
    public_base_url = os.getenv("GCS_PUBLIC_BASE_URL", "https://storage.googleapis.com").rstrip("/")
    return f"{public_base_url}/{bucket_name}/{object_key}"


def main():
    queue_name = os.getenv("RABBITMQ_QUEUE_NAME", "videos")
    rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbit_port = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbit_user = os.getenv("RABBITMQ_USER", "guest")
    rabbit_password = os.getenv("RABBITMQ_PASSWORD", "guest")
    rabbit_vhost = os.getenv("RABBITMQ_VHOST", "/")
    output_dir = os.getenv("VIDEO_OUTPUT_DIR", "./videos")

    log(
        f"Processor starting queue={queue_name} rabbit={rabbit_host}:{rabbit_port} "
        f"vhost={rabbit_vhost} db={dbname} cloud_sql={'set' if instance_connection_name else 'unset'}"
    )

    os.makedirs(output_dir, exist_ok=True)

    while True:
        try:
            credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=rabbit_host,
                    port=rabbit_port,
                    virtual_host=rabbit_vhost,
                    credentials=credentials,
                )
            )
            log("RabbitMQ connection established")
            break
        except Exception as exc:
            log(f"[!] RabbitMQ unavailable ({exc}), retrying in 3s...")
            time.sleep(3)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    log(f"Queue declared: {queue_name}")

    def callback(ch, method, properties, body):
        payload = json.loads(body.decode())
        text = payload["prompt"]
        id = payload["id"]
        start = time.time()
        log(f"Received message id={id} prompt_len={len(text)}")

        try:
            log(f"id={id} mark_processing start")
            mark_processing(id)
            log(f"id={id} mark_processing complete")

            output_path = os.path.join(output_dir, f"{id}.mp4")
            log(f"id={id} tts start output={output_path}")
            tts(text, Voice.US_MALE_1, output_file_path=output_path)
            log(f"id={id} tts complete")

            log(f"id={id} upload start")
            url = upload_to_bucket(id, output_path)
            log(f"id={id} upload complete url={url}")

            log(f"id={id} mark_complete start")
            mark_complete(id, url)
            log(f"id={id} mark_complete complete")

            log(f"[x] Generated Video: {id} elapsed={time.time() - start:.2f}s")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            log(f"id={id} acked")

            os.remove(output_path)
            log(f"id={id} removed temp file")
        except Exception as exc:
            try:
                mark_failed(id, str(exc))
            except Exception as mark_exc:
                log(f"[!] Failed to mark FAILED for {id}: {mark_exc}")
            log(f"[!] Generation failed for {id}: {exc}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            log(f"id={id} acked after failure")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    log("[*] Waiting for messages. To exit press CTRL+C")
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
