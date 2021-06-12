from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
import json
from client.client import Client
import random

app = Flask(__name__)
app.secret_key = 'inder128'

client = None


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == "POST":
		session['username'] = request.form["username"]
		session['ID'] = request.form["ID"]
		if session['ID'] == '':
			session['ID'] = str(random.randint(1000, 9999))
		print(session['ID'])

		global client
		client = Client(session['username'], session['ID'])

		flash(session['username'] + ' Welcome to the Chat Room. \nID of this room is : ' + session['ID'], 'success')
		return redirect(url_for("home"))

	return render_template('login.html')



@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('ID', None)
	if client: client.disconnect()
	return redirect(url_for("login"))



@app.route('/')
def home():
	if client is None:
		flash('Please login first', 'success')
		return redirect(url_for('logout'))

	return render_template('home.html')



@app.route('/sendMessage', methods = ['POST'])
def sendMessage():
	client.send_message(request.form['message'])
	return jsonify()


@app.route('/getMessages')
def getMessages():
	if client:
		return jsonify({"messages" : client.get_messages(), "username" : session['username']})
	else:
		return jsonify()





if __name__ == "__main__":
	app.run(port = 5000, debug = True)
	# app.run(debug = True)