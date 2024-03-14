#!/usr/bin/python3

import cgi
import cgitb
import subprocess
import mysql.connector
from mysql.connector import Error

# Enable CGI traceback for debugging
cgitb.enable()

# Constants for the database connection
DB_HOST = 'mysql2-ext.bio.ifi.lmu.de'
DB_USER = 'bioprakt13'
DB_PASSWORD = '$1$S4kE4pw1$8ANT55zOf1nKHgoau9K0A0'
DB_NAME = 'bioprakt13'

# Paths
JAR_PATH = "./alignment.jar"
SEQLIB_PATH = "./homstrad.seqlib"
SECLIB_PATH = "./homstrad.seclib"
MATRIX_PATHS = {
    "blake_cohen": "./BlakeCohenMatrix.mat",
    "blosum62": "./blosum62.mat",
    "dayhoff": "./dayhoff.mat",
    "pam250": "./pam250.mat",
}


HTML_START = """
<!DOCTYPE html>
<html>
<head>
    <title>Family Alignment Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: white;
            font-size: 13px;
        }
        #header {
            background-color: #273f87;
            color: white;
            text-align: center;
            padding: 1.1em; /* Increased padding */
            font-size: 1.1em; /* Bigger header size */
        }
        #menu {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            background-color: #f1f1f1;
            padding: 20px;
            width: 220px; /* Fixed width for the menu */
            font-size: 1.1em; /* Bigger menu text */
        }
        #content {
            margin-left: 250px; /* Adjusted to menu width */
            padding: 1.8em;
            max-width: calc(100% - 250px); /* Adjusted to menu width */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            font-size: 1.1em; /* Bigger content text */
        }
        table {
            width: 100%;
            border-collapse: collapse; /* Added for table styling */
        }
        th, td {
            text-align: left;
            padding: 10px; /* Increased padding */
            font-size: 1.2em; /* Bigger table text */
        }
        input[type="text"], select, input[type="number"] {
            width: 100%; /* Full width */
            padding: 10px; /* Increased padding */
            margin-bottom: 0.7em; /* Space between inputs */
            font-size: 1.1em; /* Increased input text size */
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #273f87;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1.1em; /* Increased button text size */
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
         }
        .form-row { /* New class for a single row in the form */
        margin-bottom: 1.1em; /* Space between rows */
        }
        .label { /* New class for labels */
            display: block; /* Make labels block elements */
            margin-bottom: 0.7em; /* Space below labels */
        }
        .flex-row {
            display: flex;
            justify-content: space-between;
        }
        .flex-row .form-row {
            flex: 1; /* Both children will take up equal space */
            margin-right: 10px; /* Add some space between the inputs */
        }
        .flex-row .form-row:last-child {
         margin-right: 0; /* Remove margin from the last element */
        }
        .alignment-section {
            padding-left: 10px; /* Adjust as needed */
        }
        .alignment-sections {
            padding-left: 25px; /* Adjust as needed */
        }
        .alignment-header {
            margin-bottom: 5px;
            padding-left: 15px; /* Adjust as needed */
        }
        pre {
            white-space: pre-wrap; /* Ensure alignment results wrap */
            word-wrap: break-word;
            padding-left: 15px; /* Adjust as needed */
        }
    </style>        
<script>
function checkAlgorithm() {
    var algorithm = document.getElementById('algorithm').value;
    var displayStyle = (algorithm === 'gotoh') ? 'table-row' : 'none';
    document.getElementById('gotoh-gap-penalty').style.display = displayStyle;
}
window.onload = checkAlgorithm;
</script>  
        <script>
            function showInputOption() {
                var option = document.querySelector('input[name="input_option"]:checked').value;
                var pdbInputDiv = document.getElementById('pdbInput');
                var sequenceInputDiv = document.getElementById('sequenceInput');
                pdbInputDiv.style.display = 'none';
                sequenceInputDiv.style.display = 'none';

                if (option === 'pdb_id') {
                    pdbInputDiv.style.display = 'block';
                } else if (option === 'sequence') {
                    sequenceInputDiv.style.display = 'block';
                }
            }
            document.addEventListener('DOMContentLoaded', function() {
                showInputOption(); // Call this function to show the default input option when the page loads
            });
        </script>
        <script>
        function validateForm() {
            var inputType = document.querySelector('input[name="input_option"]:checked').value;
            if (inputType === 'pdb_id') {
                var pdbId = document.getElementById('pdb_id').value;
                if (!pdbId) {
                    alert('Please enter a PDB ID.');
                    return false;
                }
            } else if (inputType === 'sequence') {
                var sequence = document.getElementById('sequence').value;
                if (!sequence) {
                    alert('Please enter a sequence.');
                    return false;
                }
            }
            return true;
        }
        </script>
    </head>
    <body>
        <div id="header">
            <h1>Family Alignment Tool</h1>
        </div>
        <div id="menu" style="position: fixed; left: 0; top: 0; bottom: 0; background-color: #f1f1f1; padding: 20px;">
        <ul style="list-style-type:none; padding:0;">
            <li class="menu-item"><a href='./frontpage_cgi.py' style="font-size: 20px;">Start</a></li>
            <li class="menu-item"><a href='./git_cgi.py' style="font-size: 20px;">Git Anleitung</a></li>
            <li class="menu-item"><a href='./acsearch_cgi.py' style="font-size: 20px;">AC Search</a></li>
            <li class="menu item"><a href='./workflow_cgi.py' style="font-size: 20px;">Genome to ORF</a><li>
            <li class="menu-item"><a href='./gor_cgi.py' style="font-size: 20px;">GOR Algorithmus</a><li>
            <li class="menu-item"><a href='./alignment_cgi.py' style="font-size: 20px;">Alignment Tool</a><li>
            <li class="menu-item"><a href='./family_alignment.py' style="font-size: 20px;">Family Alignment Tool</a><li>
        </ul>
    </div>
    <b>Menu</b><br>
    <div id="content">
"""


