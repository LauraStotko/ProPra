#!/usr/bin/env python3

import cgi
import cgitb
import os
import tempfile
import subprocess
import html

cgitb.enable()  # Für Debugging-Zwecke

print("Content-Type: text/html;charset=utf-8")
print()


def handle_form():
    form = cgi.FieldStorage()
    if 'submit' in form:  # Prüft, ob das Formular gesendet wurde
        # Überprüfen, ob eine Datei hochgeladen wurde
        if 'file' in form and form['file'].filename:
            fileitem = form['file']
            # Erstellen einer temporären Datei zum Speichern der hochgeladenen PDB-IDs
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(fileitem.file.read())
                temp_file_path = temp.name
            pdb_ids = ''  # Setzen von pdb_ids auf einen leeren String, wenn eine Datei hochgeladen wird
        else:
            pdb_ids = form.getvalue('pdb_ids', '')

        atom_type = form.getvalue('atom_type', 'CA')

        # Pfad zum Python-Skript, das die eigentliche Logik enthält
        script_path = './seclib_pdb.py'

        # Erstellen einer temporären Datei für die Ausgabe
        output_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt')
        output_file_path = output_file.name
        output_file.close()

        # Kommandozeilenbefehl vorbereiten
        if pdb_ids:  # Wenn PDB-IDs direkt eingegeben wurden
            command = [script_path, "--ids"] + pdb_ids.split() + ["--output", output_file_path, "--atom_type",
                                                                  atom_type]
        else:  # Wenn eine Datei hochgeladen wurde
            command = [script_path, "--id_file", temp_file_path, "--output", output_file_path, "--atom_type", atom_type]

        # Ausführen des Python-Skripts und Erfassen der Ausgabe
        try:
            subprocess.run(command, check=True)
            print(f"<h2>Ergebnisse:</h2>")
            print(f"<textarea style='width:100%;height:300px;' readonly>")
            with open(output_file_path, 'r') as f:
                print(html.escape(f.read()))
            print("</textarea>")
            print(f"<br><a href='{output_file_path}' download>Klicke hier, um die Datei herunterzuladen</a>")
        except Exception as e:
            print(f"<h2>Ausnahmefehler:</h2>")
            print(f"<pre>{html.escape(str(e))}</pre>")

        # Bereinigung der temporären Dateien, wenn eine Datei hochgeladen wurde
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
    else:
        display_form()


def display_form():
    print("""<html><head><title>PDB ID Verarbeitung</title></head><body>
            <h1>PDB-IDs Einreichen</h1>
            <form enctype="multipart/form-data" action="" method="post">
                <p>PDB-IDs (durch Leerzeichen getrennt):<br>
                <textarea name="pdb_ids" rows="5" cols="30"></textarea></p>
                <p>ODER lade eine Textdatei mit PDB-IDs hoch:<br>
                <input type="file" name="file" /></p>
                <p>Atomtyp: <input type="text" name="atom_type" value="CA"></p>
                <input type="submit" name="submit" value="Submit" />
            </form>
        </body></html>""")


if __name__ == "__main__":
    handle_form()


