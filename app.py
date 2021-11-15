from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key="ChallengeEnsolvers"

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' #input('DB PASSWORD: ')
app.config['MYSQL_DATABASE_DB'] = 'prueba1'
mysql.init_app(app)


@app.route('/')
def index():
	sql = "SELECT * FROM `prueba1`.`tasks`;"
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	tasks = cursor.fetchall()

	return render_template('tasks/index.html', tasks= tasks)

@app.route('/destroy/<int:id>')
def destroy(id):
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute("DELETE FROM `prueba1`.`tasks` WHERE id=%s", (id))
	conn.commit()

	return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM `prueba1`.`tasks` WHERE id=%s", (id))
	tasks = cursor.fetchall()

	return render_template('tasks/edit.html', tasks=tasks)

@app.route('/update', methods=['POST'])
def update():
	_name = request.form['txtName']
	id = request.form['txtID']

	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(f'/edit/{id}')

	sql = "UPDATE `prueba1`.`tasks` SET `name`=%s WHERE id=%s;"
	datos =(_name, id)
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute(sql, datos)
	conn.commit()

	return redirect('/')

@app.route('/check', methods=['POST'])
def check():
	print(request.form['txtCheck'])
	if request.form['txtCheck'] == '1':
		_check = 0 
	else:
		_check = 1
	id = request.form['txtID']

	sql = "UPDATE `prueba1`.`tasks` SET `check`=%s WHERE id=%s;"
	datos =(_check, id)
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute(sql, datos)
	conn.commit()

	return redirect('/')

@app.route('/create')
def create():
	return render_template('tasks/create.html')

@app.route('/store', methods=['POST'])
def storage():
	_name = request.form['txtName']
	
	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(url_for('create'))

	sql = "INSERT INTO `prueba1`.`tasks` (`name`) VALUES (%s);"
	datos =(_name)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()

	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
