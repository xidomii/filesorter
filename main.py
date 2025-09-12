import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Benutzername anpassen!
benutzername = "ibinc"

# Quell- und Zielordner
quelle = f"C:/Users/{benutzername}/Downloads"
ziel = f"C:/Users/{benutzername}/SortierterDownload"  # neuer Zielordner

# Kategorien
kategorien = {
    "Bilder": [".jpg", ".png", ".jpeg", ".gif"],
    "Musik": [".mp3", ".wav", ".flac"],
    "Dokumente": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Sonstiges": []
}

def sortiere_datei(pfad):
    if os.path.isfile(pfad):
        datei = os.path.basename(pfad)
        _, endung = os.path.splitext(datei)
        endung = endung.lower()

        # 👇 TMP-Dateien überspringen
        if endung == ".tmp":
            print(f"⚠️ Temporäre Datei ignoriert: {datei}")
            return

        verschoben = False
        for kategorie, endungen in kategorien.items():
            if endung in endungen:
                zielordner = os.path.join(ziel, kategorie)
                os.makedirs(zielordner, exist_ok=True)
                shutil.move(pfad, os.path.join(zielordner, datei))
                print(f"→ {datei} → {kategorie}")
                verschoben = True
                break

        if not verschoben:
            zielordner = os.path.join(ziel, "Sonstiges")
            os.makedirs(zielordner, exist_ok=True)
            shutil.move(pfad, os.path.join(zielordner, datei))
            print(f"→ {datei} → Sonstiges")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)  # kleine Pause, falls Datei noch geschrieben wird
            sortiere_datei(event.src_path)

if __name__ == "__main__":
    print(f"📂 Überwache Ordner: {quelle}")
    print(f"📂 Sortiere Dateien nach: {ziel}")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, quelle, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
