import os
import sys
import yaml
import urllib
import hashlib
import sendgrid
from bs4 import BeautifulSoup
from requests import RequestException, get


def is_good_response(response):
    content_type = response.headers['Content-Type']
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('text/html') > -1)


def get_url_content(url):
    try:
        response = get(url)
        if is_good_response(response):
            return response.content
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
    return None


def notify():
    try:
        data = {
            "personalizations": [{
                "to": [{
                    "email": config['EMAIL_TO']
                }]
            }],
            "from": {
                "email": config['EMAIL_FROM']
            },
            "template_id": config['SEND_GRID_TEMPLATE']
        }
        mailer = sendgrid.SendGridAPIClient(apikey=config['SEND_GRID_KEY'])
        response = mailer.client.mail.send.post(request_body=data)

        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print('Error sending email: {0}'.format(str(e)))


file = open('config.yml', 'r')
config = yaml.load(file.read())

disable_checksum = "7b73d2b45d13f688ac0d07bac8bd0fd1"
content = get_url_content(config['VISA_URL'])

if content is None:
    sys.exit(os.EX_OK)

html = BeautifulSoup(content, 'html.parser').select('#app_actions')[0]

current_checksum = hashlib.md5()
current_checksum.update(html.prettify())
if current_checksum.hexdigest() != config['CHECKSUM']:
    notify()
else:
    print('The button "apply now" is NOT available')
