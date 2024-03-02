#!/usr/bin/python3
import cgi
import cgitb
import subprocess
import os

# Enable debugging
cgitb.enable()
cgitb.enable(display=0, logdir='/home/h/heletych')


def generate_html_form():
    """Generates and prints an HTML form for user input."""
    print("Content-Type: text/html\r\n\r\n")
    print("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDB Visualization</title>
    </head>
    <body>
        <h2>Submit a PDB ID for Visualization</h2>
        <form action="visualize_cgi.py" method="post">
            PDB ID: <input type="text" name="pdb_id" required>
            <input type="checkbox" name="colourized"> Colorize Structure<br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """)


def process_form_submission(form):
    """Processes the form submission and calls visualize_mol.py with the provided inputs."""
    pdb_id = form.getvalue('pdb_id', '')
    #pdb_id = '1bgxt'
    colourized = 'colourized' in form

    # Adjust the path to visualize_mol.py according to your setup
    script_path = '/home/h/heletych/public_html/visualize_mol.py'
    output_dir = "/home/h/heletych/public_html/output"

    # Construct and execute the command

    if colourized:
        cmd = ["/usr/bin/python3", script_path, "--id", pdb_id, "--output", output_dir, "--colourized", "--html"]
    else:
        cmd = ["/usr/bin/python3", script_path, "--id", pdb_id, "--output", output_dir, "--html"]
    result = subprocess.check_output(cmd)

    # Redirect or display a message after processing
    print("Content-Type: text/html\n")
    print(result.decode())
    #print(f"<html><body><p>Visualization for {pdb_id} has been processed.</p></body></html>")


def main():
    form = cgi.FieldStorage()

    if form.getvalue('pdb_id'):
        process_form_submission(form)
    else:
        generate_html_form()


if __name__ == "__main__":
    main()
