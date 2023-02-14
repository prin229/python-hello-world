import pyodbc 
from flask import Flask , render_template
app = Flask(__name__)

def printres():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=sql-demo-serv.database.windows.net;DATABASE=sql-demo;UID=prince;PWD=Azure@feb2023')
	cursor = cnxn.cursor()	
	cursor.execute("select * from demo_tb") 
	row = cursor.fetchone() 
	while row:
		print (row) 
		row = cursor.fetchone()
		return row


@app.route("/")
def hello():
    return printres()
