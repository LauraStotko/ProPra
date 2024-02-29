#!/usr/bin/python3
import cgi, cgitb, os
# Enable debugging
cgitb.enable()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Programmierpraktikum 2024</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #F4F4F4; }}
        #header {{ background-color: #4B6587; color: white; text-align: center; padding: 10px 0; }}
        #content {{ padding: 30px; }}
        .info {{ margin-bottom: 20px; background-color: #D1D8E0; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div id="header">
        <h1>Gruppe 13</h1>
    </div>
    <div id="content">
        <div class="info">
            <p><br>Bilic, Diana</br> <br>Dersch, Aurelia</br> <br>Heletych, Anna</br> <br>Stotko, Laura</br></p>
        </div>
    <div id="header">
        <h1>Unsere Betreuer</h1>
        <div class="info">
            <p><br>Prof Friedel</br> <br>Katharina Reinisch</br> <br>Samuel Klein</br></p>
        </div>
    </div>
    </div>
</body>
</html>
"""
print("Content-type:text/html\r\n\r\n")
print(HTML)
