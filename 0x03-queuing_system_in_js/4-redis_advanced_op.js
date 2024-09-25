import redis from 'redis';

// Create Redis client
const client = redis.createClient();

// Handle connection events
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Function to create the hash HolbertonSchools with the specified fields and values
function createHolbertonSchoolsHash() {
  client.hset('HolbertonSchools', 'Portland', 50, redis.print);
  client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
  client.hset('HolbertonSchools', 'New York', 20, redis.print);
  client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
  client.hset('HolbertonSchools', 'Cali', 40, redis.print);
  client.hset('HolbertonSchools', 'Paris', 2, redis.print);
}

// Function to display the HolbertonSchools hash
function displayHolbertonSchoolsHash() {
  client.hgetall('HolbertonSchools', (err, obj) => {
    if (err) {
      console.error(`Error retrieving hash: ${err}`);
    } else {
      console.log(obj);
    }
  });
}

// Call the functions to create and display the hash
createHolbertonSchoolsHash();
displayHolbertonSchoolsHash();
