const config = {}

config.namespace = {
    dev: 'dev',
    pro: 'pro',
}

config.redis  = {
    host: 'redis',
    port: 6379,
}

config.clientID = {
    'Z6FBx8A4UV': {
        'name': 'Isomnia',
        'namespace': config.namespace.dev,
    },
    'l8xrzhoy5v': {
        'name': 'Django develop server',
        'namespace': config.namespace.dev,
    },
    'iPCP6C5tTRQTWhkm5tGg0FL8qc6T4Agr': {
        'name': 'Django production server',
        'namespace': config.namespace.pro,
    },
}

module.exports =  config