import os
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories for images, videos, wbfs, office files, Cisco Packet Tracer files etc.
source_dir = "/Users/Mohamed/Downloads"
image_dir = "/Users/Mohamed/Pictures/downloaded images"
video_dir = "/Users/Mohamed/Videos/downloaded videos"
office_dir = "/Users/Mohamed/Documents/Office Files"
cisco_dir = "/Users/Mohamed/Documents/Cisco Packet Tracer Files"
wbfs_dir = "C:/wbfs"

def moveFile(dest, entry, name):
    dest_path = os.path.join(dest, name)
    if not os.path.exists(dest_path):
        shutil.move(entry, dest)
        logging.info(f"Moved file {name} to {dest}")
    else:
        logging.info(f"File {name} already exists in {dest}")

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            name = os.path.basename(event.src_path)
            # Handle images
            if name.endswith(('.png', '.jpg', '.jpeg')):
                moveFile(image_dir, event.src_path, name)
            # Handle videos
            elif name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                moveFile(video_dir, event.src_path, name)
            # Handle .wbfs files
            elif name.endswith('.wbfs'):
                moveFile(wbfs_dir, event.src_path, name)
            # Handle PowerPoint, Word, and Excel files
            elif name.endswith(('.pptx', '.ppt', '.docx', '.doc', '.xlsx', '.xls')):
                moveFile(office_dir, event.src_path, name)
            # Handle Cisco Packet Tracer files (.pkt)
            elif name.endswith('.pkt'):
                moveFile(cisco_dir, event.src_path, name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir  # Monitor the source directory
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
