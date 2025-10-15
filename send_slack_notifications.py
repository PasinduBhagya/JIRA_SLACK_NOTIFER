import requests
import json
import logging
import configparser

BASE_DIR = '/opt/JIRA_SLACK_NOTIFER/'

config = configparser.ConfigParser()
config.read(BASE_DIR + '.env')

def send_slack_notification(message, webhook_url):
    
    Success_Message = config.get('MESSAGES', 'Success_Message')
    Error_Message = config.get('MESSAGES', 'Error_Message')


    logging.basicConfig(filename=BASE_DIR + config.get('LOGGING', 'LOG_FILE'),
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s') 

    try:

        if not webhook_url:
            logging.error("WEBHOOK_URL is not set in the configuration file.")
            exit(1)

        payload = {
        "text": message
        }

        response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            logging.error(f"Request to Slack returned an error {response.status_code}, the response is: - {response.text}")
        else:
            
            logging.info(Success_Message)

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        logging.error(e)
