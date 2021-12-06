from flask import jsonify, Flask
from .fun_file import *
import json
from datetime import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import src.email_fun as emailf
from random import randint
from inspect import currentframe, getframeinfo


from flask import current_app as app
from .config import Configdb


 

def patner_register(req_data):
    try:

        db = Configdb()

        first_name = req_data.get('first_name',None)
        last_name = req_data.get('last_name',None)
        org_name = req_data.get('org_name',None)

        #phone_no = req_data.get('phone_no',None)

        EMAIL_ID = req_data.get('email_id',None)

        USER_PASSWORD = req_data.get('user_password',db.DEFAULT_PASSWORD)
        # print("hello")



        mydb = mycus()
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * from patner_login_details WHERE email_id = '%s'" % (EMAIL_ID))
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(row) > 0:
            # mobile number  already exist
            return {'Message': 'Email already exist use another one.',
                    'Status': 0
                    }

        # validate email id

        if check(EMAIL_ID):
            pass
        else:
            return {'Message': 'Invalid EMAIL please provide a valid email.',
                    'Status': 0
                    }

        PASSWORD = generate_password_hash(USER_PASSWORD, method='sha256')
        public_id = str(uuid.uuid4())
        VARIFICATION_CODE = randint(100000, 999999)

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")

        mydb = mycus()
        mycursor = mydb.cursor()
        sql = "INSERT INTO patner_login_details (email_id,first_name,last_name,org_name,user_password,created_on,email_var_code,public_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (EMAIL_ID,first_name,last_name,org_name,PASSWORD,dt_string,VARIFICATION_CODE,public_id)

        result = mycursor.execute(sql, val)
        login_details_id = mycursor.lastrowid
        # print("login_details_id",login_details_id)
        mydb.commit()
        mycursor.close()
        mydb.close()

        message_data = "messagedata"
        username = first_name+" "+last_name
        # registration_verificationcode(message_data,reciver_email,username,portalname,verification_code):
        email_status = emailf.registration_verificationcode(
            message_data, EMAIL_ID, username,VARIFICATION_CODE)
        # print(email_status)

        return {'Message': 'patner signup successfull',
                'login_details_id': login_details_id,
                'email_status': email_status,
                'Status': 1
                }
    

    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + ' line: ' + str(frameinfo.lineno)
        return {'Message': 'something wrong with data insert  code 319' + file_line,
                        'error_message': str(e),

                        'Status': 0
                        }


def patner_mail_verify(req_data):
    try:
        email_id = req_data['email_id']
        EMAIL_VER_CODE = req_data['EMAIL_VER_CODE']

        mydb = mycus()
        mycursor = mydb.cursor(dictionary=True)
        sql= '''SELECT * FROM patner_login_details  WHERE email_id =%s and email_var_code = %s '''
        val=(email_id,EMAIL_VER_CODE)
        mycursor.execute(sql,val)
        row = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(row) > 0:
            for each_row in row:
                logindata = each_row
                break

            emailid = logindata["email_id"]
            USER_LOGIN_ID= logindata["id"]

            username = logindata["first_name"]+" "+logindata["last_name"]

            emailstatus = emailf.Welcome_thanks_for_creating_a_profile(emailid, username)

            mydb = mycus()
            mycursor = mydb.cursor()
            sql = "UPDATE patner_login_details SET is_email_verified='Y',email_var_code=1849637 WHERE id =" + str(USER_LOGIN_ID)+" "
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            mydb.close()    
            
            return {'Message': 'SUCCESSFULLY VERIFIED MAIL, PLEASES LOGIN',
                    'Status': 1,
                    'emailstatus': emailstatus,
                    }
        else:
            # emailid already exist
            return {'Message': 'VERIFICATION CODE IS WRONG or expired OR EMAIL IS WRONG',
                    'Status': 0,
                    'result': 0
                    }
    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + \
                    ' line: ' + str(frameinfo.lineno)
        return {'Message': 'something went wrong' + file_line,
                'Status': 0,
                'error': str(e)
                }
