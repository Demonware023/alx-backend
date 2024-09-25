export default function createPushNotificationsJobs(jobs, queue) {
  // Check if the jobs argument is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Iterate over each job in the jobs array
  jobs.forEach((jobData) => {
    // Create a new job in the queue for 'push_notification_code_3'
    const job = queue.create('push_notification_code_3', jobData);

    // When the job is saved successfully
    job.on('enqueue', () => {
      console.log(`Notification job created: ${job.id}`);
    });

    // When the job is completed
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // When the job fails
    job.on('failed', (errorMessage) => {
      console.log(`Notification job ${job.id} failed: ${errorMessage}`);
    });

    // When the job makes progress
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

    // Save the job in the queue
    job.save();
  });
}
