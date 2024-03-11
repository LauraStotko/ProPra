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
    <h1>Git-Anleitung</h1>
    <p style="font-weight: bold;">Folder Structure</p>
    <p>Our folder structure is designed to align with the organization of the submission server, promoting uniformity and clarity. Below is an overview of the main directories:</p>
    <ul style="text-align: left;">
        <li>Solution1/: Contains scripts related to tasks from Assignment Sheets 1.</li>
        <li>Solution2/: Contains scripts related to tasks from Assignment Sheets 2.</li>
        <li>Solution3/: Integrate your Alignment or GOR implementation here.</li>
        <li>additional_features/: For any additional features or experiments, create separate branches.</li>
    </ul>
    <p style="font-weight: bold;">Version Control</p>
    <p>We use Git for version control following these practices:</p>
    <ul style="text-align: left;">
        <li>The main branch reflects the submission-ready state.</li>
        <li>Create new branches for developing new features or experiments.</li>
    </ul>
</div>
</body>
</html>''')