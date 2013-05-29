from flask import Flask,render_template,request
import json
import MySQLdb
import facebook
import config

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
AUTH_URL = config.AUTH_URL
APP_SECRET = config.APP_SECRET

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html',auth_url = AUTH_URL)


	
@app.route('/game',methods=['GET','POST'])
def game():
	if request.method == 'POST':
		if 'signed_request' in request.form:
			print " Yes Signed Request obtained"
		else:
			print " No Signed Request Obtained"

		return render_template('game.html')
	else:
		return render_template('game.html')

if __name__ == '__main__':
	app.run()


