'use strict'

const redis = require('redis')

const config = require('./config')

const client = redis.createClient({
    host: config.redis.host,
    port: config.redis.port,
})

client.on('error', (err) => {
    console.error('connect redis error: ' + err)
})

module.exports = client