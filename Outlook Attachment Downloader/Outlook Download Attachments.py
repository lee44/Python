import imaplib
import email
import os

server = 'outlook.office365.com'
user = ''
password = ''
outputdir = ''
subject= ''

# connects to email client through IMAP
def connect(server, user, password):
    # Set up a connection to the mail server
    m = imaplib.IMAP4_SSL(server)
    # Login into mail account
    m.login(user, password)
    # No arguments in select() means selecting all mailboxes
    m.select()
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
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))

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
    # Grabs the last email for each subject. Delete [-1:] to show all emails for each subject
    for emailid in msgs[-1:]:
        downloaAttachmentsInEmail(m, emailid, outputdir)

subjectQuery(subject)