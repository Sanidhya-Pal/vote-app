import redis
import psycopg2
import time

print("Worker starting...")

# Wait for Redis
while True:
    try:
        redis_client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )
        redis_client.ping()
        print("Connected to Redis")
        break
    except:
        print("Waiting for Redis...")
        time.sleep(2)

# Wait for PostgreSQL
while True:
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="votingdb",
            user="postgres",
            password="password"
        )
        cursor = conn.cursor()
        print("Connected to PostgreSQL")
        break
    except:
        print("Waiting for PostgreSQL...")
        time.sleep(2)

# Read votes forever
while True:

    vote = redis_client.lpop("votes")

    if vote:

        print(f"Saving vote: {vote}", flush=True)

        cursor.execute(
            "INSERT INTO votes (vote) VALUES (%s)",
            (vote,)
        )

        conn.commit()

    time.sleep(1)
