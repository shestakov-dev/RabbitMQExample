const amqp = require('amqplib');

const QUEUE_NAME = 'example_queue';
const RABBITMQ_HOST = process.env.RABBITMQ_HOST || 'localhost';
const RABBITMQ_URL = `amqp://guest:guest@${RABBITMQ_HOST}:5672`;
const MESSAGE_DELAY_MS = 500; // Delay between publishing messages
const GRACEFUL_SHUTDOWN_DELAY_MS = 1000; // Wait for messages to flush before closing

// Sample messages to publish
const sampleMessages = [
  'Hello from RabbitMQ!',
  'Processing order #12345',
  'User registration completed',
  'File upload successful',
  'Email notification sent',
  'Database backup completed',
  'Task scheduled for execution',
  'Payment processed successfully'
];

async function publishMessages() {
  try {
    console.log(`Connecting to RabbitMQ at ${RABBITMQ_URL}...`);
    const connection = await amqp.connect(RABBITMQ_URL);
    const channel = await connection.createChannel();

    await channel.assertQueue(QUEUE_NAME, { durable: false });

    // Randomly select and publish a few messages
    const numberOfMessages = Math.floor(Math.random() * 5) + 3; // 3 to 7 messages
    console.log(`\nPublishing ${numberOfMessages} messages to queue '${QUEUE_NAME}'...\n`);

    for (let i = 0; i < numberOfMessages; i++) {
      const randomMessage = sampleMessages[Math.floor(Math.random() * sampleMessages.length)];
      const message = `[${new Date().toISOString()}] ${randomMessage}`;
      
      channel.sendToQueue(QUEUE_NAME, Buffer.from(message));
      console.log(`✓ Published: ${message}`);
      
      // Small delay between messages
      await new Promise(resolve => setTimeout(resolve, MESSAGE_DELAY_MS));
    }

    console.log(`\n${numberOfMessages} messages published successfully!`);

    // Close connection after a short delay
    setTimeout(() => {
      connection.close();
      process.exit(0);
    }, GRACEFUL_SHUTDOWN_DELAY_MS);

  } catch (error) {
    console.error('Error publishing messages:', error.message);
    process.exit(1);
  }
}

console.log('=== RabbitMQ Publisher ===');
publishMessages();
