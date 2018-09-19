import os
import sys
import yaml
import hashlib
import sendgrid
import logging
import datetime
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
        logging.error('Error during requests to {0} : {1}'.format(url, str(e)))
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

        logging.info('email-response-start')
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
        logging.info('email-response-end')
    except Exception as e:
        logging.error('Error sending email: {0}'.format(str(e)))


file = open('config.yml', 'r')
config = yaml.load(file.read())
logging.basicConfig(filename=config['LOG_FILE'], level=logging.INFO)

logging.info('-----')
logging.info('{0} started'.format(datetime.datetime.now().isoformat()))

disable_checksum = "7b73d2b45d13f688ac0d07bac8bd0fd1"
content = get_url_content(config['VISA_URL'])

if content is None:
    logging.info('Not content from: {0}'.format(config['VISA_URL']))
    sys.exit(os.EX_OK)

html = BeautifulSoup(content, 'html.parser').select('#app_actions')[0]

checksum = hashlib.md5()
checksum.update(html.prettify())
checksum = checksum.hexdigest()

logging.info('checksum when is CURRENT "{0}"'.format(checksum))
logging.info('checksum when is DISABLE "{0}"'.format(config['CHECKSUM']))
if checksum != config['CHECKSUM']:
    notify()
else:
    logging.info('NOT AVAILABLE')

logging.info('{0} finished'.format(datetime.datetime.now().isoformat()))
