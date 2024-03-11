#!/usr/bin/python3
import cgi
import cgitb
import subprocess
import tempfile
from get_pdb import download_as_fasta
from acsearch import acsearch

cgitb.enable()

print("Content-Type: text/html")
print()

print('''<!DOCTYPE html>
<html>
<head>
    <title>GOR Algorithmus</title>
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
        #menu {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            background-color: #f1f1f1;
            padding: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        .menu-item a {
            font-size: 24px;
            text-decoration: none;
            color: #000;
        }
        .menu-item a:hover {
            color: #666;
        }
    </style>
</head>
<body>
<div id="menu">
    <ul>
        <li class="menu-item"><a href='./frontpage_cgi.py'>Start</a></li>
        <li class="menu-item"><a href='./git_cgi.py'>Git Anleitung</a></li>
        <li class="menu-item"><a href='./acsearch_cgi.py'>AC Search</a></li>
        <li class="menu-item"><a href='./workflow_cgi.py'>Genome to ORF</a></li>
        <li class="menu-item"><a href='./gor_cgi.py'>GOR Algorithmus</a></li>
    </ul>
</div>

<div id="form-container">
    <h1>GOR Algorithmus</h1>
''')

print('''
    <style>
        #gor_type, #input_type, #input_data, #with_probabilities, #submit_button {
            font-size: 18px;
        }
        .form-button {
            font-size: 18px;
            padding: 10px 20px;
        }
    </style>
    <form action="gor_cgi.py" method="post" enctype="multipart/form-data">
        <label for="gor_type">GOR Typ:</label>
        <select id="gor_type" name="gor_type">
            <option value="GOR1">GOR1 (SOV median of 56.3)</option>
            <option value="GOR3">GOR3 (SOV median of 47.5)</option>
            <option value="GOR4">GOR4 (SOV median of 87.5)</option>
        </select><br><br>
        <label for="input_type">Input Art:</label>
        <select id="input_type" name="input_type" onchange="showInputField()">
            <option value="" disabled selected hidden>Choose</option>
            <option value="Sequenz">Sequenz</option>
            <option value="Fasta File">Fasta File</option>
            <option value="PDB ID">PDB ID</option>
            <option value="AC number">AC number</option>
            <option value="Multiple Alignment">Multiple Alignment</option>
        </select><br><br>
        <div id="input_field"></div><br>
        <input type="checkbox" id="with_probabilities" name="with_probabilities" value="with_probabilities">
        <label for="with_probabilities">Include Probabilities</label><br><br>
        <input type="submit" value="Submit">
    </form>
    <script>
        function showInputField() {
            var inputType = document.getElementById("input_type").value;
            var inputField = document.getElementById("input_field");
            inputField.innerHTML = "";
            if (inputType === "Sequenz") {
                inputField.innerHTML = "<label for='sequence_input'>Please upload your sequence:</label><br><textarea id='sequence_input' name='input_data' rows='4' cols='50'></textarea>";
            } else if (inputType === "AC number") {
                inputField.innerHTML = "<label for='ac_number_input'>AC Number:</label><br><input type='text' id='ac_number_input' name='input_data'>";
            } else if (inputType === "PDB ID") {
                inputField.innerHTML = "<label for='pdb_id_input'>PDB ID:</label><br><input type='text' id='pdb_id_input' name='input_data'>";
            } else if (inputType === "Fasta File") {
                inputField.innerHTML = "<label for='fasta_file_input'>Upload your fasta file:</label><br><input type='file' id='fasta_file_input' name='input_data' accept='.fasta'>";
            } else if (inputType === "Multiple Alignment") {
                inputField.innerHTML = "<label for='directory_input'>Upload your directory containing multiple alignments:</label><br><input type='file' id='directory_input' name='input_data' directory webkitdirectory mozdirectory msdirectory odirectory>";
            }
        }
    </script>
''')

form = cgi.FieldStorage()

gor_type = form.getvalue("gor_type")
input_type = form.getvalue("input_type")
input_data = form.getvalue("input_data")
with_probabilities = form.getvalue("with_probabilities") is not None

if gor_type and input_type and input_data:
    model_file = None
    if gor_type == "GOR1":
        model_file = "./Data/gor1_cb513_model.txt"
    elif gor_type == "GOR3":
        model_file = "./Data/gor3_cb513_model.txt"
    elif gor_type == "GOR4":
        model_file = "./Data/gor4_cb513_model.txt"

    if input_type == "Sequenz":
        input_file = "temp_sequence.txt"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fasta_temp:
            fasta_temp.write(input_data)

    elif input_type == "Fasta File":
        input_file = input_data
        with tempfile.NamedTemporaryFile(delete=False) as fasta_temp:
            fasta_temp.write(input_file.file.read())

    elif input_type == "AC number":
        input_file = acsearch(input_data)
        with tempfile.NamedTemporaryFile(delete=False) as fasta_temp:
            fasta_temp.write(input_file.file.read())
    elif input_type == "PDB ID":
        input_file = download_as_fasta(input_data)
        with tempfile.NamedTemporaryFile(delete=False) as fasta_temp:
            fasta_temp.write(input_file.file.read())

    command = ["java", "./predict.jar", "--model", model_file, "--format html", "--seq", fasta_temp.name]

    if with_probabilities:
        command.append("--probabilities")

    result = subprocess.run(command, capture_output=True, text=True)

    print("<div style='margin-left: 300px;'>")
    print("<h1>GOR Ergebnis</h1>")
    print("<pre>")
    print(result.stdout)
    print("</pre>")
    print("</div>")
#else:
    #print_gor_form()

print('''</div>
</body>
</html>''')