# Transcription Factor Mutation Tool

## Overview

This Python tool facilitates the generation of mutations in transcription factor (TF) sequences. It enables users to provide custom inputs for mutating specific amino acids in the intrinsically disordered region (IDR) of a TF sequence, and outputs a new CSV file containing the resulting mutated sequences. Additionally, it includes advanced mutation generation methods, such as the **shift method**.

## Features

- Accepts a CSV file containing:
  - The TF's amino acid sequence.
  - the TF's DBD + NLS amino acids sequence.
  - The TF's DNA sequence.
  - The TF's DBD + NLS DNA sequence.
- Allows users to specify:
  - The amino acids to mutate in the IDR.
  - The amino acids to which they should be mutated.
- Provides special mutation methods, including:
  - **Shift Method**: Moves specified amino acids in the TF sequence one base upstream or downstream (randomly).
- Outputs a new CSV file with the mutated TF sequences.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following arguments:

```bash
python mutate_tf.py --input_csv <input_file> \
    --mutate_from <amino_acids_to_mutate> --mutate_to <target_amino_acids> \
    [--method <mutation_method>]
```

### Arguments

- `--input_csv` (required): Path to the input CSV file containing the transcription factor data.
- `--mutate_from` (required): A string of amino acids to mutate.
- `--mutate_to` (optional): A string of target amino acids.
- `--method` (optional): Mutation method to apply. Options include:
  - `shift`: Applies the shift method to the specified amino acids.

### Example

#### Input CSV:

```csv
AminoAcidSequence,IDRAminoAcidSequence,IDRDNASequence,DNASequence
EQNARKHKQQ*,HKQQ,CACAAGCAGCAG,GAGCAGAACGCGAGAAAGCACAAGCAGCAGTAA
```

#### Command:

```bash
python mutate_tf.py --input_csv input.csv \
    --mutate_from MK --mutate_to LI
```

#### Output CSV:

```csv
AminoAcidSequence,DNASequence
EQNARIHKQQ*,GAACAGAACGCCAGAATCCACAAGCAACAGTAA
```

## Special Mutation Methods

### Shift Method

The shift method takes a string of amino acids and, for each occurrence in the TF's IDR sequence, moves it one base upstream or downstream (randomly). This can introduce subtle positional changes in the sequence for advanced analysis.

## Acknowledgments

Thank you for using the Transcription Factor Mutation Tool! Feel free to reach out with any questions or feedback.

