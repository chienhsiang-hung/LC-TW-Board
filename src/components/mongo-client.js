const { MongoClient } = require('mongodb');

class MongoCli {
    constructor() {
        let url = `mongodb://guest_for_LC-TW-Board:WfMBILY1jNkTZdJ6@@chienhsiang-hung.smnnaxp.mongodb.net/?retryWrites=true&w=majority`
        this.client = new MongoClient(url, { useUnifiedTopology: true });
    }

    async init() {
        if (this.client) {
            await this.client.connect();
            this.db = this.client.db('LC-TW-Board');
        } else {
            console.warn("Client is not initialized properly");
        }
    }
}

module.exports = new MongoCli();