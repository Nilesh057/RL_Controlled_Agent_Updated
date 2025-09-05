import csv
import os
from datetime import datetime

def track_reward(episode, total_reward, episode_log_path="data/episode_log.txt"):
    """Track episode rewards in a log file"""
    os.makedirs(os.path.dirname(episode_log_path), exist_ok=True)
    file_exists = os.path.isfile(episode_log_path)
    
    with open(episode_log_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Episode", "Total Reward", "Timestamp"])
        writer.writerow([episode, total_reward, datetime.now().isoformat(timespec="seconds")])