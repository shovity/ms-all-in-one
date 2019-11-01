'use strict'

const express = require('express')

const v1 = express.Router()

v1.use('/log', require('./log'))

module.exports = v1