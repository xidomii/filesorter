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

def warte_bis_fertig(pfad, timeout=30):
    """Wartet, bis die Datei fertig geschrieben ist (Größe bleibt stabil)."""
    letzte_groesse = -1
    start = time.time()

    while True:
        try:
            aktuelle_groesse = os.path.getsize(pfad)
        except FileNotFoundError:
            return False  # Datei verschwunden

        if aktuelle_groesse == letzte_groesse:
            return True  # Datei ist stabil = fertig

        letzte_groesse = aktuelle_groesse
        time.sleep(1)

        if time.time() - start > timeout:
            print(f"⚠️ Timeout: {os.path.basename(pfad)} wird vielleicht noch benutzt.")
            return False

def sortiere_datei(pfad):
    if os.path.isfile(pfad):
        datei = os.path.basename(pfad)
        _, endung = os.path.splitext(datei)
        endung = endung.lower()

        # 👇 TMP-Dateien komplett ignorieren
        if endung == ".tmp":
            print(f"⏭️ Ignoriere temporäre Datei: {datei}")
            return

        # 👇 Erst warten, bis Datei fertig ist
        if not warte_bis_fertig(pfad):
            print(f"⚠️ Datei konnte nicht verschoben werden: {datei}")
            return

        verschoben = False
        for kategorie, endungen in kategorien.items():
            if endung in endungen:
                zielordner = os.path.join(ziel, kategorie)
                os.makedirs(zielordner, exist_ok=True)
                shutil.move(pfad, os.path.join(zielordner, datei))
                print(f"✅ {datei} → {kategorie}")
                verschoben = True
                break

        if not verschoben:
            zielordner = os.path.join(ziel, "Sonstiges")
            os.makedirs(zielordner, exist_ok=True)
            shutil.move(pfad, os.path.join(zielordner, datei))
            print(f"✅ {datei} → Sonstiges")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
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
