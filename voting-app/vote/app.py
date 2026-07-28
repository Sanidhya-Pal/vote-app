from flask import Flask, render_template, request
import redis

app = Flask(__name__)

# Connect to the Redis container
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.route("/", methods=["GET", "POST"])
def vote():

    if request.method == "POST":
        choice = request.form["vote"]

        # Push the vote into the Redis list named "votes"
        redis_client.rpush("votes", choice)

        return f"You voted for {choice}"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
