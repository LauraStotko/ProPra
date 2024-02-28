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
        # header
        if l.startswith('#'):
            continue
        columns = l.split('\t')
        #status is 15th column
        if len(columns) <= 15:
            continue
        if not columns[15].startswith('Complete Genome'):
            continue
        organism = columns[0]
        organism = organism.split("'")[0]
        for org in organisms:
            # search for regex in the organism names
            if re.search(org, organism):
                length = float(columns[6])
                genomes.append((organism, length))
                break
    return genomes

if __name__ == '__main__':

    pars = argparse.ArgumentParser(description="Search for completely sequenced genomes")
    pars.add_argument("--organism", help="Specify at least one organism to be searched for!", nargs='+')
    args = pars.parse_args()

    # link for the genome report
    report_url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"
    report = download_genomeReport(report_url)
    #if download was successfull
    if report:
        # Search the Genome report for the specified organisms
        search_results = search_genome(report, args.organism)
        # print the name of the organism and the genome length in Mb
        for organism, length in search_results:
            print(f"{organism}\t{length}")
