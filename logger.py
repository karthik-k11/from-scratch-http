from datetime import datetime


def log_info(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[INFO] {timestamp} {message}")


def log_error(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[ERROR] {timestamp} {message}")