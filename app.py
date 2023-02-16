import pyodbc 
from flask import Flask , render_template,request
app = Flask(__name__)

def printres():
	server = 'sql-demo-serv.database.windows.net'
	database = 'sql-demo'
	username = 'prince'
	password = 'Azure@feb2023'   
	driver= '{ODBC Driver 18 for SQL Server}'
	res=""
	try:
		with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT * from demo_tb")
				row = cursor.fetchone()
				while row:
					#print (str(row[0]) + " ")
					res +=str(row[0])+ " "+str(row[1])+"</br>"
					row = cursor.fetchone()
		return res;
	except Exception as e:
		      print('error is : '+str(e))

@app.route('/handle_data', methods=['POST'])
def handle_data():
	table_name = request.form['table']
	schema_name=request.form['schema']
	email_name=request.form['email']
	metrics=request.form.getlist('metrics')
	server = 'sql-demo-serv.database.windows.net'
	database = 'sql-demo'
	username = 'prince'
	password = 'Azure@feb2023'   
	driver= '{ODBC Driver 18 for SQL Server}'
	cnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	# Do the insert
	try:
		cursor.execute("insert into demo_tb values ( 6 , 'awesome library')")
		#commit the transaction
		cnxn.commit()
		return "Inserted Successfully"
	except Exception as e:
		print('error is :'+str(e))
	

@app.route("/")
def hello():
    return render_template('profile-tool.html')
	

