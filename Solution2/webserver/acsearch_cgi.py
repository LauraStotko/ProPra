#!/usr/bin/python3
import cgi
import cgitb
import subprocess

cgitb.enable()

def print_menu():
    print('''<div id="menu" style="position: fixed; left: 0; top: 0; bottom: 0; background-color: #f1f1f1; padding: 20px;">
    <ul style="list-style-type:none; padding:0;">
        <li class="menu-item"><a href='./frontpage_cgi.py' style="font-size: 24px;">Start</a></li>
        <li class="menu-item"><a href='./git_cgi.py' style="font-size: 24px;">Git Anleitung</a></li>
        <li class="menu-item"><a href='./acsearch_cgi.py' style="font-size: 24px;">AC Search</a></li>
        <li class="menu item"><a href='./workflow_cgi.py' style="font-size: 24px;">Genome to ORF</a><li>
        <li class="menu-item"><a href='./gor_cgi.py' style="font-size: 24px;">GOR Algorithmus</a><li>
    </ul>
</div>''')

# HTML-Header
print("Content-Type: text/html")
print()

# HTML-Seiteninhalt
print('''<!DOCTYPE html>
<html>
<head>
    <title>AC Search</title>
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 0;
            flex-direction: column; 
            background-color: #add8e6;
        }
        h1 {
            font-size: 36px;
        }
        #form-container {
            text-align: center;
            padding: 20px;
            margin-top: 20px; /* Änderung: Kleinere Margin */
            margin-bottom: 20px; /* Neue Regel: Abstand unterhalb des Formularcontainers */
        }
        input[type="text"] {
            width: 300px; /* Breite des Eingabefelds */
            font-size: 18px;
            padding: 5px;
            margin-top: 10px; /* Abstand nach oben */
        }
        input[type="submit"] {
            font-size: 18px;
            padding: 10px 20px;
            margin-top: 10px; /* Abstand nach oben */
        }
        .example {
            font-size: 16px;
            color: #666; /* Graue Farbe */
        }
        .menu-item {
            margin-bottom: 10px;
        }
        #output-container {
            margin-top: 20px;
            margin-left: 250px; /* Anpassung der Margin-Left-Eigenschaft */
            text-align: center;
            overflow-y: auto; /* Vertikales Scrollen ermöglichen */
            max-height: 400px; /* Maximale Höhe des Ausgabecontainers */
            width: 80%; /* Änderung: volle Breite des Containers */
        }
        pre {
            white-space: pre-line; /* Umbruch von langen Zeilen */
            padding: 10px;
            border: 1px solid #ccc; /* Rahmen um den Output */
            background-color: #f9f9f9; /* Hintergrundfarbe des Output-Containers */
            max-width: 80%; /* Maximalbreite des Output-Containers */
            overflow-x: hidden; 
            margin: 0 auto; /* Zentrieren des Containers */
        }
    </style>
</head>
<body>
    <div id="form-container">
    <h1>AC Search</h1>
        <form method="post">
            <label for="ac_number">SwissProt AC-Nummer:</label><br>
            <input type="text" id="ac_number" name="ac_number" placeholder="z.B.: P12345"><br>
            <input type="submit" value="Submit">
        </form>
    </div>    
''')

# Menüleiste einbinden
print_menu()

form = cgi.FieldStorage()

if "ac_number" in form:
    ac_number = form.getvalue("ac_number")

    result = subprocess.run(["./acsearch.py", "--ac", ac_number], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode == 0:
        print('<div id="output-container">')
        print("<h2>Ergebnis:</h2>")
        print("<pre>")
        print(result.stdout.strip().replace("\n", "<br>"))
        print("</pre>")
        print('</div>')
    else:
        print("<p>Ein Fehler ist aufgetreten. Bitte überprüfen Sie Ihre Eingabe.</p>")

print('''</body>
</html>''')
