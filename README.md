# Transcription Factor Mutation Tool

## Overview

This Python tool facilitates the generation of mutations in transcription factor (TF) sequences. It enables users to provide custom inputs for mutating specific amino acids in the intrinsically disordered region (IDR) of a TF sequence without changing its DNA binding domain (DBD) region, and outputs a new CSV file containing the resulting mutated sequences. Additionally, it includes advanced mutation generation methods, such as the **shift** and **convert method**.

## Features

- Accepts a CSV file containing:
  - The TF's name.
  - The TF's amino acid sequence.
  - the TF's DBD amino acids sequence.
  - The TF's DNA sequence.
  - The TF's DBD DNA sequence.
- Allows users to specify:
  - The amino acids to mutate in the IDR.
- Provides special mutation methods, including:
  - **Convert Method**: Converts all the appearances of the requested amino acids to a different amino acid. The codon of the target amino acid is decided by the most common codon of that amino acid in this TF.
  - **Shift Method**: Moves specified amino acids in the TF sequence one base upstream or downstream (randomly).
- Outputs a new CSV file with the mutated TF sequences.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rotemberda/Transcription-Factor-Mutation-generator.git
   cd Transcription-Factor-Mutation-generator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following arguments:

```bash
python TF_mutation_generator.py --input_csv <input_file> \
    --mutation_targets <amino_acids_to_mutate> --method <mutation_method> \
    [--mutate_to <target_amino_acid>]
```

### Arguments

- `--input_csv` (required): Path to the input CSV file containing the transcription factor data.
- `--mutation_targets` (required): A string of amino acids to mutate.
- `--method` (required): Mutation method to apply. Options include:
  - `convert`: Applies the convert method to the specified amino acids.
  - `shift`: Applies the shift method to the specified amino acids.
- `--mutate_to` (optional): A string of a target amino acid. Required when applying the `convert` method.


### Example- Convert Method

#### Input CSV:

```csv
TF_name,protein_seq,protein_DBD_seq,DNA_seq,DNA_DBD_seq
example_tf1,AACDEFA*,FA,aaaaa1cccdddeeefffaaasss,fffaaa
example_tf2, AACDEFA*, FA, aaaaa1cccdddeeefffaaasss, fffaaa
```

#### Command:

```bash
python TF_mutation_generator.py --input_csv example.csv \
    --mutation_targets AC --method convert --mutate_to D
```

#### Output CSV: 'example_AC_to_D.csv'

```csv
TF_name,mutated_protein_seq,mutated_DNA_seq

example_tf1,DDDDEFA*,ddddddddddddeeefffaaasss

example_tf2,DDDDEFA*,ddddddddddddeeefffaaasss
```


### Example- Shift Method

The shift method takes a string of amino acids and, for each occurrence in the TF's IDR sequence, moves it one base upstream or downstream (randomly). This can introduce subtle positional changes in the sequence for advanced analysis.

#### Input CSV:

```csv
TF_name,protein_seq,protein_DBD_seq,DNA_seq,DNA_DBD_seq
example_tf1,AACDEFA*,FA,aaaaa1cccdddeeefffaaasss,fffaaa
example_tf2, AACDEFA*, FA, aaaaa1cccdddeeefffaaasss, fffaaa
```

#### Command:

```bash
python TF_mutation_generator.py --input_csv example.csv \
    --mutation_targets AC --method shift
```

#### Output CSV: 'example_AC_shift.csv'

```csv
TF_name,mutated_protein_seq,mutated_DNA_seq

example_tf1,ACADEFA*,aa1cccaaadddeeefffaaasss

example_tf2,ACADEFA*,aaacccaa1dddeeefffaaasss
```

## Testing
The tool includes a comprehensive test suite that verifies the core functionality and input validation of the mutation generator.

### Running Tests
To run the test suite:
```bash
pytest test_TF_mutation_generator.py
```

### Test Coverage
The test suite covers the following components:

1. Input Validation (`test_validate_inputs()`)
   - Command-line argument validation
   - File existence and format checking
   - Amino acid validation
   - Method validation
   - Required argument combinations
   - Case sensitivity handling

2. Data Loading (`test_load_data()`, `test_TF()`)
   - CSV file parsing
   - TF object creation
   - IDR (Intrinsically Disordered Region) identification
   - Sequence cleaning and array conversion
   - Whitespace handling

3. Core Mutation Methods
   - Convert method (`test_convert()`)
     - Amino acid conversion
     - DNA sequence updates
     - DBD preservation
   - Shift method (`test_shift()`)
     - Upstream and downstream shifts
     - Multiple amino acid handling
     - Random shift direction

4. Utility Functions
   - Most common codon identification (`test_most_common_codon()`)
   - Output file generation (`test_output()`)
     - CSV formatting
     - Data integrity
     - File handling

### Adding New Tests
When adding new functionality to the tool, please:

1. Create test cases in the existing test file
2. Follow the current naming convention: `test_functionname()`
3. Use descriptive test names that indicate the functionality being tested
4. Include test cases for both valid and invalid inputs
5. Mock external dependencies when necessary (see examples using `patch`)

## Acknowledgments

Thank you for using the Transcription Factor Mutation Tool! Feel free to reach out with any questions or feedback.

