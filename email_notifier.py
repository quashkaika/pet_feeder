import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

mail_to = '...'
gmail_user = '...'
gmail_password = '...'

class Emailer():

    def send_email_with_images(self, image_file_names):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'Pictures from Futtermaschine'
            text = MIMEText("test")
            msg.attach(text)
            for image_file_name in image_file_names:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(image_file_name, "rb").read())
                encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=image_file_name)
                msg.attach(part)

            server = smtplib.SMTP_SSL('...', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, mail_to, msg.as_string())
            server.close()

        except Exception as e:
            print('Error when sending email:%s' % str(e))
            print(str(e))

