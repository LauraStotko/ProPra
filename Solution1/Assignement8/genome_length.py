#!/usr/bin/python3
import argparse
import urllib.request
import re

def download_genomeReport(url):
    report = urllib.request.urlopen(url)
    return report.read()

def search_genome(report, organisms):
    genomes = []
    for l in report.decode().split('\n'):
        if l.startswith('#'):
            continue
        columns = l.split('\t')
        #status = 15th column
        if len(columns) > 15:
            if columns[15].startswith('Complete Genome'):
                organism = columns[0]
                for org in organisms:
                    if re.search(org, organism, re.IGNORECASE):
                        length = float(columns[6])
                        genomes.append((organism, length))
                        break
    return genomes

if __name__ == '__main__':

    pars = argparse.ArgumentParser(description="Search for completely sequenced genomes")
    pars.add_argument("--organism", help="Specify at least one organism to be searched for!", nargs='+')
    args = pars.parse_args()

    report_url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"
    report = download_genomeReport(report_url)
    if report:
        search_results = search_genome(report, args.organism)
        for organism, length in search_results:
            print(f"{organism}\t{length} Mb")
