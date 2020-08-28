# Email Downloader and Klaviyo Uploader
A script that will download all attachments of the most recent email by email subject line. After attachments are downloaded, the script will upload the excel files using the Klaviyo API. Please note Klaviyo only allows adding a maxiumum of 100 profiles per request.

## Instructions
1. Type username to var user
2. Enter password
3. Modify output directory of downloaded attachments to var outputdir


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
