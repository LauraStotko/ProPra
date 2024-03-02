#!/usr/bin/python3
import argparse
import mysql.connector

def write_fasta(sequences, path, source):
    path = f"{path}/{source}"
    with open(path, 'w') as f:
        for sequence_id, sequence in sequences.items():
                f.write(f">{sequence_id}\n{sequence}\n")
        f.close()

def get_sequences(ids, source):
    sequences = {}
    db = mysql.connector.connect(
        host="mysql2-ext.bio.ifi.lmu.de",
        user="bioprakt13",
        password="$1$S4kE4pw1$8ANT55zOf1nKHgoau9K0A0",
        database="bioprakt13"
    )
    cursor = db.cursor()

    query = '''
    SELECT s.header_id, s.sequence
    FROM Sequences s, has_ac_numbers h, Sources sc
    WHERE sc.name = %s
    AND sc.accession_nr = %s
    AND sc.source_id = h.source_id
    AND h.seq_id = s.seq_id
    '''

    for id in ids:
        parameter = (source, id)
        cursor.execute(query,parameter)

        #safe in dictionary
        for row in cursor.fetchall():
            header_id, sequence = row
            sequences[header_id] = sequence

    cursor.close()
    db.close()

    # alle Sequences, die mit der ID identifiziert sind
    return sequences


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Get Sequences from database")
    pars.add_argument("--id", type=str,help='Accession number', required=True)
    pars.add_argument("--source",type=str, help='Source name', required=True)
    pars.add_argument('--output', help='path to output file', required=False)
    # add other arguments
    args = pars.parse_args()

    sequences = get_sequences(args.id, args.source)

    if args.output:
        write_fasta(sequences, args.output, args.source)
    else:
        for header_id, sequence in sequences.items():
            print(f">{header_id}\n{sequence}\n")