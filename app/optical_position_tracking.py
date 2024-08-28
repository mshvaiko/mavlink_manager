# Description: This module is responsible for receiving the pixel coordinates from the optical_stabilization module,
# calculating the real-world coordinates, azimuth, and distance, and sending the resulting azimuth and distance to the RabbitMQ server.
import ast
import pika
import coordinates_calculate as cc

# Define the RabbitMQ host and connection
RABBIT_MQ_HOST = 'localhost'
rabbit_mq_connection = None
rabbit_mq_channel = None

# Last attitude and azimuth values from the drone
LAST_DRONE_ATTITUDE = None;
LAST_DRONE_AZIMUTH = None;

# pixel coordinates from optical_stabilzation module in pixels (x, y)
RABBIT_MQ_PIXEL_COORDINATES_QUEUE = 'drone_pixel_coordinates'

# real attitude and azimuth from optical_position_tracking module in meters and degrees (attitude, azimuth)
RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE = 'drone_attitude_and_azimuth'

# calculated real distance and azimuth from optical_position_tracking module in meters and degrees (distance, azimuth)
RABBIT_MQ_OPTICAL_POSITION_CORRECTION_QUEUE = 'optical_position_correction'

def init_rabbit_mq():
    global rabbit_mq_connection, rabbit_mq_channel
    if (RABBIT_MQ_HOST is None):
        print("Error: RabbitMQ host is not defined.")
        exit()

    # Create a connection to the RabbitMQ server, setup the channel and queue
    try:
        rabbit_mq_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_HOST))
        rabbit_mq_channel = rabbit_mq_connection.channel()
        rabbit_mq_channel.queue_declare(RABBIT_MQ_PIXEL_COORDINATES_QUEUE)
        rabbit_mq_channel.queue_declare(RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE)
        rabbit_mq_channel.queue_declare(RABBIT_MQ_OPTICAL_POSITION_CORRECTION_QUEUE)
    except Exception as err:
        print(f"Error: Could not connect to RabbitMQ server at {RABBIT_MQ_HOST}.")
        print(err)
        exit()

def update_last_attitude_and_drone_azimuth(ch, method, properties, body):
    global LAST_DRONE_ATTITUDE, LAST_DRONE_AZIMUTH
    
    LAST_DRONE_ATTITUDE, LAST_DRONE_AZIMUTH = ast.literal_eval(body.decode())
    print(f" [x] Received {body}")

def calculate_correction_distance_and_azimuth(ch, method, properties, body):
    global LAST_DRONE_ATTITUDE, LAST_DRONE_AZIMUTH
    
    if (LAST_DRONE_ATTITUDE is None or LAST_DRONE_AZIMUTH is None):
        print(f"No attitude and azimuth values received from the drone yet.")
        return

    pixel_x, pixel_y = ast.literal_eval(body.decode())
    real_x, real_y = cc.calculate_real_coordinates(pixel_x, pixel_y, LAST_DRONE_ATTITUDE)
    print(f"Real coordinates: ({real_x}, {real_y}) meters")

    azimuth, distance = cc.calculate_azimuth_and_distance(real_x, real_y)
    print(f"Azimuth to the zero point: {azimuth} degrees, distance: {distance} meters")

    resulting_azimuth = cc.calculate_resulting_azimuth(LAST_DRONE_AZIMUTH, azimuth)
    print(f"Resulting relative drone azimuth to the zero point: {resulting_azimuth} degrees")

    send_optical_position_correction(distance, resulting_azimuth)

def send_optical_position_correction(distance, resulting_azimuth):
    global rabbit_mq_channel
    # Send the calculated real distance and azimuth from optical_position_tracking module in meters and degrees (distance, azimuth)
    rabbit_mq_channel.basic_publish(exchange='', routing_key=RABBIT_MQ_OPTICAL_POSITION_CORRECTION_QUEUE, body=str((distance, resulting_azimuth)))

def main():
    init_rabbit_mq()

    rabbit_mq_channel.basic_consume(queue=RABBIT_MQ_ATTITUDE_AND_AZIMUTH_QUEUE, on_message_callback=update_last_attitude_and_drone_azimuth, auto_ack=True)
    rabbit_mq_channel.basic_consume(queue=RABBIT_MQ_PIXEL_COORDINATES_QUEUE, on_message_callback=calculate_correction_distance_and_azimuth, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rabbit_mq_channel.start_consuming()

if __name__ == "__main__":
    main()