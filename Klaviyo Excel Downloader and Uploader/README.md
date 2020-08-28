# Email Downloader and Klaviyo Profiles Uploader
A script that will download all attachments of the most recent email by email subject line. After attachments are downloaded, the script will upload the excel files using the Klaviyo API. Please note Klaviyo only allows adding a maxiumum of 100 profiles per request.

## Instructions
1. user = '' -> Type username
2. password = '' -> Enter password
3. outputdir = '' -> Modify output directory of downloaded attachments
4. subject_list = [] -> enter all the subjects to search for downloading attachments
5. csvFilePath = [] -> path to each downloaded file. Leave it alone.
6. list_id_list = [] -> list id of each klaviyo list where the csv files will be uploaded to
7. api_key = '' -> Klaviyo API Key of your account

Note: For subject_list and list_id_list, the order of the entered email subjects and order of the Klaviyo list id is important. The script takes the attachments of the first email and uploads it to Klaviyo with the first list id then the second email with the second list id and so on.

## Installation
pip3 install imaplib <br />
pip3 install email <br />
pip3 install os <br />
pip3 install requests <br />
pip3 install csv <br />
pip3 install datetime import date <br />
pip3 install time <br />

## Python Version
Python 2.7.1

## Links
Klaviyo API Docs https://www.klaviyo.com/docs/api/v2/lists
