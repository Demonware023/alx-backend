import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve seats by setting the number of available seats in Redis
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get the current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
}

// Initialize reservationEnabled and set initial available seats to 50
let reservationEnabled = true;

(async () => {
  await reserveSeat(50);
})();

// Create Kue queue
const queue = kue.createQueue();

// Express server setup
const app = express();
const port = 1245;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errMessage}`);
  });
});

// Route to process the reservation queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();
    
    if (availableSeats > 0) {
      availableSeats -= 1;
      await reserveSeat(availableSeats);

      if (availableSeats === 0) {
        reservationEnabled = false;
      }

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`API running on port ${port}`);
});