HTML_FORM = """
<form name="input" action="./family_alignment.py" method="post" onsubmit="return validateForm()">
    <!-- CHANGED -->
    <div class="form-row">
        <input type="radio" id="pdb_option" name="input_option" value="pdb_id" onchange="showInputOption()" checked>
        <label for="pdb_option">PDB ID</label>
        <input type="radio" id="sequence_option" name="input_option" value="sequence" onchange="showInputOption()">
        <label for="sequence_option">Sequence</label>
    </div>
    <div id="pdbInput" style="display:none;">
        <div class="form-row">
            <label class="label" for="pdb_id">PDB ID (with or without chain):</label>
            <input type="text" id="pdb_id" name="pdb_id" placeholder="e.g. 1bgx or 1bgxt">
        </div>
    </div>
    <div id="sequenceInput" style="display:none;">
        <div class="form-row">
            <label class="label" for="sequence">Sequence:</label>
            <input type="text" id="sequence" name="sequence" placeholder="e.g. CSCSSLMDKECVYFCHLDIIW">
        </div>
    </div>
         <div class="form-row">
        <label class="label" for="algorithm">Alignment Algorithm:</label>
        <select id="algorithm" name="algorithm" onchange="checkAlgorithm()">
            <option value="needleman-wunsch">Needleman-Wunsch</option>
            <option value="gotoh">Gotoh</option>
            <!-- Other options -->
        </select>
    </div>
    <div class="form-row">
        <label class="label" for="alignment_type">Alignment Type:</label>
        <select id="alignment_type" name="alignment_type">
            <option value="global">Global</option>
            <option value="local">Local</option>
            <option value="freeshift">Freeshift</option>
        </select>
    </div>
       <div class="form-row">
        <label class="label" for="gap_penalty">Gap Penalty:</label>
        <input type="number" max="-5" min="-20" id="gap_penalty" name="gap_penalty" placeholder="Enter gap penalty">
    </div>
    <div class="form-row" id="gotoh-gap-penalty" style="display: none;">
        <label class="label" for="extension_penalty">Gotoh Extension Penalty:</label>
        <input type="number" max="-1" min="-5" id="extension_penalty" name="extension_penalty" placeholder="Enter gap extension penalty">
    </div>
    <div class="form-row">
    <input type="checkbox" id="secondary_structure" name="secondary_structure">
    <label for="secondary_structure">Include Secondary Structure</label>
    </div>
    <input type="submit" value="Submit">
</form>
"""

