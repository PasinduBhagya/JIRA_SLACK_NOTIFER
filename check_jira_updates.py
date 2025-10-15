import requests
from requests.auth import HTTPBasicAuth
import configparser
from datetime import datetime, timedelta, timezone
import logging
from send_slack_notifications import send_slack_notification

BASE_DIR = '/opt/jira_slack_notifier/'

config = configparser.ConfigParser()
config.read(BASE_DIR + '.env')

logging.basicConfig(filename=BASE_DIR + config.get('LOGGING', 'LOG_FILE'), 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

email = config.get('JIRA', 'EMAIL')
api_token = config.get('JIRA', 'API_TOKEN')
JIRA_URL = config.get('JIRA', 'JIRA_URL')

now_time = datetime.now(timezone.utc)

url = f"{JIRA_URL}/rest/api/3/search/jql"

headers = {
        "Accept": "application/json"
}


def new_tickets(key, issue_url, summary, webhook_url, reporter, priority):

    logging.info(f"{key}: - has been created 5 mins ago!")
    message = (
            f"🆕 *New Jira Ticket Created!*\n"
            f"<{issue_url}|{key}>\n"
            f"```"
            f"Summary:  {summary}\n"
            f"Reporter: {reporter}\n"
            f"```"
        )
    send_slack_notification(message, webhook_url)

def check_comment_updates(key, issue_url, webhook_url):
    comment_url = f"{JIRA_URL}/rest/api/3/issue/{key}/comment"

    comment_response = requests.get(comment_url, headers=headers, auth=HTTPBasicAuth(email, api_token))
    comment_response.raise_for_status()
    comment_data = comment_response.json()
    comments = comment_data.get("comments", [])

    for comment in comments:
        comment_created = comment.get("created")
        comment_updated = comment.get("updated")

        comment_created_time = datetime.strptime(comment_created, "%Y-%m-%dT%H:%M:%S.%f%z")
        comment_updated_time = datetime.strptime(comment_updated, "%Y-%m-%dT%H:%M:%S.%f%z")

        if now_time - comment_updated_time < timedelta(minutes=5):
            author = comment.get("author", {}).get("displayName", "Unknown")
            body = comment.get("body", {}).get("content", [])
            comment_text = ""
            for content in body:
                for inner_content in content.get("content", []):
                    if inner_content.get("type") == "text":
                        comment_text += inner_content.get("text", "")
            logging.info(f"{key}: Comment updated by {author}: {comment_text}")
            message_2 = (
                f"✏️ *Comment Updated!*\n"
                f"<{issue_url}|{key}>\n"
                f"```"
                f"Author:   {author}\n"
                f"Updated:  {comment_updated_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Comment:  {comment_text.strip()}\n"
                f"```"
            )
            send_slack_notification(message_2, webhook_url)

        elif now_time - comment_created_time < timedelta(minutes=5):
            author = comment.get("author", {}).get("displayName", "Unknown")
            body = comment.get("body", {}).get("content", [])
            comment_text = ""
            for content in body:
                for inner_content in content.get("content", []):
                    if inner_content.get("type") == "text":
                        comment_text += inner_content.get("text", "")
            logging.info(f"{key}: New comment by {author}: {comment_text}")
            message_1 = (
                f"💬 *New Comment Added!*\n"
                f"<{issue_url}|{key}>\n"
                f"```"
                f"Author:  {author}\n"
                f"Comment: {comment_text.strip()}\n"
                f"```"
            )

            send_slack_notification(message_1, webhook_url)

        

def check_field_changes(key, issue_url, notify_fields, webhook_url):
    
    changelog_url = f"{JIRA_URL}/rest/api/3/issue/{key}/changelog"
    
    try:
        changelog_response = requests.get(changelog_url, headers=headers, auth=HTTPBasicAuth(email, api_token))
        changelog_response.raise_for_status()
        changelog_data = changelog_response.json()

        histories = changelog_data.get("values", [])

        if histories is not None:
            for history in histories:
                created = history.get("created")
                created_time = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%f%z")
                if now_time - created_time < timedelta(minutes=5):

                    items = history.get("items", [])
                    for item in items:
                        
                        field = item.get("field")

                        from_string = item.get("fromString", "None")
                        to_string = item.get("toString", "None")

                        if field in notify_fields:
                            logging.info(f"{field} was found in notify_fields.")
                            message = (
                                    f"🔄 *Ticket Updated!*\n"
                                    f"<{issue_url}|{key}>\n"
                                    f"```"
                                    f"Ticket: {key}\n"
                                    f"Field:  {field}\n"
                                    f"From:   {from_string}\n"
                                    f"To:     {to_string}\n"
                                    f"```"
                                )
                            send_slack_notification(message, webhook_url)

                        logging.info(f"{key}: Field '{field}' changed from '{from_string}' to '{to_string}'")

        else:
            logging.info(f"{key}: No changelog history found.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching changelog for {key}: {e}")

def check_jira_updates(webhook_url, params, notify_fields):
    logging.info("Script started.")
    try:
        response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(email, api_token))
        response.raise_for_status()
        data = response.json()
        issues = data.get("issues", [])

        if not issues:
            logging.info("No unresolved tickets found.")
        else:
            for issue in issues:
                key = issue["key"]

                summary = issue["fields"]["summary"]
                issue_url = f"{JIRA_URL}/browse/{key}"

                updated_time = datetime.strptime(issue["fields"]["updated"], "%Y-%m-%dT%H:%M:%S.%f%z")
                created_time = datetime.strptime(issue["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                reporter = issue["fields"]["reporter"]["displayName"]
                priority = issue["fields"].get("priority")

                if now_time - created_time < timedelta(minutes=5):
                    new_tickets(key, issue_url, summary, webhook_url, reporter, priority)
                else:
                    if now_time - updated_time < timedelta(minutes=5):
                        logging.info(f"{key}: - has been updated 5 mins ago!")
                        check_field_changes(key, issue_url, notify_fields, webhook_url)
                        
                        if "comments" in notify_fields:
                            check_comment_updates(key, issue_url, webhook_url)
                        else:
                            logging.info(f"Comments not in notify_fields, skipping comment check for {key}.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to Jira: {e}")
    
    logging.info("Script Ended.")

def check_updates_on_high_priority():
    pass

def main_function(webhook_url, jql, notify_fields):
    params = {
        "jql": jql,
        "fields": "summary,status,assignee,created,priority,updated,reporter",
    }

    check_jira_updates(webhook_url, params, notify_fields)


