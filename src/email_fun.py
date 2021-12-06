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

import src.mailjet_fun as mj_mail

project_url = "http://167.71.239.223/"
api_url = "http://167.71.239.223:8123/api/v1/"

# Get Enquiry ID
supportemail = "pmpmaharana97@gmail.com" 
plandetails_link_rec = project_url+'uat/pricing.html'
canprofile_link =  project_url+'uat/candidate/cndprofile.html'

portalname="patner.aaonxt.com"
login_link = "http://aaonxt.patner.com/patner/login.html"


def send_email(req_data):
    try:
        get_message = req_data['message']
        receiver_email = req_data['reciver_mail']
        receiver_email = str(receiver_email)

        sender_email = "f7f82ccc94ba027d75f28a7c6148221d"
        password = "f50458390a18e846177efdf31fb97b8a"
        receiver_email = receiver_email.strip()

        message = MIMEMultipart("alternative")
        message["Subject"] = "SECM JOB API"
        message["From"] = sender_email.strip()
        message["To"] = receiver_email.strip()

        # Create the plain-text and HTML version of your message
        text = """hello """ + str(get_message)

        html = """\
        <html>
        <body>
            <p>Hi,<br>
            <br>
            <a href="https://maadhab.bitbucket.io/">scmjobportal n</a>
            """ + str(get_message) + """
            </p>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()


        # use 465 or 587 or 25
        with smtplib.SMTP_SSL("in-v3.mailjet.com", 465, context=context) as server:
            server.login(sender_email, password)
            send_mail = server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        send_mail = str(send_mail)

        return {'Message': 'email successfully sent',
                'Status': 1,
                'send_mail': send_mail

                }
    except Exception as e:
        return {'Message': 'email sending failed',
                'error_message': str(e),
                'Status': 0
                }


def registration_verificationcode(message_data, reciver_email, username,verification_code):
    verification_code = str(verification_code)
    name = str(username)

    text_part = "verification link"
   
    subject = "You’re almost ready!"

    html_part = '''   Hi '''+name+''',<br><br>
                    We just need to verify your email address before you can start using '''+portalname+'''. <br>
                    We hope you find what you are looking for, here! To start with, please verify your account. <br>

                    <a href="'''+api_url+'''email_verify/?email_id='''+reciver_email+'''&EMAIL_VER_CODE='''+verification_code+'''&opstype=patner_mail_verify">click here to verify.</a><br><br>
                        <br>
                        <br>
                        <br>
                     <br>
                    Team '''+portalname+''' <br>
                    <img src="'''+project_url+'''/uat/images/logo.jpg" alt="logo_img" width="200" height="50"> <br>'''

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "scsmportal@gmail.com",
                    "Name": "scmjob"
                },
                "To": [
                    {
                        "Email": reciver_email,
                        "Name": str(name)
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('registration_verificationcode', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def Welcome_thanks_for_creating_a_profile(reciver_email, username):

    name = str(username)

    text_part = "Welcome and thanks for creating a profile"
    subject = "Welcome on board!"
    html_part = '''<p>Hi '''+name+''',</P><br>
                <p> Welcome to '''+portalname+''' ! What next? <br>
                    Click here to log into your account and start exploring: <a href="'''+login_link+'''">link</a> <br>

                    It’s a pleasure to have you on board, have a great day!<br>
                    </p>
                    <br>
                    <br>
                    <p>

                    Cheers,<br>
                    '''+portalname+'''
                    </p>
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
                        "Email": reciver_email,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def Reset_Password_link(username, emailid, url_link, usertype):
    '''
                        templates =

                            Hi <name>,
                If you have lost your password or wish to reset it, please click on the following link: [link] and follow the instructions.

                If you did not make this request, please ignore this mail.

                Sincerely,
                The <portal> Team

candidate:
    Subject: Password reset link

Body:
Trouble signing in?
Just click the link: [link] and follow the instructions to reset your password.

If you did not make this request, please ignore this mail.

Cheers,
<Name/portal name>

    '''

    portalname = 'SCMJOBPORTAL'
    link = "https://scmjobportal.com/recruiterlogin"
    name = str(username)

    text_part = "Reset Password"

    if usertype == 'RECRUITER':
        subject = '''Reset your '''+portalname+''' password'''
        html_part = '''<p>Hi '''+name+''',</P>
                            <br>
                    <p>   If you have lost your password or wish to reset it, <br>
                    please click on the following link: <a href="'''+url_link + '''">Password Reset</a> and follow the instructions.

                    If you did not make this request, please ignore this mail.
                        </p>
                        <br>
                        <br>
                        <p>

                        Sincerely,<br>
                        The '''+portalname+''' Team
                        </p>

                '''
    else:
        subject = '''Password reset link'''

        html_part = '''<p>Hi '''+name+''',</P>
                            <br>
                    <p>  Trouble signing in? <br>
                    please click on the following link: <a href="'''+url_link + '''">Password Reset</a> and follow the instructions to reset your password.<br>

                    If you did not make this request, please ignore this mail.
                        </p>
                        <br>
                        <br>
                        <p>

                        Cheers,<br>
                        The '''+portalname+''' Team
                        </p>

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
                        "Email": emailid,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('Reset_Password_link', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus



def Reset_Password_success(username, emailid, url_link, usertype):
    '''
                        templates =

                            Hi <name>,
                If you have lost your password or wish to reset it, please click on the following link: [link] and follow the instructions.

                If you did not make this request, please ignore this mail.

                Sincerely,
                The <portal> Team

candidate:
    Subject: Password reset link

Body:
Trouble signing in?
Just click the link: [link] and follow the instructions to reset your password.

If you did not make this request, please ignore this mail.

Cheers,
<Name/portal name>

    '''

    portalname = 'SCMJOBPORTAL'
    link = "https://scmjobportal.com/"
    name = str(username)

    text_part = "Reset Password"

    if usertype == 'RECRUITER':
        subject = '''Reset your '''+portalname+''' password successfully'''
        html_part = '''<p>Hi '''+name+''',</P>
                            <br>
                    <p>   Yor password successfully updated <br>
                    please click on the following link: <a href="'''+url_link + '''">Login Here</a> to login.


                        </p>
                        <br>
                        <br>
                        <p>

                        Sincerely,<br>
                        The '''+portalname+''' Team
                        </p>

                '''
    else:
        subject = '''Password reset successfully'''

        html_part = '''<p>Hi '''+name+''',</P>
                            <br>
                    <p>   Yor password successfully updated <br>
                    please click on the following link: <a href="'''+url_link + '''"> Login Here</a> to login.


                        </p>
                        <br>
                        <br>
                        <p>

                        Sincerely,<br>
                        The '''+portalname+''' Team
                        </p>

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
                        "Email": emailid,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('Reset_Password_link', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def candidate_profile_complete(username, email_id):
    '''
                        templates =
                Subject: Congratulations! Your profile is now complete

                Body:
                Hello <name>,
                You have successfully updated your profile and it is now available for recruiters to check out! Check out jobs suitable for your profile <link>

                Cheers,
                <Name/Portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = '''Congratulations! '''+username + '''Your profile is now complete'''

    subject = '''Congratulations! '''+username + '''Your profile is now complete'''
    html_part = '''Hello '''+username + ''',<br>
                You have successfully updated your profile and it is now available for recruiters to check out! <br>
                Check out jobs suitable for your profile.<br>
                <br>
                <br>

                Cheers,<br>
                '''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('registration_verificationcode', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def candidate_profile_not_complete(username, email_id):
    '''
                        templates =
                
                            Subject: Complete your profile & help us help you better
                            Body:
                            Hi <name>,
                            Update your profile now and improve your job search experience. Recruiters look for up-to-date and
                            active profiles when looking for prospective candidates. Please ensure your profile is updated for
                            recruiters to contact you.
                            Contact us on <portal customer email> for any queries or assistance.
                            Regards,
                            Team <portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = '''Complete your profile & help us help you better'''

    subject = '''Complete your profile & help us help you better'''
    html_part = '''Hi '''+username + ''',<br>
                Update your profile now and improve your job search experience. Recruiters look for up-to-date and <br>
                active profiles when looking for prospective candidates. Please ensure your profile is updated for <br>
                recruiters to contact you. <br>
                Contact us on '''+supportemail+''' for any queries or assistance.
                <br>
                <br>

                Regards,<br>
                Team'''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('candidate_profile_not_complete', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def recruiter_profile_complete(username, email_id):
    # recruiter_profile_complete(COMPANY_NAME,old_email)
    '''
                        templates =
                Subject: Congratulations! Your profile is now complete

                Body:
                Hello <name>,
                You have successfully updated your profile and it is now available for recruiters to check out! Check out jobs suitable for your profile <link>

                Cheers,
                <Name/Portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = '''Congratulations! '''+username + '''Your profile is now complete'''

    subject = '''Congratulations! '''+username + '''Your profile is now complete'''
    html_part = '''Hello '''+username + ''',<br>
                You have successfully updated your profile and it is now available for candidates to check out! <br>
                Check out candidates suitable for your profile.<br>
                <br>
                <br>

                Cheers,<br>
                 '''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('registration_verificationcode', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def recruiter_profile_not_complete(username, email_id):
    # recruiter_profile_complete(COMPANY_NAME,old_email)
    '''
                        templates =
               Subject: Update your profile
                Body:
                Hey <name>,
                We noticed that some of the information on your profile is missing. Kindly log in to the
                <portal> and head towards the profile section to update your personal details.
                Regards,
                <Name/Portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = ''' Update your profile'''

    subject = '''Congratulations! '''+username + '''Your profile is now complete'''
    html_part = '''Hey '''+username + ''',<br>
                We noticed that some of the information on your profile is missing. Kindly log in to the <br>
                '''+portalname+''' and head towards the profile section to update your personal details.<br>
                <br>
                <br>

                Regards,<br>
                 '''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('recruiter_profile_not_complete', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def recruter_membership_plan_upgraded(username, email_id,plan_name):
    # recruiter_profile_complete(COMPANY_NAME,old_email)
    '''
                        templates =
                                    Membership Upgraded
                        Subject: Congratulations! Your membership is now upgraded.
                        Body:
                        Hi <name>,
                        Your membership with <portal name> has been upgraded. Thank you for believing in us.
                        Here are the benefits of being a premium member -
                        <benefits of the membership>
                        If you wish to cancel membership, click here <link>
                        Kind regards,
                        <portal name> Team


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = ''' Congratulations! Your membership is now upgraded '''

    subject = '''Congratulations! Your membership is now upgraded'''
    html_part = '''Hi '''+username + ''',<br>
                Your membership with '''+portalname+''' has been upgraded. Thank you for believing in us. <br>
                your plan is upgraded to '''+plan_name+''' -<br>
                click here to see plan details <a href="'''+plandetails_link_rec+'''">link</a>
                <br>
                <br>

                Kind regards,<br>
                 '''+portalname+''' Team <br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('recruter_membership_plan_upgraded', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def jobseeker_membership_plan_upgraded(username, email_id,plan_name):
    '''
                        templates =
                                            Membership Upgrade - Job seeker/freelancer
                        Subject: Membership Upgraded Notification
                        Body:
                        Hi <name>,
                        <name of the job seeker> has successfully upgraded the <Membership name>
                        membership on <portal name>. To view <name of the job seeker>’s profile, click here link .
                        Sincerely,
                        <portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = ''' Membership Upgraded Notification '''

    subject = '''Congratulations! Your membership is now upgraded'''
    html_part = '''Hi '''+username + ''',<br>
                '''+username + ''' has successfully upgraded the '''+plan_name+''' <br>
                your plan is upgraded to '''+plan_name+''' -<br>
                membership on '''+portalname+'''. To view '''+ username + '''’s profile, click here <a href="'''+canprofile_link+'''">link</a>.<br>
                <br>
                <br>

                Sincerely,,<br>
                 '''+portalname+''' <br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    #write_to_file('jobseeker_membership_plan_upgraded', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus

def contactus_recive_query(username, email_id):
    '''
                        templates =
                Subject: Got queries? We are here to answer all of them!

                Body:
                 Hello username,<br>
                    we have got your query our team will soon contact you regarding this as soon as possible.
                Cheers,
                <Name/Portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = '''Got queries? We are here to answer all of them!'''

    subject = '''Got queries? We are here to answer all of them!'''
    html_part = '''Hello ,'''+username + ''',<br>
                we have got your query our team will soon contact you regarding this as soon as possible. <br>

                <br>
                <br>
                <br>

                Sincerely,<br>
                '''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }


    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def candidate_shortlistede_mail(username, email_id, job_title):
    # candidate_shortlistede_mail(user_name,candidate_email_id,job_title)
    '''
                        templates =

                Subject: You have been shortlisted!

            Body:
            Hey <name>,
            We are excited to let you know that your CV has been shortlisted for the <job profile> profile.<br>
            To take this further, please inform us of your availability for the interview. <br>
            Looking forward to hearing from you! <br>


            Cheers,
            <Portal name>


    '''

    portalname = 'SCMJOBPORTAL'
    reciver_email = email_id
    text_part = '''You have been shortlisted!'''

    subject = '''You have been shortlisted!'''
    html_part = '''Hey '''+username+''',<br>
            We are excited to let you know that your CV has been shortlisted for the '''+job_title+''' profile.<br>
            To take this further, please inform us of your availability for the interview. <br>
            Looking forward to hearing from you! <br><br>
                <br>
                <br>

                 Cheers,<br>
                '''+portalname+'''<br>

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('registration_verificationcode', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def email_last30_can_rec_registered(rec_total, can_total, textmonth):
    '''
                        templates =

                    Subject: Registration Update

        Body:
        Hello <name>,
        We wanted to inform you that this month <number> candidates and <number> recruiters have registered on <portal name>.

        Kind regards,
        <Portal> Team     '''

    username = 'admin'

    portalname = 'SCMJOBPORTAL'
    reciver_email = 'sunil.sahoo@krititech.in'  # 'rasika@agency09.in'
    text_part = '''Registration Update'''

    subject = '''Registration Update.'''
    html_part = '''Hello '''+username+''',<br>
            We wanted to inform you that this month('''+textmonth+''') <br>
            '''+str(can_total)+''' candidates and <br>
           '''+str(rec_total)+''' recruiters have registered on '''+portalname+'''. <br>
                <br>
                <br>
                 Kind regards,<br>
                 '''+portalname+''' Team

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
                        "Email": reciver_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('email_last30_can_rec_registered', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus


def send_mail_notification_toadmin_for_registration(usertype, username, reciver_email, ID):

    username_admin = 'admin'

    portalname = 'SCMJOBPORTAL'
    # 'rasika@agency09.in' sunil.sahoo@krititech.in
    admin_email = 'sunil.sahoo@krititech.in'
    if usertype == 'CANDIDATE':
        url_link = '''http://165.232.181.242/supplychain/uat/adminapp/cndview.html?id=''' + \
            str(ID)

        text_part = '''New Job Seeker Alert'''

        subject = '''New Job Seeker Alert'''
        html_part = '''Hello '''+username_admin+''',<br>
                '''+username+'''  has created a profile on '''+portalname+'''.<br>
                email:'''+reciver_email+'''<br>
                To see the complete profile, please click <a href="'''+url_link + '''">here</a>.<br>

                Sincerely,<br>
                '''+portalname+'''<br>

                '''
    else:
        url_link = '''http://165.232.181.242/supplychain/uat/adminapp/recview.html?id=''' + \
            str(ID)
        text_part = '''New Recruiter Alert'''

        subject = '''New Recruiter Alert'''
        html_part = '''
                Hello '''+username_admin+''',<br>
               '''+username+''' email:'''+reciver_email+''' has created a profile on '''+portalname+'''.<br>
               <br>
                Please click <a href="'''+url_link + '''">here</a> to check their complete profile.<br>

                Sincerely,<br>
                '''+portalname+'''<br>

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
                        "Email": admin_email,
                        "Name": username_admin
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    write_to_file('send_mail_notification_toadmin_for_registration', str(data))

    emailstatus = mj_mail.send_email_generic(data)
    return emailstatus
