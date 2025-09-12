def sortiere_datei(pfad):
    if not os.path.isfile(pfad):
        return

    datei = os.path.basename(pfad)
    _, endung = os.path.splitext(datei)
    endung = endung.lower()

    if endung in [".tmp", ".crdownload", ".part"]:
        print(f"⏭️ Ignoriere temporäre Datei: {datei}")
        return

    # Warten, bis Datei existiert und stabil ist
    if not warte_bis_fertig(pfad):
        print(f"⚠️ Datei konnte nicht verschoben werden (Timeout): {datei}")
        return

    verschoben = False
    for kategorie, endungen in kategorien.items():
        if endung in endungen:
            zielordner = os.path.join(ziel, kategorie)
            os.makedirs(zielordner, exist_ok=True)
            try:
                shutil.move(pfad, os.path.join(zielordner, datei))
                print(f"✅ {datei} → {kategorie}")
                verschoben = True
            except FileNotFoundError:
                print(f"⚠️ Datei nicht gefunden beim Verschieben: {datei}")
            break

    if not verschoben:
        zielordner = os.path.join(ziel, "Sonstiges")
        os.makedirs(zielordner, exist_ok=True)
        try:
            shutil.move(pfad, os.path.join(zielordner, datei))
            print(f"✅ {datei} → Sonstiges")
        except FileNotFoundError:
            print(f"⚠️ Datei nicht gefunden beim Verschieben: {datei}")
