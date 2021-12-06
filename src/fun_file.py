import math
import random

import mysql.connector

import base64
import uuid
import requests
import urllib
import hashlib
import re
import datetime
from .config import Configdb


def mycus():
    '''
    this data is from config file where all credential for mysql connection is their
    '''
    db = Configdb()
    mydb = mysql.connector.connect(
        host=db.HOST, user=db.USER, passwd=db.PASSWORD, database=db.DATABASE)
    return mydb


def generateOTP():
    #digits = "0123456789"
    OTP = "1234"
    # for i in range(4) :
    #	OTP += digits[math.floor(random.random() * 10)]
    return str(OTP)


def write_to_file(classname="na", textOP="demo"):
    try:
        Text = str(textOP)
        Classname = str(classname)
        CurrentTimedata = datetime.datetime.now()
        CurrentTime = CurrentTimedata.strftime("%d/%m/%Y, %H:%M:%S")
        with open("/log/line_output.txt", "a") as myfile:
            myfile.write("\n")
            myfile.write("\n")
            myfile.write("Classname:"+Classname+"--data--" +
                         Text+".Time:"+CurrentTime+".")
            return True
    except Exception as e:
        return str(e)


def RegisterCustomer(totalval):
    totalval += 1
    Result = 'SCAA' + str(totalval)
    return str(Result)


def RequestCustomer(totalval):
    totalval += 1

    Result = 'SENR0' + str(totalval)
    return str(Result)


def AreaManager(totalval):
    totalval += 1
    Result = 'SEAM0' + str(totalval)
    return str(Result)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Upload_fun(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename


def save(Photo):
    imgdata = base64.b64decode(Photo)
    # I assume you have a way of picking unique filenames
    filename = 'static/video/'+str(uuid.uuid4())+'.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
        return (filename.replace('static/video/', ''))


def EmpIdSM(totalval):
    totalval += 1
    Result = 'SESM0' + str(totalval)
    return str(Result)


def EmpIdAU(totalval):
    totalval += 1
    Result = 'SEAU0' + str(totalval)
    return str(Result)


def ClaimNo(totalval):
    totalval += 1
    Result = 'SECL0' + str(totalval)
    return str(Result)


def SMS_Integration(msg, contactno):
    uname = 'krititech'
    pwd = 'kriti@2705'
    senderid = 'SCREXP'

    msg = urllib.parse.quote(msg)

    smsurl = 'http://cloud.smsindiahub.in/vendorsms/pushsms.aspx?user='+str(uname)+'&password='+str(
        pwd)+'&msisdn='+str(contactno)+'&sid='+str(senderid)+'&msg='+str(msg)+'&fl=0&gwid=2'
    r = requests.post(url=smsurl)
    x = r.json()


def Password_encoded(MobileNo):
    result = hashlib.sha256(MobileNo.encode())
    result = (result.hexdigest())
    return result

# --------------------------------validation--------------------------------------------------


def request_form(Name, MobileNo, VehicleCategory, DateOfPurchase, PoliceStation, District, State):
    if Name != "" and MobileNo != "" and VehicleCategory != "" and DateOfPurchase != "" and PoliceStation != "" and District != "" and State != "":
        return True


def validNumber(phone_number):
    regex = "^[0-9]{10}$"
    if (re.search(regex, phone_number)):
        return True


def check(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)):
        return True


def accountNo(accountno):
    if len(accountno) >= 14 and len(accountno) <= 16:
        return True


def vehicleNo(vehicleno):
    if len(vehicleno) >= 8 and len(vehicleno) <= 10:
        return True


def adharNo(adharNo):
    regex = "^\d{4}\s\d{4}\s\d{4}$"
    if (re.search(regex, adharNo)):
        return True


def GSTINo(GSTINo):
    if len(GSTINo) == 15:
        return True


def ChassisNo(ChassisNo):
    if len(ChassisNo) == 17:
        return True


def pancard(Pancard):
    if re.match("[A-Za-z]{5}\d{4}[A-Za-z]{1}", Pancard):

        return True


def pincode(Pincode):
    regex = "^\d{6}(,\d{6})*$"
    if (re.search(regex, Pincode)):
        return True


def fun_ifsc(IFSC):
    if re.match("^[A-Z]{4}\d{7}$", IFSC):
        return True


def notification_all(desc, msg, user_token):
    url = 'https://onesignal.com/api/v1/notifications'
    headers = {'Authorization': 'Basic NjdhNzY5MWYtODZkNS00NTI4LTg5NzQtMGVmM2ZiMTQ1Njkz',
               'Content-Type': 'application/json'}

    params = {
        "app_id": "f8937086-f40e-438d-a2df-47358da0d780",
        "headings": {"en": desc},
        "contents": {"en": msg},
        "include_player_ids": [user_token]
    }
    a = json.dumps(params)
    r = requests.post(url, a, headers=headers)
