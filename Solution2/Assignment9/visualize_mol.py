import argparse
import subprocess
import os
import json


def load_config():
    """Loads configuration"""
    with open('/home/h/heletych/public_html/config.json') as config_file:
        return json.load(config_file)


def get_pdb(pdb_id, output, config):
    pdb_command = f"/usr/bin/python3 {config['get_pdb_script']} --id {pdb_id} --output {output}"
    # Set shell=True to pass the command as a single string
    subprocess.run(pdb_command, shell=True)


def visualize_mol(pdb_output_path, pdb_id, colourized, html, config):
    if html:
        pdb_file_path = f'{pdb_output_path}/{pdb_id}.pdb'
        jsmol_html_content = f"""
        <!doctype html>
        <html>
                <title>JSmol Visualization</title>
        <head>
                <script type="text/javascript" src="{config['jsmol_path']}/JSmol.min.js"></script>

                <script type="text/javascript">
                var Info = {{
                    width: 500,
                    height: 500,
                    j2sPath: "{config['jsmol_path']}/j2s",
                    script: "load output/{pdb_id}.pdb;cartoon only; {'color structure;' if colourized else ''}"

                }};
                </script>
        </head>
        <body>
                <script type="text/javascript">
                  jmolApplet0 = Jmol.getApplet("jmolApplet0", Info);
                  Jmol.script(jmolApplet0, Info.script);
                </script>
        </body>
        </html>
        """
        print(jsmol_html_content)
        #html_file_path = f'{pdb_output_path}/{pdb_id}.html'
        #with open(html_file_path, 'w') as html_file:
        #    html_file.write(jsmol_html_content)
    else:
        pdb_file_path = f'{pdb_output_path}/{pdb_id}.pdb'
        jmol_command = f'load {pdb_file_path}; cartoon only;'
        if colourized:
            jmol_command += 'color structure;'

        #xvfb = subprocess.Popen(['Xvfb', ':4', '-screen', '0', '800x600x24'], stdout=subprocess.PIPE)
        command = f'java -jar "{config["jmol_jar_path"]}" -n -J "{jmol_command} write image pngj {pdb_output_path}/{pdb_id}.png;"'
        subprocess.run(command, shell=True)
        #xvfb.terminate()


def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Visualizes PDB-ID in Cartoon-Mode with JMol")
    parser.add_argument("--id", required=True, help="PDB-ID to be visualized.")
    parser.add_argument("--output",
                        help="Destination directory for the output file based on the PDB-ID and the chosen format.")
    parser.add_argument("--html", action='store_true',
                        help="html")  # action='store_true'
    parser.add_argument("--colourized", action='store_true',
                        help="If true, colorizes the secondary structures in the visualization.")
    args = parser.parse_args()

    get_pdb(args.id, args.output, config)
    visualize_mol(args.output, args.id, args.colourized, args.html, config)


if __name__ == "__main__":
    main()
