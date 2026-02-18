# RabbitMQExample

A simple RabbitMQ example with Node.js publisher and consumer using Docker Compose.

## Overview

This project demonstrates a basic message queue system using:

- **RabbitMQ** - Message broker running in Docker
- **Publisher** - Node.js application that publishes random messages
- **Consumer** - Node.js application that consumes and processes messages

## Architecture

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│Publisher │ ──────> │ RabbitMQ │ ──────> │Consumer  │
│ (Node.js)│         │ (Docker) │         │ (Node.js)│
└──────────┘         └──────────┘         └──────────┘
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

For local development without Docker:

- [Node.js](https://nodejs.org/) (v14 or higher)
- npm (comes with Node.js)

## Quick Start with Docker Compose

### 1. Start All Services

Start RabbitMQ, publisher, and consumer with a single command:

```bash
docker compose up --build
```

This will:

- Start RabbitMQ with management UI
- Build and run the publisher (publishes messages and exits)
- Build and run the consumer (keeps running and processing messages)

The consumer will display processed messages in the terminal.

### 2. View RabbitMQ Management UI

Open your browser and navigate to: `http://localhost:15672`

- Username: `guest`
- Password: `guest`

Here you can view queues, messages, connections, and more.

### 3. Run Publisher Again

To publish more messages:

```bash
docker compose run --rm publisher
```

### 4. Stop Services

Stop all services:

```bash
docker compose down
```

## Local Development (Without Docker)

### 1. Install Dependencies

```bash
npm install
```

### 2. Start RabbitMQ

Start only RabbitMQ using Docker:

```bash
docker compose up -d rabbitmq
```

### 3. Run Consumer

In one terminal:

```bash
npm run consumer
```

### 4. Run Publisher

In another terminal:

```bash
npm run publisher
```

## How It Works

### Publisher (`publisher.js`)

- Connects to RabbitMQ
- Randomly publishes 3-7 messages from a predefined list
- Each message includes a timestamp
- Exits after publishing all messages

### Consumer (`consumer.js`)

- Connects to RabbitMQ
- Listens continuously for messages
- Processes each message (extracts timestamp and content)
- Acknowledges messages after processing
- Keeps running until manually stopped

### RabbitMQ

- Message broker that queues messages
- Ensures reliable message delivery between publisher and consumer
- Provides management UI for monitoring

## Example Output

**Publisher:**

```
=== RabbitMQ Publisher ===
Connecting to RabbitMQ at amqp://guest:guest@rabbitmq:5672...

Publishing 4 messages to queue 'example_queue'...

✓ Published: [2026-02-18T08:30:00.123Z] Hello from RabbitMQ!
✓ Published: [2026-02-18T08:30:00.623Z] Processing order #12345
✓ Published: [2026-02-18T08:30:01.123Z] Payment processed successfully
✓ Published: [2026-02-18T08:30:01.623Z] Email notification sent

4 messages published successfully!
```

**Consumer:**

```
=== RabbitMQ Consumer ===
Connecting to RabbitMQ at amqp://guest:guest@rabbitmq:5672...
Waiting for messages in queue 'example_queue'...
To exit, press CTRL+C

✓ Received: [2026-02-18T08:30:00.123Z] Hello from RabbitMQ!
  → Processing message...
  → Timestamp: 2026-02-18T08:30:00.123Z
  → Content: Hello from RabbitMQ!
  → Processing completed!

✓ Received: [2026-02-18T08:30:00.623Z] Processing order #12345
  → Processing message...
  → Timestamp: 2026-02-18T08:30:00.623Z
  → Content: Processing order #12345
  → Processing completed!
```

## Project Structure

```
RabbitMQExample/
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile.publisher     # Publisher Docker image
├── Dockerfile.consumer      # Consumer Docker image
├── package.json            # Node.js dependencies and scripts
├── publisher.js            # Message publisher application
├── consumer.js             # Message consumer application
└── README.md              # This file
```

## Configuration

Both publisher and consumer use the `RABBITMQ_HOST` environment variable to connect to RabbitMQ:

- In Docker: automatically set to `rabbitmq` (service name)
- Locally: defaults to `localhost`

## Technologies Used

- **Node.js 18** - JavaScript runtime
- **amqplib** - AMQP 0-9-1 client library for Node.js
- **RabbitMQ 3** - Message broker with management plugin
- **Docker & Docker Compose** - Containerization and orchestration

## Troubleshooting

### Services won't start

Wait a few seconds for RabbitMQ to fully initialize. The publisher and consumer have dependency checks.

### View all logs

```bash
docker compose logs -f
```

### View specific service logs

```bash
docker compose logs -f consumer
docker compose logs -f publisher
```

## License

MIT
