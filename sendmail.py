#send email with Google mail
#if send mail without attach use only email_body and email_subject params
#if send mail with attach use all params



# trace errors from Exceptions
import traceback

# send mail
import sys
import datetime
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



# Sending email
def send_mail(email_body, email_subject, path=None, file=None):

    #initialize server variabile
    server = None

    # email login
    email_user = ''
    email_passwd = ''

    # email to/from
    email_from = "cristian.gard28@gmail.com"
    email_to = "gard.cristian@gmail.com"

    # send mail without attachment
    if path is None and file is None:
        msg = EmailMessage()
        msg['Subject'] = email_subject
        msg['From'] = email_from
        msg['To'] = email_to
        msg.set_content(email_body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email_user, email_passwd)
            server.send_message(msg)

        # if exception quit
        except Exception:
            print(traceback.format_exc())
            sys.exit()

        # quit email server if was open
        finally:
            if server is not None:
                server.quit()

    # send mail with attachement
    else:
        # instance of MIMEMultipart
        msg = MIMEMultipart()
        msg['Subject'] = email_subject
        msg['From'] = email_from
        msg['To'] = email_to
        body = email_body

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # send mail
        try:
            # attach file
            filepath = str(path + file)
            attachment = open(filepath, "rb")

            # instance of MIMEBase and named as p
            payload = MIMEBase('application', 'octet-stream', Name=filepath)

            # To change the payload into encoded form
            payload.set_payload(attachment.read())

            # encode into base64
            encoders.encode_base64(payload)

            # add header
            payload.add_header('Content-Disposition', 'attachment', filename=file)

            # attach the instance 'payload' to instance 'msg'
            msg.attach(payload)

            # initialize server wiht port 465(for attachemnt)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

            # start TLS for security
            # server.starttls()

            # Authentication
            server.login(email_user, email_passwd)
            # Converts the Multipart msg into a string
            txt = msg.as_string()
            server.sendmail(email_from, email_to, txt)

        #if exception quit
        except Exception:
            print(traceback.format_exc())
            sys.exit()

        # quit email server if was open
        finally:
            if server is not None:
                server.quit()

