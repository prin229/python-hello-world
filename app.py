import pyodbc 
import os
import uuid
import sys
import csv
from azure.storage.blob import BlockBlobService, PublicAccess
from flask import Flask , render_template,request
app = Flask(__name__)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    table_name = request.form['table']
    schema_name=request.form['schema']
    email_name=request.form['email']
    metrics=request.form.getlist('metrics')
    try:
        # Create the BlockBlobService that is used to call the Blob service for the storage account
        blob_service_client = BlockBlobService(
            account_name='blobinputdata', account_key='ogHP2hQWPtChoxFXA0CXF6S1HtykpyZ0kg0fL9/K9BbxH7U9eiUb/WbesMEUz6XrrDv8ro1tO0PR+ASt2HmXqg==')

        # Create a container called 'quickstartblobs'.
        container_name = 'quickstartblobs'
        blob_service_client.create_container(container_name)

        # Set the permission so the blobs are public.
        blob_service_client.set_container_acl(
            container_name, public_access=PublicAccess.Container)

        # Create Sample folder if it not exists, and create a file in folder Sample to test the upload and download.
        local_path = os.path.expanduser("~/Sample")
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("~/Sample"))
        local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".csv"
        full_path_to_file = os.path.join(local_path, local_file_name)

		# Write text to the file.
        header = ['schema', 'table', 'email', 'metrics']
        data = [schema_name, table_name, email_name, metrics]
        file = open(full_path_to_file,  'w',encoding='UTF8')
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)
        file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        blob_service_client.create_blob_from_path(
            container_name, 'input/'+local_file_name, full_path_to_file)

        # List the blobs in the container
        #print("\nList blobs in the container")
        #generator = blob_service_client.list_blobs(container_name)
        #for blob in generator:
            #print("\t Blob name: " + blob.name)

        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
        #full_path_to_file2 = os.path.join(local_path, str.replace(
        #   local_file_name ,'.txt', '_DOWNLOADED.txt'))
        #print("\nDownloading blob to " + full_path_to_file2)
        #blob_service_client.get_blob_to_path(
            #container_name, local_file_name, full_path_to_file2)

        #sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
        #                 "application will exit.")
        #sys.stdout.flush()
        #input()

        # Clean up resources. This includes the container and the temp files
        #blob_service_client.delete_container(container_name)
        os.remove(full_path_to_file)
        return render_template('success.html')
        #os.remove(full_path_to_file2)
    except Exception as e:
        print(e)
        return render_template('error.html')

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

#run_sample()
#@app.route('/handle_data', methods=['POST'])
def check_data_arch():
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
		return render_template('success.html')
	except Exception as e:
		return render_template('error.html')
	

#handle_data()
@app.route("/")
def hello():
    return render_template('profile-tool.html')
	

