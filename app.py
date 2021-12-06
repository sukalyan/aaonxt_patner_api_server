import json
from flask import Flask, url_for, redirect, flash, session, jsonify, request, render_template, make_response, abort,send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse, request
import jwt
from functools import wraps

import datetime

from src.fun_file import *
import src.patner as patnr

import src.user_all_data as usrd

from inspect import currentframe, getframeinfo

# from src.employee_signup import employee_signup,employee_signup_password

UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
app = Flask(__name__)

cors = CORS(app)
CORS(app, support_credentials=True)

api = Api(app, prefix="/api", catch_all_404s=True)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'application/json'
app.config["DEBUG"] = True

app.config["APPLICATION_ROOT"] = "/patneraaonxt/api/v1"

AROOT="/api/v1/"
#patner/register

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing', 'status': 0})
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            # print(data)
            mydb = mycus()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(
                "SELECT * from patner_login_details WHERE public_id = '%s' and is_loged_in = 1" % (data['public_id']))
            user_login = mycursor.fetchall()
            mycursor.close()
            mydb.close()
            if len(user_login) > 0:
                pass
            else:

                return jsonify({'Message': 'Alreday logout, please login again',
                                'Status': 0
                                })
        except Exception as e:
            frameinfo = getframeinfo(currentframe())
            file_line = ' path: ' + \
                        str(frameinfo.filename) + \
                ' line: ' + str(frameinfo.lineno)
            return jsonify({'Message': 'token is invalid or expired',
                            'Status': 0,
                            'error': str(e),
                            'error_line': file_line
                            })

        current_user = usrd.get_current_user_data(user_login)
        return f(current_user, *args, **kwargs)

    return decorated


@app.route(AROOT+'patner/viewprofile', methods=['POST'])
@token_required
def user_details(current_user):
    try:

        return jsonify({'Message': 'succesfully login and fetched data.',
                        'userdetails': current_user,
                        'Status': 1
                        })

    except Exception as e:
        return jsonify({'Message': 'something went wrong code 151',
                        'Status': 0,
                        'error': str(e)
                        })



@app.route(AROOT+'patner/register', methods=['POST'])
def candidate_register():
    try:
        req_data = request.get_json()
        # write_to_file('candidate_register', str(req_data))
        if req_data['opstype'] == 'patner_register':
            rs = patnr.patner_register(req_data)
            return jsonify(rs)
        else:
            frameinfo = getframeinfo(currentframe())
            file_line = ' path: ' + str(frameinfo.filename) + ' line: ' + str(frameinfo.lineno)
            return jsonify({'Message': 'check operation type' + file_line,
                            'Status': 0,
                            'error': 'wrong operation type'
                            })

    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + ' line: ' + str(frameinfo.lineno)
        return jsonify({'Message': 'something wrong with data insert  code 319' + file_line,
                        'error_message': str(e),

                        'Status': 0
                        })


@app.route(AROOT+'email_verify/', methods=['POST', 'GET'])
def email_verificationlink():
    try:
        email_ver_code = request.args.get('EMAIL_VER_CODE')
        email_id = request.args.get('email_id')
        opstype = request.args.get('opstype')
        req_data = {'opstype': opstype, 'email_id': email_id,
                    'EMAIL_VER_CODE': email_ver_code}

        if req_data['opstype'] == 'patner_mail_verify':
            rs = patnr.patner_mail_verify(req_data)
            if rs['Status'] == 1:
                print(1)
                return redirect("http://167.71.239.223/patner/login.html", code=302)

            else:
                print(2)
                # print('mail verifi status 0')
                return redirect("http://167.71.239.223/patner/verification_fail.html", code=302)

        else:
            print(3)
            # print('mail verifi wrong opstype')
            return redirect("http://167.71.239.223/error_page.html", code=302)

    except Exception as e:
        print(4)
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + \
                    ' line: ' + str(frameinfo.lineno)
        return jsonify({'Message': 'something wrong with data insert  code 384' + file_line,
                        'error_message': str(e),
                        'Status': 0
                        })



@app.route(AROOT+'login',methods=['POST'])
def login():
    try:
        auth = request.authorization
        print(auth.username)
        print(auth.password)

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'basic realm = "Login required!"'})

        mydb = mycus()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * from patner_login_details WHERE email_id = '%s' AND is_active = 1 " % auth.username)
        user = mycursor.fetchall()
        mycursor.close()
        mydb.close()

        if len(user) > 0:
            userdata={}
            for i in user:
                USER_PASSWORD = i['user_password']
                IS_EMAIL_VERIFIED = i['is_email_verified']
                # USER_ID = i['USER_ID']
                PUBLIC_ID = i['public_id']
                login_row_data = i
                break
        else:
            # return make_response('Could not verify', 401, {'WWW-Authenticate': 'basic realm = "Login required!"'})
            return jsonify({'Message': 'username not exist please signup',
                            'Status': 0
                            })
        if IS_EMAIL_VERIFIED == 'N':
            # please dont change the string
            return jsonify({'Message': 'Please verify your account. Verification mail sent on your registered Email id',
                            'Status': 2
                            })

        if check_password_hash(USER_PASSWORD, auth.password):
            db = Configdb()

            token = jwt.encode({'public_id': PUBLIC_ID, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=db.WEBTOKEN_EXPIRE)}, app.config['SECRET_KEY'])
            # print(token)
            # print(type(token))

            userdata["email_id"] = login_row_data['email_id']
            userdata["name"] = login_row_data['first_name'] +" " + login_row_data['last_name']
            userdata["org_name"] = login_row_data['org_name']

            mydb = mycus()
            mycursor = mydb.cursor()
            sql = "UPDATE patner_login_details SET is_loged_in =%s WHERE id =%s "
            logintable_id = login_row_data['id']
            val = (str(1), str(logintable_id))
            result = mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()

            return jsonify({'Token': token, 'Details': userdata,'Status': 1})
        else:
            return jsonify({'Message': 'Wrong Email Id or password.',
                            'Status': 0
                            })

    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + \
                    ' line: ' + str(frameinfo.lineno)
        return jsonify({'Message': 'something wrong with login please check code 2032' + file_line,
                        'error_message': str(e),
                        'Status': 0
                        })



@app.route(AROOT+"logout", methods=['POST'])
@token_required
def logout(current_user):
    try:
        print(current_user)

        userid = current_user['id']
        mydb = mycus()
        mycursor = mydb.cursor()
        sql = "UPDATE patner_login_details SET is_loged_in =%s WHERE id =%s "

        val = (str(0), str(userid))
        result = mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        return jsonify({'Message': 'logout successfull',
                        'Status': 1
                        })

    except Exception as e:
        frameinfo = getframeinfo(currentframe())
        file_line = ' path: ' + str(frameinfo.filename) + \
                    ' line: ' + str(frameinfo.lineno)
        return jsonify({'Message': 'something wrong with input please check code 1918' + file_line,
                        'error_message': str(e),
                        'Status': 0
                        })


if __name__ == '__main__':
    app.run(port='8123', host='0.0.0.0', debug=True)
