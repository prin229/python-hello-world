import pyodbc 
from flask import Flask , render_template
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
				cursor.execute("SELECT id from demo_tb")
				row = cursor.fetchone()
				while row:
					#print (str(row[0]) + " ")
					res +=str(row[0])+ " "
					row = cursor.fetchone()
		return res;
	except Exception as e:
		      print('error is : '+str(e))


print(printres())
@app.route("/")
def hello():
    return printres()
	

