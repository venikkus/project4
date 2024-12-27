def read_fasta(file_path):
    """
    Reads sequences from a file in FASTA format.

    :param file_path: Path to the FASTA file
    :return: List of tuples (identifier, sequence)
    """
    sequences = []
    with open(file_path, 'r') as f:
        header = None
        sequence = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:  # Save the previous sequence
                    sequences.append((header, sequence))
                header = line[1:]  # Protein identifier (without the ">" symbol)
                sequence = ""  # Start a new sequence
            else:
                sequence += line
        if header:  # Add the last sequence
            sequences.append((header, sequence))
    return sequences


def find_full_proteins(full_proteins_file, fragments_file, output_file):
    """
    Find full proteins containing fragments and save them to a file in FASTA format.

    :param full_proteins_file: Path to the file with full proteins (FASTA format)
    :param fragments_file: Path to the file with protein fragments (FASTA format)
    :param output_file: Path to the output file to save results
    """
    # Read data from the file with full proteins
    full_proteins = read_fasta(full_proteins_file)

    # Read data from the file with fragments
    fragments = read_fasta(fragments_file)

    # Create a set to store results
    matching_proteins = set()

    # Search for fragments in full proteins
    for _, fragment in fragments:
        for header, protein_sequence in full_proteins:
            if fragment in protein_sequence:  # If the fragment is found in the full protein
                matching_proteins.add((header, protein_sequence))

    # Write results to a file in FASTA format
    with open(output_file, "w") as f:
        for header, sequence in matching_proteins:
            f.write(f">{header}\n")
            f.write(f"{sequence}\n")

    print(f"Results have been saved to the file: {output_file}")


# Example usage
# Specify file paths
full_proteins_path = input("Write path to full proteins file: ")
# "augustus.whole.aa"
fragments_path = input("Write path to fragment file: ")
# "peptides.fa"
output_path = input("Write path to output file: ")
# "results.fasta"
find_full_proteins(full_proteins_path, fragments_path, output_path)