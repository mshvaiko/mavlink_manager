# MAVLink Manager

This project provides a Python-based manager for MAVLink communication between a flight controller (FC) and other services. It supports both serial and UDP connections for receiving MAVLink messages from the FC, sending messages to other services via RabbitMQ using Pika, and potentially sending optical flow messages for position correction back to the FC.

## General Description

The MAVLink Manager handles the following tasks:
- **MAVLink Communication**: Establishes and manages connections to the FC via serial or UDP.
- **Message Handling**: Processes incoming MAVLink messages and routes them to appropriate services via RabbitMQ.
- **RabbitMQ Communication**: Uses Pika for RabbitMQ communication.

### Key Components:
- **MAVLink Connection**: Manages connections to the FC and receives MAVLink messages.
- **Message Handler**: Processes and routes MAVLink messages via RabbitMQ.
- **RabbitMQ Client**: Uses Pika for communication with RabbitMQ.
- **Configuration Management**: Handles configuration settings for connections and message processing.

## Requirements

Ensure the following are installed before running the manager:

- **Python 3.10+**
- **pymavlink**: MAVLink Python library for handling MAVLink messages.
- **pyserial**: For serial communication.
- **pyyaml**: For configuration management.
- **pika**: RabbitMQ Python client.

### Install Dependencies

All necessary Python packages are listed in the `requirements.txt` file. Install them using pip:

```bash
pip install -r requirements.txt
