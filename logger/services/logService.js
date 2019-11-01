'user strict'

// data:log:{namespace} HASH
//  key => log.id
//  value => log.row_data
 
// index:log:{namespace}:created  ZSET
//  value => log.id
//  scrore => created

// index:log:{namespace}:key:{key}  ZSET
//  value => log.id
//  scrore => created

// index:log:{namespace}:action:{action}  ZSET
//  value => log.id
//  scrore => created


const redis = require('../redis')

const logService = {}

logService.push = (log) => {
    redis.multi()
        .hset(`data:log:${log.namespace}`, log.id, JSON.stringify(log))
        .zadd(`index:log:${log.namespace}:created`, log.created, log.id)
        .zadd(`index:log:${log.namespace}:key:${log.key}`, log.created, log.id)
        .zadd(`index:log:${log.namespace}:action:${log.action}`, log.created, log.id)
        .exec((error, replies) => {
            if (error) {
                console.error(error)
            }
        })
}

logService.get = (query, done) => {
    const { namespace, key, startTime, endTime, limit, offset  } = query || {}
    
    redis.zrange(`index:log:${namespace}:created`, -offset - limit, -offset - 1, (error, logIds) => {
        if (error) {
            done(error)
        } else {
            logIds.reverse()

            redis.hmget(`data:log:${namespace}`, logIds, (error, logs) => {
                if (error) {
                    done(error)
                } else {
                    done(null, { data: logs.map(l => JSON.parse(l)) })
                }
            })
        }
    })
}

module.exports = logService
