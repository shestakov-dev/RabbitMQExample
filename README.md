# RabbitMQExample

A complete RabbitMQ example demonstrating message queue communication between a FastAPI publisher and a Python consumer using Docker Compose.

## Overview

This project demonstrates a microservices architecture with:
- **Publisher** - FastAPI application with REST API endpoint (`/orders`) that publishes JSON messages to RabbitMQ
- **RabbitMQ** - Message broker for reliable message delivery
- **Consumer** - Python application that consumes messages, saves them to a file, and generates log messages

## Architecture

```
┌─────────────┐         ┌──────────┐         ┌──────────┐
│  Publisher  │         │ RabbitMQ │         │ Consumer │
│  (FastAPI)  │ ──────> │ (Docker) │ ──────> │ (Python) │
│   :8000     │  JSON   │  :5672   │  JSON   │  Logs +  │
│             │         │ :15672   │         │   File   │
└─────────────┘         └──────────┘         └──────────┘
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation & Usage

### 1. Start All Services

Start all services (RabbitMQ, Publisher, Consumer) with Docker Compose:

```bash
docker compose up --build
```

This will:
- Build the publisher and consumer Docker images
- Start RabbitMQ with management UI
- Start the publisher API on `http://localhost:8000`
- Start the consumer listening for messages

### 2. Publish Orders

Send orders to the publisher API using the `/orders` endpoint:

**Example using curl:**

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-001",
    "customer_name": "John Doe",
    "product": "Laptop",
    "quantity": 2,
    "price": 1299.99
  }'
```

**Example using Python:**

```python
import requests

order = {
    "order_id": "ORD-002",
    "customer_name": "Jane Smith",
    "product": "Mouse",
    "quantity": 5,
    "price": 29.99
}

response = requests.post("http://localhost:8000/orders", json=order)
print(response.json())
```

**Interactive API Documentation:**

Open `http://localhost:8000/docs` in your browser for interactive Swagger UI.

### 3. View Consumer Logs

The consumer will log each received order. View the logs:

```bash
docker compose logs -f consumer
```

Example output:
```
============================================================
✓ Received new order
  Order ID: ORD-001
  Customer: John Doe
  Product: Laptop
  Quantity: 2
  Price: $1299.99
  Timestamp: 2026-02-18T08:30:00.123456
✓ Saved order to file: ORD-001
  Total orders in file: 1
✓ Order processed successfully
============================================================
```

### 4. View Saved Orders

All orders are saved to `./data/orders.json`:

```bash
cat data/orders.json
```

### 5. Access RabbitMQ Management UI

Open `http://localhost:15672` in your browser:
- Username: `guest`
- Password: `guest`

View queues, messages, connections, and more.

## Project Structure

```
RabbitMQExample/
├── docker-compose.yml          # Orchestrates all services
├── publisher/
│   ├── Dockerfile             # Publisher container image
│   ├── app.py                 # FastAPI application
│   └── requirements.txt       # Python dependencies
├── consumer/
│   ├── Dockerfile             # Consumer container image
│   ├── app.py                 # Consumer application
│   └── requirements.txt       # Python dependencies
├── data/
│   └── orders.json            # Saved orders (auto-generated)
└── README.md                  # This file
```

## API Endpoints

### Publisher Service (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/orders` | Publish order to queue |
| GET | `/health` | Check RabbitMQ connection |
| GET | `/docs` | Interactive API documentation |

### Order Schema

```json
{
  "order_id": "string",
  "customer_name": "string",
  "product": "string",
  "quantity": integer,
  "price": float
}
```

## How It Works

### 1. Publisher (FastAPI)
- Exposes REST API endpoint `/orders`
- Receives order data in JSON format
- Adds timestamp to each order
- Publishes message to RabbitMQ queue `orders_queue`
- Returns confirmation to client

### 2. RabbitMQ
- Message broker that queues messages
- Ensures reliable delivery (persistent messages)
- Provides management UI for monitoring
- Handles connection from both publisher and consumer

### 3. Consumer
- Connects to RabbitMQ on startup
- Listens continuously for messages on `orders_queue`
- Processes each message:
  - Parses JSON data
  - Logs order details
  - Saves to file (`/data/orders.json`)
  - Acknowledges message
- Automatic reconnection on failure

## Testing Multiple Orders

You can use this bash script to publish multiple orders:

```bash
#!/bin/bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/orders \
    -H "Content-Type: application/json" \
    -d "{
      \"order_id\": \"ORD-$(printf '%03d' $i)\",
      \"customer_name\": \"Customer $i\",
      \"product\": \"Product $i\",
      \"quantity\": $((RANDOM % 10 + 1)),
      \"price\": $((RANDOM % 1000 + 100))
    }"
  sleep 1
done
```

## Stopping the Application

Stop all services:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

## Troubleshooting

### Publisher can't connect to RabbitMQ

Wait a few seconds for RabbitMQ to fully start. The publisher has built-in retry logic.

### Consumer not receiving messages

1. Check if consumer is running: `docker compose ps`
2. Check consumer logs: `docker compose logs consumer`
3. Verify queue exists in RabbitMQ management UI

### View all service logs

```bash
docker compose logs -f
```

## Technologies Used

- **Python 3.11** - Programming language
- **FastAPI** - Modern web framework for building APIs
- **Pika** - Python client for RabbitMQ (AMQP 0-9-1)
- **RabbitMQ 3** - Message broker with management plugin
- **Docker & Docker Compose** - Containerization and orchestration
- **Uvicorn** - ASGI server for FastAPI

## License

MIT