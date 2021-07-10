import redis
from rq import Queue
from server import config

# get redis connection
redis_connection = redis.from_url(config.DevelopmentConfig.REDIS_URL)

# get rq queue with redis connection
queue = Queue(connection=redis_connection)

def get_job_from_id(job_id):
    job = queue.fetch_job(job_id)
    return job