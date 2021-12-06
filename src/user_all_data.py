#printfrom flask import jsonify,Flask
from .fun_file import *
import json
from datetime import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from inspect import currentframe, getframeinfo


from flask import current_app as app


#Get Enquiry ID



def get_current_user_data(user_login):
    try:

        for i in user_login:
            user_login_data = i
            #print("user_login_data---------------------------21",user_login_data)
            break

        del user_login_data['public_id']
        del user_login_data['user_password']
        del user_login_data['email_var_code']
        

        return user_login_data

    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + ' line: ' + str(frameinfo.lineno)
        return {'Message': 'something wrong with user_all_data->get_current_user_data' + file_line,
                        'error_message': str(e),
                        'Status': 0
                        }
