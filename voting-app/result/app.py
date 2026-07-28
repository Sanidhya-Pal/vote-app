from flask import Flask, render_template
import psycopg2
import time

app = Flask(__name__)

# Wait until PostgreSQL is ready
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


@app.route("/")
def results():

    cursor.execute("""
        SELECT vote, COUNT(*)
        FROM votes
        GROUP BY vote
    """)

    rows = cursor.fetchall()

    cats = 0
    dogs = 0

    for vote, count in rows:

        if vote == "Cats":
            cats = count

        elif vote == "Dogs":
            dogs = count

    return render_template(
        "index.html",
        cats=cats,
        dogs=dogs
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
