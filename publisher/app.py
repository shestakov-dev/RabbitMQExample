from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Order Publisher API")

# RabbitMQ configuration
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
QUEUE_NAME = 'orders_queue'


class Order(BaseModel):
    order_id: str
    customer_name: str
    product: str
    quantity: int
    price: float


def get_rabbitmq_connection():
    """Establish connection to RabbitMQ"""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials,
            connection_attempts=5,
            retry_delay=2
        )
        return pika.BlockingConnection(parameters)
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "Publisher API is running", "timestamp": datetime.now().isoformat()}


@app.post("/orders")
def publish_order(order: Order):
    """Publish order to RabbitMQ queue"""
    try:
        # Add timestamp to order
        order_data = order.dict()
        order_data['timestamp'] = datetime.now().isoformat()
        
        # Connect to RabbitMQ
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare queue (idempotent operation)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        
        # Publish message
        message = json.dumps(order_data)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        
        logger.info(f"Published order: {order_data['order_id']}")
        
        # Close connection
        connection.close()
        
        return {
            "status": "success",
            "message": "Order published successfully",
            "order": order_data
        }
        
    except Exception as e:
        logger.error(f"Error publishing order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to publish order: {str(e)}")


@app.get("/health")
def health_check():
    """Check if service can connect to RabbitMQ"""
    try:
        connection = get_rabbitmq_connection()
        connection.close()
        return {"status": "healthy", "rabbitmq": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "rabbitmq": "disconnected", "error": str(e)}
