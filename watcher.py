#!/usr/bin/env python

import logging
import os
import shutil
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileHandler(FileSystemEventHandler):
    def __init__(self, src_folder, dest_folder):
        self.src_folder = src_folder
        self.dest_folder = dest_folder

    def on_created(self, event):
        if not event.is_directory:
            src_path = event.src_path
            dest_path = self.get_destination_path(src_path)
            copy_file(src_path, dest_path)
            logging.info(f"Created: {src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            src_path = event.src_path
            dest_path = self.get_destination_path(src_path)
            copy_file(src_path, dest_path)
            logging.info(f"Modified: {src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            src_path = event.src_path
            dest_path = self.get_deleted_marker_path(src_path)
            with open(dest_path, "w") as marker_file:
                marker_file.write("[DELETED]")
            logging.info(f"Deleted: {src_path}")

    def get_destination_path(self, src_path):
        relative_path = os.path.relpath(src_path, self.src_folder)
        return os.path.join(self.dest_folder, relative_path)

    def get_deleted_marker_path(self, src_path):
        filename = os.path.basename(src_path)
        marker_filename = f"{filename} [DELETED].txt"
        return os.path.join(self.dest_folder, marker_filename)


def copy_file(source_path, destination_path):
    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    shutil.copy2(source_path, destination_path)


if __name__ == "__main__":
    src_folder = "/source"
    dest_folder = "/destination"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Create the observer and event handler
    event_handler = FileHandler(src_folder, dest_folder)
    observer = Observer()
    observer.schedule(event_handler, src_folder, recursive=True)

    logging.info(f"Syncing {src_folder} to {dest_folder}")

    # Start the observer
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
