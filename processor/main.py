#!/usr/bin/env python
import os
import sys
import pika
from text2speech import tts
from text2speech import Voice


def main():
    queue_name = 'videos'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):           
        text = str(body.decode())

        tts(text, Voice.US_MALE_1, output_file_path=f"../output.mp4")

        print(f" [x] Generated Video: {text}")
        
        ch.basic_ack(delivery_tag = method.delivery_tag)

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