HTML_END = "</div>\n</body>\n</html>"

def read_sequences_file(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                sequences[key] = value
    return sequences

def connect_to_database():
    try:
        connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
        
def fetch_related_pdb_ids_and_chain(pdb_id, connection):
    cursor = connection.cursor()
    query = """
    SELECT pdb_id, COALESCE(chain, '') FROM Alignments WHERE a_id = (
        SELECT a_id FROM Alignments WHERE pdb_id = %s LIMIT 1
    )
    """
    cursor.execute(query, (pdb_id,))
    result = cursor.fetchall()
    cursor.close()
    return [f"{row[0]}{row[1]}" for row in result] if result else []


def fetch_family_name_and_chain(user_input, connection):
    pdb_id = user_input[:4].strip()
    chain = user_input[4:] if len(user_input) > 4 else None

    if not chain:
        # Fetch the first available chain for this PDB ID
        cursor = connection.cursor()
        chain_query = "SELECT MIN(chain) FROM Alignments WHERE pdb_id = %s"
        cursor.execute(chain_query, (pdb_id,))
        chain_result = cursor.fetchall()  # Using fetchall to ensure all results are consumed
        cursor.close()
        if chain_result and chain_result[0][0]:
            chain = chain_result[0][0]  # Use the first available chain
        else:
            chain = ''  # Handle case where no chain is found

    # Now proceed with the original query to fetch family name using the PDB ID with the first available chain
    cursor = connection.cursor()
    family_query = """
    SELECT h.family_name, COALESCE(a.chain, '') FROM Homestrad h
    JOIN Alignments a ON h.a_id = a.a_id
    WHERE a.pdb_id = %s AND (a.chain = %s OR %s = '')
    """
    cursor.execute(family_query, (pdb_id, chain, chain))
    result = cursor.fetchall()  # Using fetchall to ensure all results are consumed
    cursor.close()

    pdb_id_with_chain = f"{pdb_id}{chain}" if chain else pdb_id  # Ensure the ID and chain are correctly concatenated
    return (result[0][0], pdb_id_with_chain) if result else (None, pdb_id)


# Corrected function to run the alignment jar
def run_jar(algorithm, alignment_type, pdb_id1, pdb_id2, gap_extension_penalty, gap_penalty, sub_matrix, matrix_path, include_secondary_structure=False):
    command = [
        "java", "-jar", JAR_PATH,
        "--ge", gap_extension_penalty,
        "--go", gap_penalty,
        "--seqlib", SEQLIB_PATH,
        "-m", matrix_path,
        "--mode", alignment_type,
        "--pdbId1", pdb_id1,
        "--pdbId2", pdb_id2,
        "--format", "html",
    ]
    
    if include_secondary_structure:
        command.extend([
            "--seclib", "./homstrad.seclib",
            "--mSec", "./secstruc_matrix.txt"
        ])
    
    # Append the algorithm-specific parameter if necessary
    if algorithm == "needleman-wunsch":
        command.append("--nw")

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.stdout:
            return result.stdout
        else:
            print("Error or no output from alignment tool. Details:", result.stderr)  # Print error details
            return "No output from alignment tool."
    except subprocess.CalledProcessError as e:
        return f"Error executing jar: {e.stderr}"


def main():
    print("Content-type:text/html\r\n")
    form = cgi.FieldStorage()

    # Determine if the form has been submitted
    form_submitted = "input_option" in form

    if form_submitted:
        connection = connect_to_database()
        if not connection:
            print(HTML_START + "<h2>Error connecting to the database.</h2>" + HTML_END)
            return

        # Load sequences from the file
        sequences = read_sequences_file(SEQLIB_PATH)

        input_type = form.getvalue("input_option", "pdb_id")
        user_input = form.getvalue("pdb_id", "").strip() if input_type == "pdb_id" else form.getvalue("sequence", "").strip()

        pdb_id_with_chain = None

        if input_type == "sequence":
            # Search for the sequence in the loaded sequences
            found_pdb_id = None
            for pdb_id, sequence in sequences.items():
                if user_input in sequence:  # Assuming exact match is required
                    found_pdb_id = pdb_id
                    break

            if found_pdb_id is None:
                print(HTML_START + "<h2>Sequence not found in the database.</h2>" + HTML_END)
                return
            else:
                # Use the found PDB ID for the rest of the logic
                pdb_id_with_chain = found_pdb_id
        else:
            # Directly use the user-provided PDB ID if the input type is pdb_id
            pdb_id_with_chain = user_input

        if not pdb_id_with_chain:
            print(HTML_START + "<h2>Invalid input provided.</h2>" + HTML_END)
            return

        # Fetch family name and potentially modify pdb_id_with_chain if chain is not specified
        family_name, pdb_id_with_chain = fetch_family_name_and_chain(pdb_id_with_chain, connection)

        # Rest of the logic remains the same...

        # Adjust validation logic based on modified pdb_id_with_chain
        valid_input = pdb_id_with_chain in sequences or any(pdb_id_with_chain.startswith(pdb) for pdb in sequences)

        if valid_input:
            related_pdb_ids_with_chains = fetch_related_pdb_ids_and_chain(pdb_id_with_chain[:4], connection)

            algorithm = form.getvalue("algorithm", "needleman-wunsch")
            alignment_type = form.getvalue("alignment_type", "global")
            gap_penalty = form.getvalue("gap_penalty", "-1")
            gap_extension_penalty = form.getvalue("extension_penalty", "0")
            sub_matrix = form.getvalue("sub_matrix", "blosum62")
            matrix_path = MATRIX_PATHS.get(sub_matrix, MATRIX_PATHS["blosum62"])

            # Start of HTML output
            print(HTML_START)
            print(f"<div class='alignment-section'>")
            print(f"<h2>Family: {family_name}</h2>")
            print(f"<h3>Alignments for PDB ID: {pdb_id_with_chain}</h3>")
            
            include_secondary_structure = "secondary_structure" in form

            for related_pdb_id in related_pdb_ids_with_chains:
                if pdb_id_with_chain != related_pdb_id:
                    pdb_id_with_chain = pdb_id_with_chain.strip()
                    related_pdb_id = related_pdb_id.strip()
                    output = run_jar(algorithm, alignment_type, pdb_id_with_chain, related_pdb_id, gap_extension_penalty, gap_penalty, sub_matrix, matrix_path, include_secondary_structure)
                    print(f"<h4>Alignment between {pdb_id_with_chain} and {related_pdb_id}</h4>")
                    print(f"{output}")

            print(f"</div>")  # Close the alignment section
            print(HTML_END)  # End of HTML output

        else:
            # Display error message if the input is not valid
            error_message = "Error: PDB ID/Sequence not found in the database."
            print(HTML_START + f"<h2>{error_message}</h2>" + HTML_FORM + HTML_END)

    else:
        # Display the form initially and allow the user to select the input type
        print(HTML_START + HTML_FORM + HTML_END)

if __name__ == "__main__":
    main()
