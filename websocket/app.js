'use strict'

const http = require('http')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const cors = require('cors')

const io = require('./io')
const logger = require('./engine/logger')
const router = require('./router')
const config = require('./config')

// initial apps instance
const app = express()
const server = http.createServer(app)

// attach io to server
io.attach(server)

// set app configs
app.set('view engine', 'pug')

// apply middlewares
app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())
app.use(router)

// listen
server.listen(config.port, () => {
    logger.debug('server realtime interface running at port ' + config.port)
})
