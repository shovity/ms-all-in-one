'use strict'

const express = require('express')
const uuid = require('uuid/v4')
const moment = require('moment')

const logService = require('../../services/logService')

const api = express.Router()


api.get('/', (req, res) => {
    const limit = req.query.limit || 100
    const offset = req.query.offset || 0
    const namespace = req.query.namespace
    const key = req.query.key
    const startTime = req.query.start_time
    const endTime = req.query.end_time

    if (!namespace) {
        return res.json({ error: { message: 'missing namespace' } })
    }

    logService.get({ namespace, key, startTime, endTime, limit, offset }, (error, logs) => {
        return res.json(logs)
    })
})

api.post('/', (req, res) => {

    const { namespace, key, action, message, user, data } = req.body

    if (!namespace || !key || !action || !message) {
        return res.json({ error: { message: 'missing param: namespace || key || action || message' } })
    }

    const id = uuid()
    const created = Date.now()
    
    logService.push({ namespace, key, action, message, user, data, created, id })

    return res.json({ id })
})

module.exports = api
