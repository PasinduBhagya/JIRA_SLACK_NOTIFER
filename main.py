import configparser
import re
import logging

from check_jira_updates import main_function

BASE_DIR = '/opt/jira_slack_notifier/'

monitorConfig = configparser.ConfigParser()
monitorConfig.read(BASE_DIR + 'monitors.cfg')

config = configparser.ConfigParser()
config.read(BASE_DIR + '.env')


monitor_sections = monitorConfig.sections()
monitor_pattern = re.compile(r"^MONITOR_\d+$")


logging.basicConfig(filename=BASE_DIR + config.get('LOGGING', 'LOG_FILE'), 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

for index, section in enumerate(monitor_sections, start=1):
    if monitor_pattern.match(section):
        logging.info(f"Valid section was found - {section}")

        webhook_url = monitorConfig.get(section, 'WEBHOOK_URL')
        jql = monitorConfig.get(section, 'JQL').strip("'")
        notify_fields = monitorConfig.get(section, 'NOTIFY_FIELDS')

        main_function(webhook_url, jql, notify_fields)
    else:
        logging.warning(f"{section} is not a valid monitor section. Skipping.")