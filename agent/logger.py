import csv
import os
import random
from datetime import datetime

def log_episode(log_path, task_id, intent, action, reward, feedback, suggestion):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)
    confidence = round(random.uniform(0.5, 1.0), 2)
    timestamp = datetime.now().isoformat(timespec="seconds")

    with open(log_path, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow([
                "Task ID", "Parsed Intent", "Action Taken", "Reward Assigned",
                "Timestamp", "Agent Confidence", "User Feedback", "Suggested Correction"
            ])
        w.writerow([task_id, intent, action, reward, timestamp, confidence, feedback, suggestion or ""])

def log_total_reward(episode, total_reward, episode_log_path):
    """Log total reward for an episode"""
    os.makedirs(os.path.dirname(episode_log_path), exist_ok=True)
    file_exists = os.path.isfile(episode_log_path)
    timestamp = datetime.now().isoformat(timespec="seconds")
    
    with open(episode_log_path, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["Episode", "Total Reward", "Timestamp"])
        w.writerow([episode, total_reward, timestamp])
