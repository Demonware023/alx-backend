import kue from 'kue';

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send a notification
function sendNotification(phoneNumber, message, job, done) {
  // Track initial progress (0%)
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // If blacklisted, fail the job
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Track progress to 50%
  job.progress(50, 100);

  // Log notification details
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Complete the job successfully
  done();
}

// Create the Kue queue
const queue = kue.createQueue();

// Process jobs from 'push_notification_code_2' queue, with two jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
