#!/usr/bin/python3
import cgi
import cgitb
import subprocess
import tempfile

cgitb.enable()

def print_menu():
    print('''<div id="menu" style="position: fixed; left: 0; top: 0; bottom: 0; background-color: #f1f1f1; padding: 20px;">
    <ul style="list-style-type:none; padding:0;">
        <li class="menu-item"><a href='./frontpage_cgi.py' style="font-size: 24px;">Start</a></li>
        <li class="menu-item"><a href='./git_cgi.py' style="font-size: 24px;">Git Anleitung</a></li>
        <li class="menu-item"><a href='./acsearch_cgi.py' style="font-size: 24px;">AC Search</a></li>
        <li class="menu-item"><a href='./workflow_cgi.py' style="font-size: 24px;">Genome to ORF</a><li>
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
    <title>Upload Files</title>
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 0;
            flex-direction: column;
            overflow-y:scroll;
            background-color: #add8e6;
        }
        h1 {
            font-size: 36px;
        }
        #form-container {
            text-align: center;
            padding: 20px;
            margin-top: 100px; /* Abstand nach oben */
        }
        input[type="file"] {
            font-size: 18px;
            padding: 5px;
            margin-top: 10px; /* Abstand nach oben */
        }
        input[type="submit"] {
            font-size: 18px;
            padding: 10px 20px;
            margin-top: 10px; /* Abstand nach oben */
        }
        .menu-item {
            margin-bottom: 10px;
        }
        #output-container {
            margin-top: 20px;
            margin-left: 250px;
            text-align: left;
            overflow-y: auto; 
        }
        pre {
            white-space: pre-line; 
            margin-left: 250px;
            padding: 10px;
            border: 1px solid #ccc; 
            background-color: #f9f9f9;
            width: 10%;
            overflow-y: auto; 
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div id="form-container">
    <h1>Upload Files</h1>
        <form method="post" enctype="multipart/form-data">
            <label for="fasta_file">Upload FASTA File:</label><br>
            <input type="file" id="fasta_file" name="fasta_file" accept=".fasta,.fna,.fa"><br>
            <label for="txt_file">Upload TXT File:</label><br>
            <input type="file" id="txt_file" name="txt_file" accept=".txt"><br>
            <input type="submit" value="Submit">
        </form>
    </div>    
''')

# menu
print_menu()

form = cgi.FieldStorage()

if "fasta_file" in form and "txt_file" in form:
    fasta_file = form["fasta_file"]
    txt_file = form["txt_file"]

    # Erstelle temp Dateien für die hochgeladenen Dateien
    with tempfile.NamedTemporaryFile(delete=False) as fasta_temp, tempfile.NamedTemporaryFile(delete=False) as txt_temp:
        fasta_temp.write(fasta_file.file.read())
        txt_temp.write(txt_file.file.read())

    # Aufruf des vorhandenen Skripts mit den temp Dateien als Argumente
    result = subprocess.run(["./Workflow.py", "--organism", fasta_temp.name, "--features", txt_temp.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode == 0:
        print('<div id="output-container">')
        print("<h2>Ergebnis:</h2>")
        print("<pre>")
        print(result.stdout.strip().replace("\n", "<br>"))
        print("</pre>")
        print('<p><a href="data:text/plain;charset=utf-8,' + result.stdout.strip().replace("\n", "%0A") + '" download="output.txt">Download Output</a></p>')
        print('</div>')
    else:
        print("<p>Ein Fehler ist aufgetreten. Bitte checken Sie Ihre Eingabe.</p>")

print('''</body>
</html>''')
