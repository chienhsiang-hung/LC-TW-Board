export var allValues

const { MongoClient } = require("mongodb");

// Connection URI
const uri =
  "mongodb+srv://guest_for_LC-TW-Board:oB5FomLHVAYJ7jLo@chienhsiang-hung.smnnaxp.mongodb.net/?retryWrites=true&w=majority";

// Create a new MongoClient
const client = new MongoClient(uri);

async function run() {
  try {
    // Connect the client to the server (optional starting in v4.7)
    await client.connect();

    const database = client.db('LC-TW-Board');
    const collection = database.collection('main');
    const query = { currentGlobalRanking: 15 };
    const record = await collection.findOne(query);
    console.log(record);

    const cursor = collection.find({});
    // await cursor.forEach(doc => console.log(doc));
    var allValues = await cursor.toArray();
    console.log(allValues);

    // Establish and verify connection
    await client.db("LC-TW-Board").command({ ping: 1 });
    console.log("Connected successfully to server");
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);
