import re
import pandas as pd

def parse_blast_results(file_path):
    """
    Parse BLAST result file to extract the first alignment row under headers for each query block.
    If no alignments are found, record "No significant similarity found."

    :param file_path: Path to the BLAST result file
    :return: A DataFrame containing parsed BLAST results.
    """
    results = []
    current_query = None
    parsing_alignments = False
    no_hits = False

    # Updated regex pattern to capture `NA` correctly in `Common Name`
    alignment_pattern = re.compile(
        r"RecName: Full=(.+?)\s{2,}(.+?)(?:\.\.\. NA|(?:\s{2,}(NA|.+?)))\s{2,}(\d+|NA)\s+([\d.]+)\s+([\d.]+)\s+([\d.%]+)\s+([\deE.-]+)\s+([\d.]+)\s+(\d+)\s+(\S+)"
    )


    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Identify a new query block
            if line.startswith("Query #"):
                if current_query and no_hits:
                    results.append({
                        "Query": current_query,
                        "Description": "No significant similarity found",
                        "Scientific Name": "NA",
                        "Common Name": "NA",
                        "TaxID": "NA",
                        "Max Score": "NA",
                        "Total Score": "NA",
                        "Query Cover": "NA",
                        "E-value": "NA",
                        "Percent Identity": "NA",
                        "Alignment Length": "NA",
                        "Accession": "NA",
                    })
                current_query = re.match(r"Query #\d+: \S+", line).group(0)
                no_hits = True  # Assume no hits until proven otherwise

            # Detect the "Sequences producing significant alignments:" section
            elif line.startswith("Sequences producing significant alignments:"):
                parsing_alignments = True

            # Parse the first alignment row after the headers
            elif parsing_alignments and line.startswith("RecName: Full="):
                match = alignment_pattern.match(line)
                if match:
                    description = match.group(1).strip()
                    scientific_name = match.group(2).strip()
                    common_name = match.group(3).strip() if match.group(3) else "NA"
                    taxid = match.group(4).strip()
                    max_score = match.group(5).strip()
                    total_score = match.group(6).strip()
                    query_cover = match.group(7).strip()
                    e_value = match.group(8).strip()
                    percent_identity = match.group(9).strip()
                    alignment_length = match.group(10).strip()
                    accession = match.group(11).strip()

                    # Append result
                    results.append({
                        "Query": current_query,
                        "Description": description,
                        "Scientific Name": scientific_name,
                        "Common Name": common_name,
                        "TaxID": taxid,
                        "Max Score": max_score,
                        "Total Score": total_score,
                        "Query Cover": query_cover,
                        "E-value": e_value,
                        "Percent Identity": percent_identity,
                        "Alignment Length": alignment_length,
                        "Accession": accession,
                    })

                    parsing_alignments = False  # Only capture the first row
                    no_hits = False  # Hits found for this query

    # Handle the last query block
    if current_query and no_hits:
        results.append({
            "Query": current_query,
            "Description": "No significant similarity found",
            "Scientific Name": "NA",
            "Common Name": "NA",
            "TaxID": "NA",
            "Max Score": "NA",
            "Total Score": "NA",
            "Query Cover": "NA",
            "E-value": "NA",
            "Percent Identity": "NA",
            "Alignment Length": "NA",
            "Accession": "NA",
        })

    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    return df

# File path to your BLAST result file
blast_file_path = input("Enter the path to the BLAST result file: ")
# data/PXRD4D97013-Alignment.txt
output_csv_path = input("Enter the output CSV file path: ")
# data/PXRD4D97013-Alignment.txtbest_blast_matches.csv

df_results = parse_blast_results(blast_file_path)

# Save to CSV
df_results.to_csv(output_csv_path, index=False)

# Display results
print(f"Results saved to {output_csv_path}")
print(df_results)