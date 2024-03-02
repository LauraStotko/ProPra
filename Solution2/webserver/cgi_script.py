#!/usr/bin/python3

import cgi
import cgitb
import get_pdb_alignments  # Assuming get_pdb_alignments is implemented correctly

cgitb.enable()

HTML_START = """
<html>
<head>
<title>PDB Alignment Viewer</title>
</head>
<body>
<div id="header" style="background-color:#b0c4de;text-align:center">
<h1 style="margin-bottom:0;">PDB Alignment Viewer</h1>
</div>
<div id="menu" style="background-color:#b4cdcd; height:100%;float:left;padding: 10px;">
<b>Menu</b><br>
<a href="./cgi_script.py">Query PDB Alignments</a><br>
</div>
<div id="content">
"""

HTML_FORM = """
<form name="input" action="./cgi_script.py" method="post">
    <table>
        <tr>
            <td align="right">PDB ID(s): </td>
            <td><input type="text" name="pdb_ids" placeholder="e.g. 1bgx or 1bgx,1xo1"/></td>
        </tr>
    </table>
    <input type="submit" value="Submit"/>
</form>
"""

HTML_END = "</div>\n</body>\n</html>"

form = cgi.FieldStorage()

print(HTML_START)

if "pdb_ids" in form:
    pdb_ids = form.getvalue("pdb_ids")
    pdb_id_list = [pdb_id.strip() for pdb_id in pdb_ids.split(',')]

    # Call the function to query PDB alignments
    output = get_pdb_alignments.get_pdb_alignments(pdb_id_list)

    # Check if the output is valid
    if output:
        print(output)
    else:
        print("<p>No alignments found.</p>")
else:
    print(HTML_FORM)

print(HTML_END)
