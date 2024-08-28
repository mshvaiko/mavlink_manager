# Description: This module is used to emulate the drone's attitude and azimuth values and send them to the RabbitMQ server.
import random
import time
import pika

# Define the RabbitMQ host and connection
RABBIT_MQ_HOST = 'localhost'
rabbit_mq_connection = None
rabbit_mq_channel = None

# real attitude and azimuth from optical_position_tracking module in meters and degrees (attitude, azimuth)
RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE = 'drone_attitude_and_azimuth'

def init_rabbit_mq():
    global rabbit_mq_connection, rabbit_mq_channel
    if (RABBIT_MQ_HOST is None):
        print("Error: RabbitMQ host is not defined.")
        exit()

    # Create a connection to the RabbitMQ server, setup the channel and queue
    try:
        rabbit_mq_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_HOST))
        rabbit_mq_channel = rabbit_mq_connection.channel()
        rabbit_mq_channel.queue_declare(RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE)
    except Exception as err:
        print(f"Error: Could not connect to RabbitMQ server at {RABBIT_MQ_HOST}.")
        print(err)
        exit()

def send_random_attitude_and_azimuth():
    # Send random attitude and azimuth values to the RabbitMQ queue
    attitude = random.randint(30, 40)
    azimuth = random.randint(0, 360)
    rabbit_mq_channel.basic_publish(exchange='', routing_key=RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE, body=str((attitude, azimuth)))
    print(f" [x] Sent attitude: {attitude}, azimuth: {azimuth}")

       
def close_rabbit_mq():
    global rabbit_mq_connection
    # Close the RabbitMQ connection
    if rabbit_mq_connection is not None:
        rabbit_mq_connection.close()

def main():
    init_rabbit_mq()

    try:
        while True:
            send_random_attitude_and_azimuth()
            time.sleep(5)
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        # Release the capture and close the RabbitMQ connection
        close_rabbit_mq()

if __name__ == "__main__":
    main()