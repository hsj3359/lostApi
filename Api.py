import sqlite3

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/userLogin', methods=['POST'])
def userLogin():
    user = request.get_json()  # json 데이터를 받아옴
    return jsonify(user)  # 받아온 데이터를 다시 전송


@app.route('/')
def environments():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM userTable")
    return jsonify({"num": c.fetchall()})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)