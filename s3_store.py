from flask import Flask,render_template,request
import boto,base64
import boto.s3.connection
from cryptography.fernet import Fernet

app=Flask(__name__)
s3=boto.connect_s3("AKIAI4IO35AB6GLDATKA","wNGAPV6UK3A6lyg8VFafMLkpNCQ7YaybQiUgwk39")
bucket=s3.get_bucket('cloud2-storage')
key=base64.urlsafe_b64encode("gh54ygtg45ythdf3er32g3u71y7i86u=".encode())
crypto=Fernet(key)

def readbytesfile(file_name):
	data=""
	with open(file_name,'rb') as file_upload:
		data=crypto.encrypt(file_upload.read())
	return data

@app.route("/")
def main():
	keys=[]
	for key in bucket.list():
		keys.append(key)
	return render_template("main_page.html",keys=keys)

@app.route("/upload",methods=['POST'])
def upload():
	file_name=request.form['uploadfile']
	data=readbytesfile(file_name)
	key1=bucket.new_key(file_name)
	key1.set_contents_from_string(data)
	keys=[]
	for key1 in bucket.list():
		keys.append(key1)
	return render_template("main_page.html",keys=keys,message1="File Uploaded")

@app.route("/download")
def download():
	file_name=request.args['file_name']
	key1=bucket.get_key(file_name)
	key1.get_contents_to_filename(file_name)
	with open(file_name,'rb+') as f:
		content=f.read()
		f.seek(0)
		f.write(crypto.decrypt(content))
		f.truncate()
	keys=[]
	for key1 in bucket.list():
		keys.append(key1)
	return render_template("main_page.html",keys=keys,message1="File Downloaded")

if __name__=="__main__":
	app.run(host='0.0.0.0',port=8080)