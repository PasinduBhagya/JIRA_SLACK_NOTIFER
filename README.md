# 📝 JIRA Monitor Service

A Python-based automation service that monitors JIRA updates and sends notifications to Slack every 5 minutes using `systemd` timers.  
Ideal for teams that want real-time updates without manual checks.

---

## ⚡ Quick Setup

Follow these steps to quickly set up the JIRA Monitor Service on your Linux system:

```bash
# Navigate to /opt directory
cd /opt 

# Clone the repository
git clone https://github.com/PasinduBhagya/jira_slack_notifier.git
cd jira_slack_notifier

# Rename and configure the environment file
mv sample.env .env
nano .env
```

Update the `.env` file with your JIRA credentials and instance details:

```ini
EMAIL=myemail@example.com
API_TOKEN=mytoken
JIRA_URL=https://myjiraurl.example.com
```

Next, rename and configure the monitor configuration file:

```bash
mv sample-monitors.cfg monitors.cfg
nano monitors.cfg
```

Example configuration for `monitors.cfg`:

```ini
[MONITOR_1]
WEBHOOK_URL=https://hooks.slack.com/services/xxxx/yyyy/zzzz
JQL=project='MYPROJECT AND status="In Progress"'
NOTIFY_FIELDS=["summary", "status", "assignee"]
```

Once configured, reload `systemd` and enable the timer:

```bash
# Reload systemd daemon to detect new service and timer files
sudo systemctl daemon-reload

# Start the JIRA monitor timer
sudo systemctl start monitor-jira.timer

# Enable the timer to start automatically at boot
sudo systemctl enable monitor-jira.timer

# (Optional) Run the service immediately
sudo systemctl start monitor-jira.service
```

✅ **Your JIRA Monitor Service is now live!**  
It will automatically check for new or updated issues every 5 minutes and send notifications to Slack.

---

## 🛠️ Installation

### 1️⃣ Create the Service File

Create a systemd service file named `monitor-jira.service`:

```bash
sudo nano /etc/systemd/system/monitor-jira.service
```

Paste the following configuration:

```ini
[Unit]
Description=Service to Monitor JIRA updates and notify via Slack

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/jira_slack_notifier/main.py
```

Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

### 2️⃣ Create the Timer File

Create a systemd timer file named `monitor-jira.timer`:

```bash
sudo nano /etc/systemd/system/monitor-jira.timer
```

Paste the following configuration:

```ini
[Unit]
Description=Run monitor-jira.service every 5 minutes

[Timer]
OnCalendar=*:0/5
Persistent=true
Unit=monitor-jira.service

[Install]
WantedBy=timers.target
```

Save and exit.

---

## 🚀 Deployment

Run these commands to deploy and enable the timer:

```bash
# Reload systemd to recognize new files
sudo systemctl daemon-reload

# Start the timer
sudo systemctl start monitor-jira.timer

# Enable the timer to start automatically on boot
sudo systemctl enable monitor-jira.timer

# (Optional) Run the service immediately
sudo systemctl start monitor-jira.service
```

---

## 🔍 Verification

Check if the timer and service are running correctly:

```bash
# Check timer status
sudo systemctl status monitor-jira.timer

# Check service status
sudo systemctl status monitor-jira.service

# View recent logs
sudo journalctl -u monitor-jira.service -n 20
```

---

## 🗓️ Schedule Details

- **Runs every:** 5 minutes  
- **Executes:** `/opt/jira_slack_notifier/main.py`  
- **Purpose:** Monitors new JIRA updates and sends Slack notifications

---

## 🧩 Roadmap

- Add error handling and logging to a file  
- Support multiple JIRA projects  
- Integrate retry mechanism for failed Slack notifications  
- Add configuration via `.env` and `monitors.cfg` files  
- Extend Slack notifications with rich formatting (attachments, buttons)  

---

## 📚 References

- [systemd Timers Documentation](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)  
- [Python Official Documentation](https://docs.python.org/3/)  
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)

---

## 🔧 Project Notes

- Ensure Python 3 is installed (`python3 --version`)  
- Place your Python script at `/opt/jira_slack_notifier/main.py`  
- Update JIRA configurations in `.env`  
- Update Slack webhook URLs and JQL filters in `monitors.cfg`  
- Test manually before enabling the timer:
  ```bash
  python3 /opt/jira_slack_notifier/main.py
  ```

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/python-3.11-blue)
![Systemd](https://img.shields.io/badge/systemd-enabled-green)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
