#!/usr/bin/env python
import pika
import sys
import os
import json

from database import DatabaseClient


def main():

    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "my-secret-pw",
        "database": "test"
    }

    db_client = DatabaseClient(db_config)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='airports_api', durable=True)

    def callback(ch, method, properties, body):
        body_json = json.loads(body)
        if "create" == body_json["method"]:
            db_client.insert(body_json["params"], "airport")
        if "update" == body_json["method"]:
            db_client.update(body_json["params"], "airport", {"field": "id", "value": body_json["id"]})
        if "delete" == body_json["method"]:
            db_client.delete("airport", {"field": "id", "value": body_json["id"]})
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='airports_api', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
