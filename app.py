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


##################TASKS#########################

@app.route('/')
def index_task():
	sql = "SELECT * FROM `prueba1`.`tasks` WHERE `tasks`.`id_folder` IS NULL;"
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	tasks = cursor.fetchall()

	return render_template('tasks/index_task.html', tasks= tasks)

@app.route('/destroy_task/<int:id>')
def destroy_task(id):
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute("DELETE FROM `prueba1`.`tasks` WHERE id=%s", (id))
	conn.commit()

	return redirect('/')

@app.route('/edit_task/<int:id>')
def edit_task(id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM `prueba1`.`tasks` WHERE id=%s", (id))
	tasks = cursor.fetchall()

	return render_template('tasks/edit_task.html', tasks=tasks)

@app.route('/update_task', methods=['POST'])
def update_task():
	_name = request.form['txtName']
	id = request.form['txtID']

	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(f'/edit_task/{id}')

	sql = "UPDATE `prueba1`.`tasks` SET `name`=%s WHERE id=%s;"
	datos =(_name, id)
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute(sql, datos)
	conn.commit()

	return redirect('/')

@app.route('/check_task', methods=['POST'])
def check_task():
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

	if request.form['txtNameFolder']:
		folder = request.form['txtNameFolder']
		return redirect(f'/{folder}/items')

	return redirect('/')

@app.route('/create_task')
def create_task():
	return render_template('tasks/create_task.html')

@app.route('/store_task', methods=['POST'])
def storage_task():
	_name = request.form['txtName']
	#_id_folder = request.form['txtIDfolder']
	
	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(url_for('create_task'))

	sql = "INSERT INTO `prueba1`.`tasks` (`name`) VALUES (%s);"# formatear id_folder
	datos =(_name)# agregar id_folder
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()

	# if request.form['txtNameFolder']:
	# 	folder = request.form['txtNameFolder']
	# 	return redirect(f'/{folder}/items')

	return redirect('/')


##################FOLDERS#########################

@app.route('/folders')
def index_folder():
	sql = "SELECT * FROM `prueba1`.`folders`;"
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	folders = cursor.fetchall()

	return render_template('folders/index_folder.html', folders= folders)

@app.route('/<string:folder>/items')
def index_folder_items(folder):
	sql = '''
	SELECT * 
	FROM `prueba1`.`tasks`, `prueba1`.`folders` 
	WHERE `tasks`.`id_folder`=`folders`.`id`
	AND `folders`.`name` LIKE %s;
	'''
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql, (folder))
	items = cursor.fetchall()

	return render_template('tasks/index_task.html', tasks= items)

@app.route('/destroy_folder/<int:id>')
def destroy_folder(id):
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute("DELETE FROM `prueba1`.`folders` WHERE id=%s", (id))
	conn.commit()

	return redirect('/folders')

@app.route('/edit_folder/<int:id>')
def edit_folder(id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM `prueba1`.`folders` WHERE id=%s", (id))
	folders = cursor.fetchall()

	return render_template('folders/edit_folder.html', folders=folders)

@app.route('/update_folder', methods=['POST'])
def update_folder():
	_name = request.form['txtName']
	id = request.form['txtID']

	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(f'/edit_folder/{id}')

	sql = "UPDATE `prueba1`.`folders` SET `name`=%s WHERE id=%s;"
	datos =(_name, id)
	conn=mysql.connect()
	cursor= conn.cursor()
	cursor.execute(sql, datos)
	conn.commit()

	return redirect('/folders')

@app.route('/create_folder')
def create_folder():
	return render_template('folders/create_folder.html')

@app.route('/store_folder', methods=['POST'])
def storage_folder():
	_name = request.form['txtName']
	
	#data validation
	if _name=='':
		flash('Remember fill the field')
		return redirect(url_for('create_folder'))

	sql = "INSERT INTO `prueba1`.`folders` (`name`) VALUES (%s);"
	datos =(_name)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()

	return redirect('/folders')


if __name__ == '__main__':
	app.run(debug=True)
