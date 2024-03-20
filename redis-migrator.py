import redis

def migrate_redis_data(source_host, source_port, destination_host, destination_port):
    # Connect to source Redis server
    source_redis = redis.StrictRedis(host=source_host, port=source_port, decode_responses=True)

    # Connect to destination Redis server
    destination_redis = redis.StrictRedis(host=destination_host, port=destination_port)

    # Get list of keys from source Redis
    keys = source_redis.keys()

    # Migrate keys from source to destination Redis
    for key in keys:
        key_type = source_redis.type(key)
        if key_type == 'string':
            value = source_redis.get(key)
            destination_redis.set(key, value)
        elif key_type == 'list':
            values = source_redis.lrange(key, 0, -1)
            for value in values:
                destination_redis.rpush(key, value)
        elif key_type == 'set':
            values = source_redis.smembers(key)
            for value in values:
                destination_redis.sadd(key, value)
        elif key_type == 'zset':
            values_with_scores = source_redis.zrange(key, 0, -1, withscores=True)
            for value, score in values_with_scores:
                destination_redis.zadd(key, {value: score})
        elif key_type == 'hash':
            fields_and_values = source_redis.hgetall(key)
            destination_redis.hmset(key, fields_and_values)

    print("Data migration completed.")

# Example configuration
source_host = 'localhost'  # or source_host = '127.0.0.1'
source_port = 6379
destination_host = '1.3.3.7' # the public ip address for the destination host
destination_port = 6379

migrate_redis_data(source_host, source_port, destination_host, destination_port)
