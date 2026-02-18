import pika
import json
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# RabbitMQ configuration
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
QUEUE_NAME = 'orders_queue'

# Output file configuration
OUTPUT_FILE = '/data/orders.json'


def ensure_data_directory():
    """Ensure the data directory exists"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    logger.info(f"Data directory ready: {os.path.dirname(OUTPUT_FILE)}")


def save_order_to_file(order_data):
    """Save order to JSON file"""
    try:
        # Read existing orders
        orders = []
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r') as f:
                try:
                    orders = json.load(f)
                except json.JSONDecodeError:
                    logger.warning("Existing file is not valid JSON, starting fresh")
                    orders = []
        
        # Append new order
        orders.append(order_data)
        
        # Write back to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(orders, f, indent=2)
        
        logger.info(f"✓ Saved order to file: {order_data.get('order_id', 'unknown')}")
        logger.info(f"  Total orders in file: {len(orders)}")
        
    except Exception as e:
        logger.error(f"✗ Failed to save order to file: {e}")


def callback(ch, method, properties, body):
    """Process received message"""
    try:
        # Parse JSON message
        order_data = json.loads(body)
        
        logger.info("=" * 60)
        logger.info(f"✓ Received new order")
        logger.info(f"  Order ID: {order_data.get('order_id', 'N/A')}")
        logger.info(f"  Customer: {order_data.get('customer_name', 'N/A')}")
        logger.info(f"  Product: {order_data.get('product', 'N/A')}")
        logger.info(f"  Quantity: {order_data.get('quantity', 'N/A')}")
        logger.info(f"  Price: ${order_data.get('price', 0):.2f}")
        logger.info(f"  Timestamp: {order_data.get('timestamp', 'N/A')}")
        
        # Save to file
        save_order_to_file(order_data)
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"✓ Order processed successfully")
        logger.info("=" * 60)
        
    except json.JSONDecodeError as e:
        logger.error(f"✗ Invalid JSON message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge to remove from queue
    except Exception as e:
        logger.error(f"✗ Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    """Main consumer loop"""
    logger.info("=" * 60)
    logger.info("Starting RabbitMQ Consumer")
    logger.info("=" * 60)
    
    # Ensure data directory exists
    ensure_data_directory()
    
    # Connect to RabbitMQ with retry logic
    while True:
        try:
            logger.info(f"Connecting to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}...")
            
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            # Declare queue
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            
            # Set prefetch count
            channel.basic_qos(prefetch_count=1)
            
            logger.info(f"✓ Connected to RabbitMQ")
            logger.info(f"✓ Listening for messages on queue: {QUEUE_NAME}")
            logger.info(f"✓ Output file: {OUTPUT_FILE}")
            logger.info("Waiting for orders... (Press CTRL+C to exit)")
            logger.info("=" * 60)
            
            # Start consuming
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("\nShutting down consumer...")
            break
        except Exception as e:
            logger.error(f"Connection error: {e}")
            logger.info("Retrying in 5 seconds...")
            import time
            time.sleep(5)


if __name__ == "__main__":
    main()
