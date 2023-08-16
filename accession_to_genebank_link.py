#!/usr/bin/env python3

import argparse
import subprocess
import csv

def convert_ftp_link(ftp_link):
    https_link = ftp_link.replace('ftp://', 'https://')
    filename_id = https_link.split('/')[-1]
    download_link = f'{https_link}/{filename_id}_genomic.fna.gz'
    return download_link

def get_ftp_link_from_accession(accession):
    command = f'esearch -db assembly -query "{accession}" | esummary | xtract -pattern DocumentSummary -element FtpPath_GenBank'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return process.communicate()[0].decode().strip()

def main(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        csv_writer = csv.writer(f_out, delimiter='\t')
        csv_writer.writerow(['Accession', 'Link'])
        for line in f_in:
            accession = line.strip()
            ftp_link = get_ftp_link_from_accession(accession)
            https_link = convert_ftp_link(ftp_link)
            csv_writer.writerow([accession, https_link])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Accession list to FTP links.')
    parser.add_argument('-i', '--input', required=True, help='Input file containing accession list.')
    parser.add_argument('-o', '--output', default='results.tsv', help='Output file to store results.')

    args = parser.parse_args()
    main(args.input, args.output)

