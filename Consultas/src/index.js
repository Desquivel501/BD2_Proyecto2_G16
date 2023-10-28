import express from 'express'
import { MongoClient, ServerApiVersion  } from 'mongodb'
import dotenv from 'dotenv'

dotenv.config()

var mongoURL = process.env.MONGO_HOST

const client = new MongoClient(mongoURL, { serverApi: ServerApiVersion.v1 });

const db = client.db("bd2-proyecto2");
const coll = db.collection("games");


var app = express()        
app.use(express.json());  

var port = 3000


app.get('/', function(req, res) {
  res.json({ mensaje: '¡Hola Mundo!' })   
})


app.get('/consulta1', async function(req, res) {
    let result = await coll.aggregate([
        {
          $sort: {
            rating: -1,
            aggregated_rating: -1,
          },
        },
        {
          $limit: 100,
        },
        {
          $project: {
            name: 1,
            platforms: 1,
            rating: 1,
            aggregated_rating: 1,
            genres: 1,
          },
        },
      ]).toArray()

    res.json(result)
})

app.post('/consulta2', async function(req, res) {

    console.log(req.body)

    let data = req.body
    let re = new RegExp(data.name, 'i')

    let result = await coll.aggregate([
        {
          $match: {
            name: {
              $regex: re,
            },
          },
        },
        {
          $sort: {
            rating: -1,
            aggregated_rating: -1,
          },
        },
      ]).toArray()

    res.json(result)
})


app.post('/consulta3', async function(req, res) {

    console.log(req.body)

    let data = req.body
    let re = new RegExp(data.name, 'i')

    let result = await coll.aggregate([
        {
          $match: {
            name: {
              $regex: re,
            },
          },
        },
        {
          $sort: {
            platforms: -1,
            rating: -1,
            aggregated_rating: -1,
          },
        },
      ]).toArray()

    res.json(result)
})


app.get('/consulta4', async function(req, res) {

    let result = await coll.aggregate([
        {
          $project: {
            lan_count: {
              $size: {
                $ifNull: ["$language_supports", []],
              },
            },
            name: 1,
            rating: 1,
            aggregated_rating: 1,
            language_supports: 1,
          },
        },
        {
          $sort: {
            lan_count: -1,
            rating: -1,
            aggregated_rating: -1,
            name: -1,
          },
        },
        {
          $limit: 100,
        },
      ]).toArray()

    res.json(result)
})


app.post('/consulta5', async function(req, res) {

    var data = req.body

    let result = await coll.aggregate([
        {
          $match: {
            'genres': data.genre,
          },
        },
        {
          $sort: {
            aggregated_rating: -1,
            rating: -1,
          },
        },
      ]).toArray()

    res.json(result)
})


app.post('/platforms', async function(req, res) {

    var data = req.body

    var query = {}

    if(data.name){
        let re = new RegExp(data.name, 'i')
        query = {
            name: {
                $regex: re,
            }
          }
    }

    if(data.alternative_name){
        let re = new RegExp(data.alternative_name, 'i')
        query = {
            alternative_name: {
                $regex: re,
            }
          }
    }

    let result = await client.db("bd2-proyecto2").collection("platforms").aggregate([
        {
          $match: query,
        },
        {
          $sort: {
            name: -1,
          },
        },
      ]).toArray()

    res.json(result)
})



app.listen(port)
console.log('API escuchando en el puerto ' + port)