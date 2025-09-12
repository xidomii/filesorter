import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


username = "ibinc"

source_dir = f"C:/Users/{username}/Downloads"
destination_dir = f"C:/Users/{username}/Documents/sortiert"

categories = {
    "Bilder": [".jpg", ",png", ".jpeg", ".gif",],
    "Musik": [".mp3", ".wav", ".flac"],
    "Dokumente": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archive": [".zip", ".rar", ".7z"],
    "Sonstiges": []
}

def sort_file(path):
    if os.path.isfile(path):
        file = os.path.basename(path)
        _, end = os.path.splitext(file)
        end = end.lower()

        moved = False
        for category, endings in categories.items():
            if end in endings:
                destination = os.path.join(destination_dir, category)
                os.makedirs(destination, exist_ok=True)
                shutil.move(path, os.path.join(destination, file))
                print(f"---> {file} ---> {category}")
                moved = True
                break

        if not moved:
            destination = os.path.join(destination_dir, "Sonstiges")
            os.makedirs(destination, exist_ok=True)
            shutil.move(path, os.path.join(destination, file))
            print(f"---> {file} ---> Sonstiges")


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            sort_file(event.src_path)


if __name__ == "__main__":
    print("Überwachung des Download-Ordners gestartet...")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()