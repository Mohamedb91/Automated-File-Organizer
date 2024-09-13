import os 
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

source_dir = "/Users/Mohamed/Downloads"
image_dir = "/Users/Mohamed/Pictures/downloaded images"

def moveFile(dest, entry, name):
    files_exists = os.path.exists(dest + "/" + name)
    if files_exists:
        pass
    shutil.move(entry,dest)

class EventHandler(LoggingEventHandler):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            dest = source_dir
            if name.endswith('.png') or name.endswith('.jpg') or name.endswith('jpeg'):
                dest = image_dir
                moveFile(dest, entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()