from flask import Flask,Blueprint, redirect, url_for, request,render_template, session
import mysql.connector

# mycursor = mydb.cursor()

nurseBp = Blueprint('nurseBp', __name__, template_folder='templates',static_folder='static')
mydb = mysql.connector.connect(
    host='34.71.50.183',
    user="root",
    port=3306,
    passwd="alykhaled123",
    database="operationsDB"
)
mycursor = mydb.cursor()
mydb.autocommit = True

@nurseBp.route('/')
def nurseIndex():
    '''
    This is the index page for the doctor that view some statics about latest
    operations and patients that are
    waiting for a doctor
    '''
    session["id"] = "65566"
    mycursor.execute("SELECT Operation.operationName AS 'Operation Name', Operation.date AS 'Date' FROM operationsDB.Nurse_has_Operation JOIN Operation ON OperationID = Operation.id WHERE NurseSSN="+ session.get("id") )
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    nurseOperationsAll = mycursor.fetchall()
    nurseOperations = {
        'message':"data retrieved",
        'rec':nurseOperationsAll,
        'header':row_headers
    }
    return render_template("nurseDashboard.html",data=nurseOperations)

@nurseBp.route('/operations')
def viewOperations():
    '''
    This is the page that allows the doctor
    to view and to add a new operation to the database
    using there api
    '''
    search = request.args.get('search')
    date = request.args.get('date')
    type = request.args.get('type')
    if type == 'name':
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID WHERE Operation.operationName LIKE '%"+search+"%'")
    elif type == 'patient':
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID WHERE Patient.name LIKE '%"+search+"%'")
    elif type == 'id':
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID WHERE Operation.id LIKE '%"+search+"%'")
    elif type == 'doctor':
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID WHERE Doctor.name LIKE '%"+search+"%'")
    elif type == 'date':
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID WHERE date LIKE '%"+date+"%'")
    else :
        mycursor.execute("SELECT id as ID ,operationName as 'Operation Name', Patient.name as 'Patient Name', Doctor.name as 'Doctor Name', date as Date,startTime as 'Start Time', endTime as 'End Time', Room_Location AS 'Room Location' FROM Operation JOIN Patient ON Operation.patientId = Patient.ssn JOIN Doctor on Operation.doctorID = Doctor.ssn JOIN `Operation Room` ON roomId = Operation_Room_ID")
    
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    data = {
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
    }
    return render_template("nurseViewOperations.html",data=data)

@nurseBp.route('/patients')
def viewPatients():
    '''
    This is the page that allows the doctor
    to view patients in a table
    '''

    search = request.args.get('search')
    type = request.args.get('type')
    if type == 'name':
        mycursor.execute("SELECT ssn as SSN,name as Name ,phone as 'Phone Number',illness as Illness,2022-YEAR(bdate) as AGE FROM operationsDB.Patient WHERE Patient.name  LIKE '%"+search+"%'")
    elif type == 'ssn':
        mycursor.execute("SELECT ssn as SSN,name as Name ,phone as 'Phone Number',illness as Illness,2022-YEAR(bdate) as AGE FROM operationsDB.Patient WHERE Patient.ssn LIKE '%"+search+"%'")
    elif type == 'age':
        mycursor.execute("SELECT ssn as SSN,name as Name ,phone as 'Phone Number',illness as Illness,2022-YEAR(bdate) as AGE FROM operationsDB.Patient WHERE Patient.bdate LIKE '%"+search+"%'")
    
    else :
        mycursor.execute("SELECT ssn as SSN,name as Name ,phone as 'Phone Number',illness as Illness,2022-YEAR(bdate) as AGE FROM operationsDB.Patient")
    
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    data = {
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
    }
    return render_template("nurseViewPatients.html",data=data)

@nurseBp.route('/rooms')
def viewRooms():
    '''
    This is the page that allows the doctor
    to view rooms in a table
    '''

    search = request.args.get('search')
    type = request.args.get('type')
    if type == 'location':
        mycursor.execute("SELECT * FROM operationsDB.`Operation Room` WHERE Room_Location LIKE '%"+search+"%'")
    elif type == 'id':
        mycursor.execute("SELECT * FROM operationsDB.`Operation Room` WHERE Operation_Room_ID LIKE '%"+search+"%'")
    else :
        mycursor.execute("SELECT * FROM operationsDB.`Operation Room`;")
    
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    data = {
        'message':"data retrieved",
        'rec':myresult,
        'header':row_headers
    }
    return render_template("nurseViewRooms.html",data=data)

@nurseBp.route('/add' ,methods=['POST'])
def addNurse():
     
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ssn = request.form['ssn']
        SuperSSN = request.form['SuperSSN']
        biography = request.form['biography']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        phone = request.form['phone']
        address = request.form['address']
        image = request.files['image']
        salary=request.form['Salary']
        if SuperSSN == '':
            SuperSSN = 'NULL'
            
        sql = "INSERT INTO `operationsDB`.`Nurse` (`ssn`, `name`, `birthdate`, `address`, `superSsn`, `salary`, `biography`, `phone`, `gender`,`username`,`email`,`password`,`image`) VALUES (%s,%s,%s,%s,"+SuperSSN+",%s,%s,%s,%s,%s,%s,%s,%s);"
        
        val = (ssn,name,birthdate,address,salary,biography,phone,gender,username,email,password,image.read())
        mycursor.execute(sql,val)
        mydb.commit()

    return redirect(url_for('adminBp.viewNurses'))

@nurseBp.route('/update/<ssn>' ,methods=['POST', 'GET'])
def updateNurse(ssn):

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ssn = request.form['ssn']
        SuperSSN = request.form['SuperSSN']
        biography = request.form['biography']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        phone = request.form['phone']
        address = request.form['address']
        image = request.files['image']
        salary=request.form['Salary']
        if SuperSSN == '':
            SuperSSN = 'NULL'

        
        if image.filename == '':
            sql = "UPDATE `operationsDB`.`Nurse` SET ssn=%s,name=%s,birthdate=%s,address=%s,superSsn="+SuperSSN+",salary=%s,biography=%s,phone=%s,gender=%s,username=%s,email=%s,password=%s WHERE ssn="+ssn
            val = (ssn,name,birthdate,address,salary,biography,phone,gender,username,email,password)
            mycursor.execute(sql,val)
            mydb.commit()
        else:
            sql = "UPDATE `operationsDB`.`Nurse` SET ssn=%s,name=%s,birthdate=%s,address=%s,superSsn="+SuperSSN+",salary=%s,biography=%s,phone=%s,gender=%s,username=%s,email=%s,password=%s,image=%s WHERE ssn="+ssn
            val = (ssn,name,birthdate,address,salary,biography,phone,gender,username,email,password,image.read())
            mycursor.execute(sql,val)
            mydb.commit()


    return redirect(url_for('adminBp.viewNurses'))

@nurseBp.route('/delete/<ssn>' ,methods=['GET'])
def deleteNurse(ssn):
    #TODO
    sql = "DELETE FROM Nurse WHERE ssn="+ssn
    # val = (int(operation_id))
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('adminBp.viewNurses'))

