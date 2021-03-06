from flask import Flask,Blueprint, redirect, url_for, request,render_template, send_file, session
import mysql.connector
from io import BytesIO

mydb = mysql.connector.connect(
    host='34.71.50.183',
    user="root",
    port=3306,
    passwd="alykhaled123",
    database="operationsDB"
)
mydb.autocommit = True

# mycursor = mydb.cursor()

patientBp = Blueprint('patientBp', __name__, template_folder='templates',static_folder='static')

mycursor = mydb.cursor()

@patientBp.route('/')
def patientIndex():
    '''
    This is the index page for the patient that view some statics about latest
    operations and patients that are
    waiting for a patient
    '''
    mycursor.execute("SELECT name,email,username FROM Patient WHERE ssn = "+str(session.get("id")))
    print(session.get("id"))
    result = mycursor.fetchall()[0]
    name = result[0]
    email = result[1]
    username = result[2]
    session['name'] = name
    session['email'] = email
    session['username'] = username

    mycursor.execute("SELECT id,File.name as 'File Name' , Doctor.name as 'Doctor Name', data FROM operationsDB.File Join Doctor ON doctorId = Doctor.ssn Where patientId = "+str(session.get("id"))+";")
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    data = {
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
    }

    return render_template("patientDashboard.html",data=data)

@patientBp.route('/operations')
def viewOperations():
    '''
    This is the page that allows the patient
    to view and to add a new operation to the database
    using there api
    '''
    mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn WHERE Patient.ssn = "+str(1190156))
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    data = {
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
    }
    return render_template("patientViewOperations.html",data=data)

@patientBp.route('/add' ,methods=['POST'])
def addPatient():
    #TODO
    if request.method == 'POST':
        ssn = request.form['ssn']
        name = request.form['name']
        medicalHistory = request.form['medicalHistory']
        illness = request.form['illness']
        bdate = request.form['bdate']
        phone = request.form['phone']
        image = request.files['image']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        Relatives_phone_Number = request.form['Relatives_phone_Number']
        sql = "INSERT INTO `operationsDB`.`Patient` (`ssn`,`name`,`medicalHistory`,`illness`,`bdate`,`phone`,`image`,`username`,`password`,`email`,`address`,`gender`,`Relatives_phone_Number`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val = (ssn,name,medicalHistory,illness,bdate,phone,image.read(),username,password,email,address,gender,Relatives_phone_Number)
        mycursor.execute(sql,val)
        mydb.commit()

    return redirect(url_for('adminBp.viewPatient'))

@patientBp.route('/download/<fileId>')
def downloadFile(fileId):
    #TODO
    mycursor.execute("SELECT id ,name, extension, data FROM File WHERE File.id = "+str(fileId))
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    file_data = mycursor.fetchall()[0]
    return send_file(BytesIO(file_data[3]),attachment_filename=file_data[1], as_attachment=True)

@patientBp.route('/update/<patient_id>' ,methods=['POST','GET'])
def updatePatient(patient_id):
       
    if request.method == 'POST':
        ssn = request.form['ssn']
        name = request.form['name']
        medicalHistory = request.form['medicalHistory']
        illness = request.form['illness']
        bdate = request.form['bdate']
        phone = request.form['phone']
        image = request.files['image']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        Relatives_phone_Number = request.form['Relatives_phone_Number']
        sql = "UPDATE `operationsDB`.`Patient` SET ssn=%s,name=%s,medicalHistory=%s,illness=%s,bdate=%s,phone=%s,image=%s,username=%s,password=%s,email=%s,address=%s,gender=%s,Relatives_phone_Number=%s WHERE ssn="+patient_id
        val = (ssn,name,medicalHistory,illness,bdate,phone,image.read(),username,password,email,address,gender,Relatives_phone_Number)
        mycursor.execute(sql,val)
        mydb.commit()
    return redirect(url_for('adminBp.viewPatient'))

@patientBp.route('/delete/<ssn>' ,methods=['GET'])
def deletePatient(ssn):
    sql = "DELETE FROM Patient WHERE ssn="+ssn
    # val = (int(operation_id))
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('adminBp.viewPatient'))
   

