from flask import Flask,Blueprint, redirect, url_for, request,render_template
# mycursor = mydb.cursor()
import mysql.connector
mydb = mysql.connector.connect(
    host='34.71.50.183',
    user="root",
    port=3306,
    passwd="alykhaled123",
    database="operationsDB"
)
mydb.autocommit = True

equipmentBp = Blueprint('equipmentBp', __name__, template_folder='templates',static_folder='static')
mycursor = mydb.cursor()

@equipmentBp.route('/add' ,methods=['POST'])
def addEquipment():
    '''
    This is add POST request for the equipment
    that add a new equipment to the database
    '''
    if request.method == 'POST':
        Equipment_Name = request.form['Equipment_Name']
        Eq_room = request.form['Eq_Room']
        EquipmentModel = request.form['Equipment_Model']
        Eq_Admission_date = request.form['Eq_Admission_date']
        sql = "INSERT INTO `operationsDB`.`Equipment` (`Equipment_Name`, `Eq_Room`, `Equipment_Model`, `Eq_Admission_date`) VALUES (%s,%s,%s,%s);"
        val = (Equipment_Name,Eq_room,EquipmentModel,Eq_Admission_date)
        mycursor.execute(sql,val)
        mydb.commit()

    return render_template("adminAddEquipment.html")

@equipmentBp.route('/update/<id>' ,methods=['POST','GET'])
def updateEquipment(id):
    '''
    This is update PUT request for the doctor
    that update a doctor in the database
    '''
    if request.method == 'POST':
        Equipment_Name = request.form['Equipment_Name']
        Eq_room = request.form['Eq_Room']
        EquipmentModel = request.form['Equipment_Model']
        Eq_Admission_date = request.form['Eq_Admission_date']
        sql = "UPDATE `operationsDB`.`Equipment` SET Equipment_Name=%s,Eq_Room=%s,Equipment_Model=%s,Eq_Admission_date=%s WHERE Equipment_ID="+id
        val = (Equipment_Name,Eq_room,EquipmentModel,Eq_Admission_date)
        mycursor.execute(sql,val)
        mydb.commit()
    return redirect(url_for('adminBp.viewEquipment'))

@equipmentBp.route('/delete/<Equipment_ID>' ,methods=['GET'])
def deleteEquipment(Equipment_ID):
    sql = "DELETE FROM Equipment WHERE Equipment_ID="+Equipment_ID
    # val = (int(operation_id))
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('adminBp.viewEquipment'))
