'use strict'

const express = require('express')

const apiV1 = require('./v1')

const router = express.Router()

router.use('/v1', apiV1)

module.exports = router
