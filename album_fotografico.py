def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            righe = f.readlines()[1:]  # salto l'intestazione
    except FileNotFoundError:
        print(f"Errore: il file '{file_path}' non esiste.")  # messaggio d'errore
        return None

    album = []                  #album = lista di [anno, [foto, ...]]
    for riga in righe:
        if not riga.strip():  # ignoro righe vuote
            continue
        codice, titolo, autore, mese, anno = [c.strip() for c in riga.split(",")]
        foto = [codice, titolo, autore, int(mese), int(anno)]
        for elemento in album:  # cerco se l'anno esiste già
            if elemento[0] == foto[4]:
                elemento[1].append(foto)
                break
        else:  # anno non trovato: lo creo
            album.append([foto[4], [foto]])
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if not (len(codice) == 4 and codice[0] == "P" and codice[1:].isdigit()):  # formato P + 3 cifre
        return None

    if not 1 <= mese <= 12:  # mese non valido
        return None

    for elemento in album:  # elemento = [anno, [foto, ...]]
        for f in elemento[1]:  # elemento[1] = lista delle foto di quell'anno
            if f[0] == codice:  # f[0] = codice della foto
                return None

    try:
        with open(file_path, "r+", encoding="utf-8") as f:  # r+ dà errore se il file non esiste
            f.read()
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None

    foto = [codice, titolo, autore, mese, anno]
    for elemento in album:
        if elemento[0] == anno:  # l'anno della nuova foto esiste già
            elemento[1].append(foto)
            break
    else:
        album.append([anno, [foto]])
    return foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for elemento in album:
        for f in elemento[1]:
            if f[0] == codice:
                return ", ".join(str(x) for x in f) #unisco i campi in una stringa: P001, Titolo, Autore, 7, 2019
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for a, foto_anno in album:
        if a == anno:
            return sorted([f[1] for f in foto_anno]) # raccolgo i titoli (f[1]) di tutte le foto dell'anno e li restituisco in ordine alfabetico
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
