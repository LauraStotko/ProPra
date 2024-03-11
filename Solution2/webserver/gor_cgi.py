#!/usr/bin/python3
import cgi
import cgitb
import subprocess
import tempfile
import os
from get_pdb import download_as_fasta
from acsearch import acsearch

cgitb.enable()

def print_menu():
    print('''
    <div id="menu">
    <ul>
        <li class="menu-item"><a href='./frontpage_cgi.py'>Start</a></li>
        <li class="menu-item"><a href='./git_cgi.py'>Git Anleitung</a></li>
        <li class="menu-item"><a href='./acsearch_cgi.py'>AC Search</a></li>
        <li class="menu-item"><a href='./workflow_cgi.py'>Genome to ORF</a></li>
        <li class="menu-item"><a href='./gor_cgi.py'>GOR Algorithmus</a></li>
    </ul>
    </div>
    ''')

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
            overflow-y:scroll;
            background-color: #add8e6;
        }
        h1 {
            font-size: 36px;
        }
        #form-container {
            text-align: center;
            padding: 20px;
            margin-top: 100px; 
            margin-bottom: 20px;
            margin-left: 50px;
        }
        input[type="text"] {
            width: 300px; 
            font-size: 18px;
            padding: 5px;
            margin-top: 10px; 
        }
        input[type="submit"] {
            font-size: 18px;
            padding: 10px 20px;
            margin-top: 10px; 
        }
        .example {
            font-size: 16px;
            color: #666; 
        }
        .menu-item {
            margin-bottom: 10px;
        }
        #output-container {
            margin-top: 20px;
            margin-left: 50px;
            position: absolute;
            left: 50px;
            text-align: left;
            overflow-y: auto;
            width: 25cm;
            height: 30cm;
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #f9f9f9;
        }
        pre {
            white-space: pre-line; 
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
''')

print_menu()

print('''
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
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fasta_temp:
            fasta_temp.write(input_data)

    elif input_type == "Fasta File":
        input_data = form["input_data"]
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fasta_temp:
            fasta_temp.write(input_data.file.read().decode("utf-8"))

    elif input_type == "AC number":
        input_file = acsearch(form["input_data"])
        with tempfile.NamedTemporaryFile(delete=False) as fasta_temp:
            fasta_temp.write(input_data.file.read().decode("utf-8"))

    elif input_type == "PDB ID":
        input_file = download_as_fasta(form["input_data"])
        with tempfile.NamedTemporaryFile(delete=False) as fasta_temp:
            fasta_temp.write(input_data.file.read().decode("utf-8"))

    command = ["java", "-jar", "predict.jar", "--model", model_file, "--format", "html", "--seq", fasta_temp.name]

    if with_probabilities:
        command.append("--probabilities")

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode == 0:
        html_file_path = "./output.html"
        # Dateiberechtigungen auf 755 setzen
        os.chmod(html_file_path, 0o755)
        with open(html_file_path, "r") as html_file:
            html_content = html_file.read()

        print("<div style='margin-left: 300px;' id=output-container>")
        print("<div id='result'>")
        print(html_content)
        print("</div>")
        print(f'<form action="{html_file_path}" method="get" download="output.html"><button type="submit">Download Output</button></form>')
        print('</div>')
    else:
        print("<p>Ein Fehler ist aufgetreten. Bitte checken Sie Ihre Eingabe.</p>")

#else:
    #print_gor_form()

print('''</div>
</body>
</html>''')