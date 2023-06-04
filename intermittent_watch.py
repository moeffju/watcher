#!/usr/bin/env python

import configparser
import logging
import os
import shutil
import sys
import time
from datetime import datetime

CONFIG_FILE = "config.ini"

def copy_file(source_path, destination_path):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.copy2(source_path, destination_path)

def update_last_sync_timestamp(timestamp):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config['DEFAULT']['LastSyncTimestamp'] = str(timestamp)
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

def get_last_sync_timestamp():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return float(config['DEFAULT'].get('LastSyncTimestamp', 0.0))

def watch_folder(source_folder, destination_folder, interval=1):
    last_sync_timestamp = get_last_sync_timestamp()
    if last_sync_timestamp > 0.0:
        last_sync_timestamp_fmt = datetime.fromtimestamp(last_sync_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Resuming from {last_sync_timestamp_fmt}")
    logging.info(f"Watching '{source_folder}' every {interval} seconds, syncing to '{destination_folder}'")
    files_processed = False

    while True:
        for root, dirs, files in os.walk(source_folder):
            logging.debug(f"Checking {len(files)} files")
            for file in files:
                file_path = os.path.join(root, file)
                file_modified_timestamp = os.path.getmtime(file_path)
                if file_modified_timestamp > last_sync_timestamp:
                    destination_path = os.path.join(destination_folder, os.path.relpath(file_path, source_folder))
                    logging.info(f"Syncing '{file_path}' --> '{destination_path}'")
                    copy_file(file_path, destination_path)
                    files_processed = True
        
        if files_processed:
            last_sync_timestamp = time.time()
            update_last_sync_timestamp(last_sync_timestamp)
            files_processed = False
        
        time.sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    if len(sys.argv) < 3:
        logging.error("Please pass a source and destination directory")
        sys.exit(1)
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    watch_folder(sys.argv[1], sys.argv[2], interval)
