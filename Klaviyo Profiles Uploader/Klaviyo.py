import imaplib
import email
import os
import requests
import csv 
from datetime import date 
import time

server = 'outlook.office365.com'
user = ''
password = ''
outputdir = '/Users/user_name/Downloads'

#Subject of the emails you want to download attachments from
subject_list = []
# Path to each file that was downloaded from emails
csvFilePath = []

# list_id of each klaviyo list where the csv files will be uploaded to
list_id_list = []
# Klaviyo API Key
api_key = ''

# connects to email client through IMAP
def connect(server, user, password):
    # Set up a connection to the mail server
    m = imaplib.IMAP4_SSL(server)
    # Login into mail account
    m.login(user, password)
    # No arguments in select() means selecting all mailboxes
    m.select('Reports')
    return m

# downloads attachment for an email id, which is a unique identifier for an
# email, which is obtained through the msg object in imaplib, see below 
# subjectQuery function. 'emailid' is a variable in the msg object class.

def downloaAttachmentsInEmail(m, emailid, outputdir):
    # Body.PEEK reads the entire email without marking the email as read
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    # mail variable is now a Message Object Model, which is like a tree that needs to be traversed
    mail = email.message_from_bytes(email_body)
    # For attachments, we don't want content type that has multipart. Note: content type consists of maintype/subtype
    if mail.get_content_maintype() != 'multipart':
        return
    # for-loop is traversing the message tree that comes from mail.walk()
    for part in mail.walk():
        # Content-Disposition response header is a header indicating if the content is expected to be displayed as an attachment, that is downloaded and saved locally.
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            path = outputdir + '/' + str(date.today()) + '_' + part.get_filename()
            csvFilePath.append(path)
            open(path, 'wb').write(part.get_payload(decode=True))

# download attachments from all emails with a specified subject line
# search query is executed with a subject filter
# a list of msg objects are returned in msgs, and then looped through to 
# obtain the emailid variable, which is then passed through to the above 
# downloadAttachmentsinEmail function

def subjectQuery(subject):
    m = connect(server, user, password)
    m.select()
    # typ is the response while msgs is all the email id's with the specified subject
    typ, msgs = m.search(None, '(SUBJECT "' + subject + '")')
    # msgs is a list with length = 1. This only index contains a byte literal of all the email id's
    msgs = msgs[0].split()
    # Grabs the last email for each subject
    for emailid in msgs[-1:]:
        downloaAttachmentsInEmail(m, emailid, outputdir)

def getList(list_id):
    url = 'https://a.klaviyo.com/api/v2/list/'+list_id
    # Klaviyo API docs say arguments such as the api-key can be sent as a content type application/json
    headers = {"api-key" : api_key,"Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    print(response.content)

def updateList(list_id,csvFilePath):
    url = 'https://a.klaviyo.com/api/v2/list/'+list_id+'/members'
    # Klaviyo API docs say arguments such as the api-key can be sent as a content type application/json
    headers = {"api-key" : api_key,"Content-Type" : "application/json"}
    profiles = make_json(csvFilePath)
    response = requests.post(url, headers=headers, json = profiles)
    print(response.content)

# Function to convert a CSV to JSON
def make_json(csvFilePath): 
    # create a dictionary
    profiles = {}
    # create a list inside a dictionary
    profiles['profiles'] = [] 
      
    # Open csv and read with DictReader which creates key/value pairs using column headers and row values
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
          
        # csvReader is a list where each index contains a dictionary. In that dictionary, is the key/value pairs for the entire row. 
        for rows in csvReader: 
            profiles['profiles'].append(rows)

    return profiles

# # Download all attachments from email using the subjects
for subject in subject_list:
    subjectQuery(subject)

time.sleep(10)

# Pairs each element from both list as dictionary entries sequentially
res = dict(zip(list_id_list, csvFilePath))

for key, value in res.items():
    updateList(key,value)