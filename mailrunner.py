import smtplib
import time
import imaplib
import email
import datetime
import subprocess

SENDER = 'First Last <username@example.com>'

SERVICE = 'someapp'

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "username" + ORG_EMAIL
FROM_PWD = "password"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

def read_email():
    """
    read_email()

    :return:

    Read email from inbox and parse for the expected commands to start/kill the service
    """
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        mtype, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = []

        if mail_ids:
            id_list = mail_ids.split(' ')

        for i in id_list:
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['date']
                    now = datetime.datetime.now()
                    now = now.strftime("%a, %d %B")
                    if email_from == SENDER and now in email_date:
                        print("Processing {} @ {}".format(email_subject, datetime.datetime.now()))
                        if email_subject == 'Launch services':
                            # Store email in trash
                            mail.store(i, '+X-GM-LABELS', '\\Trash')
                            mail.expunge()
                            # Start services
                            subprocess.call(SERVICE, shell=True)
                        elif email_subject == 'Kill services':
                            # Store mail in trash
                            mail.store(i, '+X-GM-LABELS', '\\Trash')
                            mail.expunge()
                            # Kill service
                            subprocess.call(['killall', SERVICE])
    except Exception as e:
        print(e)

def main():
    """
    main()

    :return:
    """
    read_email()


if __name__ == '__main__':
    main()
