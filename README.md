# RabbitMQExample

A simple example demonstrating RabbitMQ message queue with Node.js publisher and consumer using Docker Compose.

## Overview

This project demonstrates:
- **RabbitMQ** message broker running in Docker
- **Publisher** - A Node.js application that publishes random messages to a queue
- **Consumer** - A Node.js application that consumes and processes messages from the queue

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (v14 or higher)
- npm (comes with Node.js)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shestakov-dev/RabbitMQExample.git
cd RabbitMQExample
```

2. Install Node.js dependencies:
```bash
npm install
```

## Usage

### 1. Start RabbitMQ

Start the RabbitMQ server using Docker Compose:

```bash
docker-compose up -d
```

This will start RabbitMQ on:
- AMQP port: `localhost:5672`
- Management UI: `http://localhost:15672` (username: `guest`, password: `guest`)

### 2. Run the Consumer

In a terminal, start the consumer to listen for messages:

```bash
npm run consumer
```

The consumer will wait for messages and process them as they arrive.

### 3. Run the Publisher

In another terminal, run the publisher to send random messages:

```bash
npm run publisher
```

The publisher will send 3-7 random messages to the queue and then exit.

## Architecture

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│Publisher │ ──────> │ RabbitMQ │ ──────> │Consumer  │
│ (Node.js)│         │ (Docker) │         │ (Node.js)│
└──────────┘         └──────────┘         └──────────┘
```

## How It Works

1. **Publisher** (`publisher.js`):
   - Connects to RabbitMQ
   - Randomly selects and publishes 3-7 messages
   - Each message includes a timestamp
   - Exits after publishing all messages

2. **Consumer** (`consumer.js`):
   - Connects to RabbitMQ
   - Listens continuously for messages
   - Processes each message (extracts timestamp and content)
   - Acknowledges messages after processing
   - Keeps running until manually stopped (CTRL+C)

3. **RabbitMQ**:
   - Message broker that queues messages
   - Ensures reliable message delivery
   - Provides management UI for monitoring

## Stopping the Application

1. Stop the consumer with `CTRL+C`
2. Stop RabbitMQ:
```bash
docker-compose down
```

## Viewing RabbitMQ Management UI

Open your browser and navigate to: `http://localhost:15672`
- Username: `guest`
- Password: `guest`

Here you can view queues, connections, channels, and message rates.

## Project Structure

```
RabbitMQExample/
├── docker-compose.yml  # Docker Compose configuration for RabbitMQ
├── package.json        # Node.js dependencies and scripts
├── publisher.js        # Message publisher application
├── consumer.js         # Message consumer application
└── README.md          # This file
```

## Technologies Used

- **RabbitMQ 3** - Message broker with management plugin
- **Node.js** - JavaScript runtime
- **amqplib** - AMQP 0-9-1 client library for Node.js
- **Docker & Docker Compose** - Containerization

## License

MIT