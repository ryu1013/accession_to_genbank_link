#!/usr/bin/env python3

import argparse
import subprocess
import csv
import requests

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        super().error(message)

def convert_ftp_link(ftp_link, file_format):
    https_link = ftp_link.replace('ftp://', 'https://')
    filename_id = https_link.split('/')[-1]
    
    format_map = {
        'fna': f'{https_link}/{filename_id}_genomic.fna.gz',
        'gff': f'{https_link}/{filename_id}_genomic.gff.gz',
        'gtf': f'{https_link}/{filename_id}_genomic.gtf.gz',
        'faa': f'{https_link}/{filename_id}_protein.faa.gz',
    }
    
    return format_map.get(file_format, 'Not Found')

def get_ftp_link_from_accession(accession):
    command = f'esearch -db assembly -query "{accession}" | esummary | xtract -pattern DocumentSummary -element FtpPath_GenBank'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    ftp_path = process.communicate()[0].decode().strip()
    return ftp_path if ftp_path else "Not Found"

def is_link_valid(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def main(input_file, output_file, file_format):
    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        csv_writer = csv.writer(f_out, delimiter='\t')
        csv_writer.writerow(['Accession', 'Link'])
        
        for line in f_in:
            accession = line.strip()
            ftp_link = get_ftp_link_from_accession(accession)
            if ftp_link == "Not Found":
                continue
            https_link = convert_ftp_link(ftp_link, file_format)
            if not is_link_valid(https_link):
                continue
            csv_writer.writerow([accession, https_link])

if __name__ == "__main__":
    parser = CustomArgumentParser(
        description='Convert Accession list to FTP links.', 
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Usage examples:\n"
               "./access_to_genbank_link.py -i accession_list.txt -f fna\n"
               "./access_to_genbank_link.py -i accession_list.txt -o genome_links.tsv -f fna"
    )
    parser.add_argument('-i', '--input', required=True, help='Input file containing accession list.')
    parser.add_argument('-o', '--output', default='results.tsv', help='Output file to store results.')
    parser.add_argument(
        '-f', '--format', 
        required=True, 
        choices=['fna', 'gff', 'gtf', 'faa'], 
        help='File format to be fetched. Options are:\n'
             'fna (FASTA Format DNA)\n'
             'gff (General feature format)\n'
             'gtf (General transfer format)\n'
             'faa (FASTA Format Amino Acids)',
        metavar="FORMAT"
    )
    args = parser.parse_args()
    main(args.input, args.output, args.format)
