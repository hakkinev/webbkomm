import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS 
from dotenv import load_dotenv

load_dotenv()

PORT=8167 # hakkinevs port

db_url = os.environ.get("DB_URL")
print(os.environ.get("ASD"))

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

rooms = [
    {"number": 101, "type": "Standard ", "price": 100},
    {"number": 102, "type": "Deluxe ", "price": 200},
    {"number": 103, "type": "Family ", "price": 150}
]

@app.route("/test", )
def dbtest():
    with conn.cursor() as cur:
        cur.execute("SELECT * from people")
        rows = cur.fetchall()
        return rows

@app.route("/", )
def info():
    #return "<h1>Hello, Flask!</h1>"
    return "Hotel API, endpoints /rooms, /bookings"

@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endpoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        rooms.append(request_body)
        return {
            'msg' :f"Du har skapat en nytt rum, id är {len(rooms)-1}"
        }
    else:
        return rooms

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE' ])
def one_room_endpoint(id):
    if request.method == 'GET':
        return rooms[id]
    if request.method == 'PUT' or request.method == 'PATCH':
        return {
            'msg' :f"Du uppdaterar id: {id} ",
            'method' : request.method
        }
    if request.method == 'DELETE':
        return {
            'msg' :f"Du har raderat id: {id} ",
            'method' : request.method
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
