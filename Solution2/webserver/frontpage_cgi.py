#!/usr/bin/python3
import cgi
import cgitb

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
    <title>Gruppe 13 - Bioinformatische Tools</title>
    <style>
        body {
            display: flex;
            align-items: center;
            margin: 0;
            padding: 0;
            background-color: #add8e6;
        }
        #content {
            text-align: center;
            padding: 20px;
            margin-left: 250px; 
        }
        .menu-item {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>''')

# Menüleiste einbinden
print_menu()

print('''<div id="content">
    <h1>Gruppe 13</h1>
    <h2>Projekt von: Bilic Diana, Dersch Aurelia, Heletych Anna, Stotko Laura</h2>
    <h3>Betreuer: Prof. Friedel, Katharina Reinisch, Samuel Klein</h3>
</div>
</body>
</html>''')