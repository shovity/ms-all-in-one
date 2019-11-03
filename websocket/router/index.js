'use strict'

const express = require('express')

const socketer = require('../engine/socketer')
const config = require('../config')
const io = require('../io')

const router = express.Router()
const namespace = {}

// create namespace map
Object.keys(config.namespace).forEach(k => {
    const name = config.namespace[k]
    namespace[name] = socketer.create(io, name)
})

// handle hook
router.post('/api/emitter', (req, res, next) => {
    const { action, payload, client_id, sid, room, user_id } = req.body
    const clientInfo = config.clientID[client_id]

    if (!clientInfo) {
        return res.json({ error: 'missing or invalid client_id' })
    }

    if (!action) {
        return res.json({ error: 'action is requried' })
    }

    const instance = namespace[clientInfo.namespace]

    if (!instance) {
        return res.json({ error: `namespace ${clientInfo.namespace} not available` })
    }

    if (sid) {
        // sending to a sid
        instance.namespace.to(sid).emit(action, payload)

    } else if (room) {
        // sending to a room
        instance.namespace.in(room).emit(action, payload)

    } else if (user_id) {
        const userIds = Array.isArray(user_id)? user_id : [ user_id ]
        const missUserIds = []

        userIds.forEach(userId => {
            instance.getAllClients((clients) => {
                const userClients = clients.filter(c => c.user.id === userId)

                if (userClients.length === 0) {
                    missUserIds.push(userId)
                    return
                }

                userClients.forEach(client => {
                    instance.namespace.to(client.sid).emit(action, payload)
                })
            })
        })

        return res.json(missUserIds)

    } else {

        // sending to all client
        instance.namespace.emit(action, payload)
    }

    return res.json({})
})

router.get('/:nsp', (req, res, next) => {
    const pstatus = {
        heapUsed: process.memoryUsage().heapUsed / 1024 / 1024,
        cpuUsage: process.cpuUsage(),
    } 

    res.render('home', { nsp: req.params.nsp, pstatus })
})

// response 404
router.use((req, res) => {
    res.json({ error: 404, url: req.originalUrl })
})

module.exports = router