#!/usr/bin/env python

import argparse
from pymavlink import mavutil

def process_gps_msg(msg):
    """Process and print GPS_RAW_INT or GLOBAL_POSITION_INT messages."""
    lat = msg.lat / 1e7
    lon = msg.lon / 1e7
    alt = msg.alt / 1e3
    msg_type = msg.get_type()
    print(f"{msg_type} -> Latitude: {lat}, Longitude: {lon}, Altitude: {alt} meters")

def process_imu_msg(msg):
    """Process and print RAW_IMU or SCALED_IMU messages."""
    x_accel = msg.xacc / 1000
    y_accel = msg.yacc / 1000
    z_accel = msg.zacc / 1000
    msg_type = msg.get_type()
    print(f"{msg_type} -> X Accel: {x_accel} G, Y Accel: {y_accel} G, Z Accel: {z_accel} G")

def main(connection_string):
    """Main function to handle MAVLink connection and message processing."""
    print("Hello from MAVLink manager service")

    # Start a connection listening on the specified port
    connection = mavutil.mavlink_connection(connection_string)

    # Wait for the first heartbeat
    connection.wait_heartbeat()
    print(f"Heartbeat from system (system {connection.target_system} component {connection.target_component})")

    # Try to receive GPS and IMU data
    while True:
        try:
            msg = connection.recv_match(
                type=['GPS_RAW_INT', 'GLOBAL_POSITION_INT', 'RAW_IMU', 'SCALED_IMU'],
                blocking=True,
                timeout=10
            )
            if msg:
                if msg.get_type() in ['GPS_RAW_INT', 'GLOBAL_POSITION_INT']:
                    process_gps_msg(msg)
                elif msg.get_type() in ['RAW_IMU', 'SCALED_IMU']:
                    process_imu_msg(msg)
        except KeyboardInterrupt:
            print("User interrupted the process")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MAVLink Manager Service')
    parser.add_argument('--host', type=str, default='udpin:localhost:14550', help='MAVLink connection string (e.g., udpin:localhost:14550)')

    args = parser.parse_args()
    main(args.host)
