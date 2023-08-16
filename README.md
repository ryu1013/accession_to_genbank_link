# GenBank Accession to HTTPS Link Converter

This tool assists users by converting GenBank accession numbers into HTTPS links based on a specified file format, making data retrieval more streamlined.

## **Prerequisites**

- Python 3.x
- External Python Libraries: `requests` (needed for link verification)
- [Entrez Direct Utilities](https://www.ncbi.nlm.nih.gov/books/NBK179288/)

## **Setup & Installation**

1. Install the `requests` library, which is essential for link verification:

    ```bash
    pip install requests
    ```

2. Setup Entrez Direct Utilities following the guide from [NCBI's Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/).

3. Download accession_to_genbank_link.py

4. Make it executable (if you use it in linux):
   ```sh
   chmod +x accession_to_genbank_link.py
   ```

## **Usage**

```bash
./access_to_genbank_link.py -i INPUT_FILE -f FORMAT [-o OUTPUT_FILE]
```

Where:

- `INPUT_FILE`: Path to the file containing a list of accession numbers.
- `FORMAT`: Desired file format to retrieve. Options include:
  - `fna`: FASTA format for DNA sequences. Represents nucleotide sequences.
  - `gff`: General feature format, containing annotations and feature-related data.
  - `gtf`: General transfer format, a variant of GFF, typically used for gene annotations and exon structures.
  - `faa`: FASTA format for amino acids, detailing protein sequences corresponding to genes.
- `OUTPUT_FILE` (Optional): Designates the name of the output file. If not provided, defaults to `results.tsv`.

### **Examples**

Retrieve `fna` format links from a list of accession numbers:

```bash
./access_to_genbank_link.py -i accession_list.txt -f fna
```

With a custom output file:

```bash
./access_to_genbank_link.py -i accession_list.txt -o my_output.tsv -f fna
```

## **Features**

- **Custom Argument Parsing**: Enriched error messages with user-friendly help prompts.
- **FTP to HTTPS Conversion**: Transforms FTP links to their HTTPS equivalents for improved accessibility.
- **Link Verification**: Checks each link's validity using the `requests` library before committing to the output.

## **Disclaimer**

Ensure you have the necessary permissions to fetch and utilize data from GenBank. Always comply with NCBI's terms of service and usage guidelines.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcomed.
