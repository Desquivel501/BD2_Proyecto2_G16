
import { MongoClient } from 'mongodb'
import dotenv from 'dotenv'
dotenv.config()

var url = process.env.MONGO_HOST

export const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true })