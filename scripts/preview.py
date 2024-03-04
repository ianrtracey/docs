import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".ipynb"):
            # avoid recursion by only running when ipynb files are changed
            subprocess.run("python scripts/render.py", shell=True)


if __name__ == "__main__":
    event_handler = FileChangeHandler()
    root = os.path.dirname(os.path.dirname(__file__))
    observer = Observer()
    observer.schedule(event_handler, path=root, recursive=True)
    observer.start()

    print(f"Watching directory '{root}' for changes...")
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
