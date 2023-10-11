from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
import pickle
import numpy as np

model = pickle.load(open('migraine.pkl', 'rb'))

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/', methods = ['GET'])
def function():
	return render_template('login.html')
	
@app.route('/insert', methods = ['GET','POST'])
def insert():
	cur = mysql.connection.cursor()
	if request.method == "POST":
		name = request.form['name']
		username = request.form['username']
		phone = request.form['phone']
		mail = request.form['mail']
		state = request.form['state']
		password = request.form['password']
		

		if name == "" and username == "" and phone == "" and mail == "" and state == "" and password == "":
			return render_template('result.html', result = "Please enter valid data")
		else:
			params = [mail, username]
			count = cur.execute("SELECT * FROM users WHERE mail = %s and username = %s", params)
			if count != 0:
				return render_template('result.html', result = "This mail id or username is already registerd, plesae enter another mail id or username")
			else:
				cur.execute("INSERT INTO users (Name, Username, PhoneNo, Mail, State, Password) VALUES (%s, %s, %s, %s, %s, %s)", (name, username, phone, mail, state, password))
				mysql.connection.commit()
				return render_template('index.html')
	else:
		return render_template('signup.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	cur = mysql.connection.cursor()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		param = [username, password]
		c = cur.execute("SELECT * FROM users WHERE username = %s and password = %s", param)
		if c == 1:
			return render_template('index.html')
		else:
			return render_template('result.html', result = "Oops! incorrect username or password. Please enter correct details.")
	else:
		return render_template('login.html')

@app.route('/predict', methods = ['GET','POST'])
def migraine():
	if request.method == 'POST':
		data1 = request.form['b']
		data2 = request.form['c']
		data3 = request.form['d']
		data4 = request.form['e']
		data5 = request.form['f']
		data6 = request.form['g']
		data7 = request.form['h']
		data8 = request.form['i']
		data9 = request.form['j']
		data10 = request.form['k']
		data11 = request.form['l']
		data12 = request.form['m']
		data13 = request.form['n']
		data14 = request.form['o']
		data15 = request.form['p']
		data16 = request.form['q']
		data17 = request.form['r']
		data18 = request.form['s']
		data19 = request.form['t']
		data20 = request.form['u']
		data21 = request.form['v']
		data22 = request.form['w']
		data23 = request.form['x']
		arr = np.array([[data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23]], dtype = float)
	
		if(model.predict(arr) == 0):
			return render_template('result.html', result = "Basilar Type Aura")
		elif(model.predict(arr) == 1):
			return render_template('result.html', result = "Familial Hemiplegic Migraine")
		elif(model.predict(arr) == 2):
			return render_template('result.html', result = "Migraine Without Aura")
		elif(model.predict(arr) == 3):
			return render_template('result.html', result = "Other")
		elif(model.predict(arr) == 4):
			return render_template('result.html', result = "Sporadic Hemiplegic Migraine")
		elif(model.predict(arr) == 5):
			return render_template('result.html', result = "Typical Aura With Migraine")
		elif(model.predict(arr) == 6):
			return render_template('result.html', result = "Typical Aura Without Migraine")
	else:
		return render_template('login.html')

if __name__ == '__main__':
	app.run(debug = True)