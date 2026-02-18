const amqp = require('amqplib');

const QUEUE_NAME = 'example_queue';
const RABBITMQ_URL = 'amqp://guest:guest@localhost:5672';

async function consumeMessages() {
  try {
    console.log('Connecting to RabbitMQ...');
    const connection = await amqp.connect(RABBITMQ_URL);
    const channel = await connection.createChannel();

    await channel.assertQueue(QUEUE_NAME, { durable: false });

    console.log(`Waiting for messages in queue '${QUEUE_NAME}'...`);
    console.log('To exit, press CTRL+C\n');

    channel.consume(QUEUE_NAME, (msg) => {
      if (msg !== null) {
        const messageContent = msg.content.toString();
        console.log(`✓ Received: ${messageContent}`);
        
        // Process the message (simulate some work)
        processMessage(messageContent);
        
        // Acknowledge the message
        channel.ack(msg);
      }
    });

  } catch (error) {
    console.error('Error consuming messages:', error.message);
    process.exit(1);
  }
}

function processMessage(message) {
  // Simulate processing the message
  console.log(`  → Processing message...`);
  
  // Extract timestamp and content
  const timestampMatch = message.match(/\[(.*?)\]/);
  const timestamp = timestampMatch ? timestampMatch[1] : 'Unknown time';
  const content = message.replace(/\[.*?\]\s*/, '');
  
  console.log(`  → Timestamp: ${timestamp}`);
  console.log(`  → Content: ${content}`);
  console.log(`  → Processing completed!\n`);
}

console.log('=== RabbitMQ Consumer ===');
consumeMessages();
