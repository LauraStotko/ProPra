#!/usr/bin/python3
import cgi
import cgitb
import subprocess
import tempfile

cgitb.enable()

def print_menu():
    print('''
        <div id="menu">
        <ul>
            <li class="menu-item"><a href='./frontpage_cgi.py'>Start</a></li>
            <li class="menu-item"><a href='./git_cgi.py'>Git Anleitung</a></li>
            <li class="menu-item"><a href='./acsearch_cgi.py'>AC Search</a></li>
            <li class="menu-item"><a href='./workflow_cgi.py'>Genome to ORF</a></li>
            <li class="menu-item"><a href='./trainingset_cgi.py'>Datasets</a></li>
            <li class="menu-item"><a href='./gor_cgi.py'>GOR Algorithm</a></li>
            <li class="menu-item"><a href='./gorExperts_cgi.py'>Expert GOR</a></li>
        </ul>
        </div>
        ''')
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
    <div id="form-container">
    
    </div>    
''')

print_menu()
