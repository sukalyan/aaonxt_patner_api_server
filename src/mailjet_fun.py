from mailjet_rest import Client
import os

from flask import jsonify, Flask
from .fun_file import *
import json
from datetime import datetime
import time
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from flask import current_app as app


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Get Enquiry ID


def send_email_mj(req_data):
    try:

        get_message = req_data['message']
        receiver_email = req_data['reciver_mail']

        api_key = 'f7f82ccc94ba027d75f28a7c6148221d'
        api_secret = 'f50458390a18e846177efdf31fb97b8a'

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "scsmportal@gmail.com",
                        "Name": "scmjob"
                    },
                    "To": [
                        {
                            "Email": receiver_email,
                            "Name": "user"
                        }
                    ],
                    "Subject": "message from scm job ",
                    "TextPart": str(get_message),
                    "HTMLPart": "<h3> "+str(get_message)+"</h3>",
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        #print(result.status_code)
        #print(result.json())

        return {'Message': 'email successfully sent',
                'Status': 1,

                }

    except Exception as e:
        return {'Message': 'email sending fail',
                'error_message': str(e),

                'Status': 0
                }


def send_email_generic(data):
    try:

        #get_message = req_data['message']
        #receiver_email = req_data['reciver_mail']

        api_key = 'f7f82ccc94ba027d75f28a7c6148221d'
        api_secret = 'f50458390a18e846177efdf31fb97b8a'

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        '''
        data = {
        'Messages': [
            {
            "From": {
                "Email": "scsmportal@gmail.com",
                "Name": "scmjob"
            },
            "To": [
                {
                "Email": receiver_email,
                "Name": "user"
                }
            ],
            "Subject": "message from scm job ",
            "TextPart": str(get_message),
            "HTMLPart": "<h3>Dear user welcome <a href='https://maadhab.bitbucket.io/'>scmjobportal</a>!</h3><br />"+ str(get_message) +"",
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }

        '''
        result = mailjet.send.create(data=data)
        #print(result.status_code)
        #print(result.json())

        return {'Message': 'email successfully sent',
                'Status': 1,

                }

    except Exception as e:
        return {'Message': 'email sending fail',
                'error_message': str(e),

                'Status': 0
                }
