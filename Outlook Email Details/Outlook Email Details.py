import imaplib
import email
import os

server = 'outlook.office365.com'
user = ''
password = ''
subject = ''

def emailDetails():
    connection = imaplib.IMAP4_SSL(server)
    connection.login(user, password)
    # In outlook, folders are not considered mailboxes. Leaving it blank means all mailboxes
    connection.select()
    result, data = connection.uid('search', '(SUBJECT "' + subject + '")')
    if result == 'OK':
        email_id = data[0].split()
        for num in email_id[-1:]:
            result, data = connection.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])
                print('From:' + email_message['From'])
                print('To:' + email_message['To'])
                print('Date:' + email_message['Date'])
                print('Subject:' + str(email_message['Subject']))
                # print('Content:' + str(email_message.get_payload()[0]))
    connection.close()
    connection.logout()    

emailDetails()