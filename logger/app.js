'use strict'

const http = require('http')
const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

const router = require('./router')
const config = require('./config')

// initial apps instance
const app = express()
const server = http.createServer(app)


// apply middlewares
app.use(cors())
app.use(bodyParser.json())
app.use('/api', router)

app.get('/', (req, res) => {
    return res.json({ name: 'You know for log' })
})

app.use((req, res, next) => {
    return res.json({ error: 404, url: req.url })
})

// listen
server.listen(config.port, () => {
    console.log('logger server running at port ' + config.port)
})
