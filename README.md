# 📝 JIRA Monitor Service

A Python-based automation service that monitors JIRA updates and sends notifications to Slack every 5 minutes using `systemd` timers.  
Ideal for teams that want real-time updates without manual checks.

---

## ⚡ Quick Setup

```bash
# Clone the repo
cd /opt 
git clone https://github.com/PasinduBhagya/JIRA_SLACK_NOTIFER.git
cd JIRA_SLACK_NOTIFER

# Reload systemd, start and enable timer
sudo systemctl daemon-reload
sudo systemctl start monitor-jira.timer
sudo systemctl enable monitor-jira.timer
```

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
ExecStart=/usr/bin/python3 /opt/jira-monitor/main.py
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
- **Executes:** `/opt/JIRA_SLACK_NOTIFER/main.py`  
- **Purpose:** Monitors new JIRA updates and sends Slack notifications

---

## 🧩 Roadmap

- Add error handling and logging to a file  
- Support multiple JIRA projects  
- Integrate retry mechanism for failed Slack notifications  
- Add configuration via `.env` and `monitors.cfg` file  
- Extend Slack notifications with rich formatting (attachments, buttons)  

---

## 📚 References

- [systemd Timers Documentation](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)  
- [Python Official Documentation](https://docs.python.org/3/)  
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)

---

## 🔧 Project Notes

- Ensure Python 3 is installed (`python3 --version`)  
- Place your Python script at `/opt/JIRA_SLACK_NOTIFER/main.py`  
- Update JIRA configurations inside your script or via `.env` file  
- Update Slack webhook URL inside your script or via `monitors.cfg` file  
- Test manually first: `python3 /opt/JIRA_SLACK_NOTIFER/main.py`  

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/python-3.11-blue)
![Systemd](https://img.shields.io/badge/systemd-enabled-green)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

