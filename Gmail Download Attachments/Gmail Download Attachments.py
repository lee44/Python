# Two Step Verification - Off
# Less Secure App Access - On
# IMAP - Enabled

import imaplib, email

imap_url = 'imap.gmail.com'
user = ''
password = ''
subject = ''

print('Connecting to ' + imap_url)

# Setting up connection
con = imaplib.IMAP4_SSL(imap_url)
# Log In Gmail Account
con.login(user,password)
# List of Mail Box Names
boxlist = con.list()
# print(boxlist)

# Specify which Mail Box to search through. Blank means all mail boxes
con.select()

result, data = con.uid('search', '(SUBJECT "' + subject + '")')
ids = data[0]
# list of uids
id_list = ids.split()

i = len(id_list)
for x in range(i):
    latest_email_uid = id_list[x]

    # fetch the email body (RFC822) for the given ID
    result, email_data = con.uid('fetch', latest_email_uid, '(RFC822)')
    
    raw_email = email_data[0][1]
    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    print(raw_email_string)
    email_message = email.message_from_string(raw_email_string)
    print(email_message)
    # downloading attachments
    for part in email_message.walk():
        
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join('C:/DownloadPath/', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]

    try:
        fileName
    except NameError:
        fileName = 'No File'

    print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))

con.close()
con.logout()