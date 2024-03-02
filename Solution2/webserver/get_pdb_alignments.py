#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb

cgitb.enable()

HTML_START = """
<html>
<head>
<title>PDB Alignments</title>
</head>
<body>
<div id="header" style="background-color:#b0c4de;text-align:center">
<h1 style="margin-bottom:0;">PDB Alignment Viewer</h1>
</div>
<div id="content">
"""

HTML_END = "</div>\n</body>\n</html>"

form = cgi.FieldStorage()

DB_HOST = 'mysql2-ext.bio.ifi.lmu.de'
DB_USER = 'bioprakt13'
DB_PASSWORD = '$1$S4kE4pw1$8ANT55zOf1nKHgoau9K0A0'
DB_NAME = 'bioprakt13'

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def query_alignments_for_pdb_ids(pdb_id_list):
    """Queries the database for alignments related to the submitted PDB IDs."""
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            for pdb_id in pdb_id_list:
                alignments = get_alignments_for_pdb_id(cursor, pdb_id)
                print_alignment_results(alignments)
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error while querying database: {e}")

def get_alignments_for_pdb_id(cursor, pdb_id):
    """Queries the database for alignments related to a single PDB ID."""
    try:
        query = f"SELECT * FROM Alignments WHERE a_id = (SELECT a_id FROM Alignments WHERE pdb_id = '{pdb_id}')"
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error while querying database: {e}")
        return None

def print_alignment_results(alignments):
    """Prints alignment results."""
    if alignments:
        print("<h2>Alignments:</h2>")
        for alignment in alignments:
            aligned_sequence = alignment['aligned_sequence']  # Extracting the aligned_sequence value
            print(f"<p>{aligned_sequence}</p>")
    else:
        print("<p>No alignments found.</p>")

# Main script logic
print("Content-type:text/html\r\n\r\n")
print(HTML_START)

if "pdb_ids" in form:
    pdb_ids = form.getvalue("pdb_ids")
    pdb_id_list = [pdb_id.strip() for pdb_id in pdb_ids.split(',')]

    query_alignments_for_pdb_ids(pdb_id_list)
else:
    print("<p>Please enter one or two PDB IDs.</p>")

print(HTML_END)
