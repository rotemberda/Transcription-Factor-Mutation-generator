import pytest
from TF_mutation_generator import TF, validate_inputs, load_data, most_common_codon, convert, shift, output
from unittest.mock import patch
import csv, tempfile, sys
import numpy as np
from pathlib import Path



#csv loaded correctly
expected_tf1 = TF(name= "example_tf1", full_protein= "AACDEFA*", protein_DBD= "FA", full_DNA= "aaaaa1cccdddeeefffaaasss", DNA_DBD= "fffaaa")
# csv loaded with whitespaces
expected_tf2 = TF(name= "example_tf2", full_protein= "AACDEFA*", protein_DBD= "FA", full_DNA= "aaaaa1cccdddeeefffaaasss", DNA_DBD= "fffaaa")
expected_output = [expected_tf1, expected_tf2]

def test_validate_inputs():
    # mocking sys.argv to simulate command-line arguments

    # valid input
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.csv",
        "--mutation_targets", "aCD",
        "--method", "convert",
        "--mutate_to", "g"    # check for case-insensativity
    ]

    with patch.object(sys, "argv", test_args):
        args = validate_inputs()
        assert args.input_csv == "example.csv"
        assert args.mutation_targets == "ACD"
        assert args.method == "convert"
        assert args.mutate_to == "G"


    # missing file
    test_args = [
        "TF_mutation_generator.py",
        "--input_csv", "missing.csv",
        "--mutation_targets", "ACD",
        "--method", "convert",
        "--mutate_to", "G"
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()
    

    # non csv file
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.txt",
        "--mutation_targets", "ACD",
        "--method", "convert",
        "--mutate_to", "G"    
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()


    # invalid amino acid
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.csv",
        "--mutation_targets", "XCD",   # mutation_targets are not amino acid
        "--method", "convert",
        "--mutate_to", "G"    
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()

    
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.csv",
        "--mutation_targets", "ACD",   
        "--method", "convert",
        "--mutate_to", "X"     # mutate_to is not amino acid
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()


    # mutate_to is not length 1
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.csv",
        "--mutation_targets", "ACD",
        "--method", "convert",
        "--mutate_to", "GC"    
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()


    # using 'convert' method without mutate_to argument
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.txt",
        "--mutation_targets", "ACD",
        "--method", "convert"    
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()


    # no methods were given
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.csv",
        "--mutation_targets", "ACD"   
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()

    # the method isn't one of the provided methods
    test_args = [
        "TF_mutation_generator.py",  
        "--input_csv", "example.txt",
        "--mutation_targets", "ACD",
        "--method", "not_a_method"    
    ]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            validate_inputs()


def test_load_data():

    example_list = load_data("example.csv")

    assert len(example_list) == len(expected_output), "Length mismatch"
    for r, e in zip(example_list, expected_output):
        assert r.name == e.name
        assert (r.full_protein == e.full_protein).all(), "full protein mismatch"
        assert r.protein_dbd == e.protein_dbd, "protein DBD missmatch"
        assert (r.protein_idr == e.protein_idr).all(), "protein IDR missmatch"
        assert (r.full_dna == e.full_dna).all(), "full dna mismatch"
        assert r.dna_dbd == e.dna_dbd, "DNA DBA missmatch"
        assert (r.dna_idr == e.dna_idr).all(), "DNA IDR ,missmatch" 


def test_TF():

    # test the idr creation
    # testing the clean_dbd and string_to_array functions
    assert (expected_tf1.protein_idr == np.array(['A','A','C','D','E'])).all()
    assert (expected_tf1.dna_idr == np.array(['aaa','aa1','ccc','ddd','eee'])).all()


def test_most_common_codon():
    assert most_common_codon(expected_tf1, 'A') == 'aaa'


def test_convert():
    expected_tf3 = TF(name= "example_tf3", full_protein= "AACDCEFCA*", protein_DBD= "FCA", full_DNA= "aaaaa1cccdddcc2eeefffcccaaasss", DNA_DBD= "fffcccaaa")
    convert(expected_tf3, 'C', 'A')

    assert expected_tf3.mutated_protein == 'AAADAEFCA*'
    assert expected_tf3.mutated_dna == 'aaaaa1aaadddaaaeeefffcccaaasss'
    

def test_shift():
    expected_tf4 = TF(name= "example_tf4", full_protein= "AACDEDFA*", protein_DBD= "FA", full_DNA= "aaaaa1cccdddeeedddfffaaasss", DNA_DBD= "fffaaa")
    aa_to_shift = 'ADE'

    # mock randomness to always choose -1 (downstream shift)
    with patch("TF_mutation_generator.choice", return_value=-1):
        shift(expected_tf4, aa_to_shift)
    
    # expected results after shifting
    assert expected_tf4.mutated_protein == 'AADECDFA*'
    assert expected_tf4.mutated_dna == 'aa1aaadddeeecccdddfffaaasss'
    

    expected_tf5 = TF(name= "example_tf5", full_protein= "AACDEDFA*", protein_DBD= "FA", full_DNA= "aaaaa1cccdddeeedddfffaaasss", DNA_DBD= "fffaaa")
    aa_to_shift = 'ACE'
    
    # mock randomness to always choose 1 (upstream shift)
    with patch("TF_mutation_generator.choice", return_value=1):
        shift(expected_tf5, aa_to_shift)
    
    # expected results after shifting
    assert expected_tf5.mutated_protein == 'ACADDEFA*'
    assert expected_tf5.mutated_dna == 'aaacccaa1ddddddeeefffaaasss'


def test_output():

    # mock TF class
    class MockTF:
        def __init__(self, name, mutated_protein, mutated_dna):
            self.name = name
            self.mutated_protein = mutated_protein
            self.mutated_dna = mutated_dna

    # mock data
    tfs_list = [
        MockTF("TF1", "MUTATED_PROTEIN_1", "MUTATED_DNA_1"),
        MockTF("TF2", "MUTATED_PROTEIN_2", "MUTATED_DNA_2"),
    ]

    expected_output = [
        {"TF_name": "TF1", "mutated_protein_seq": "MUTATED_PROTEIN_1", "mutated_DNA_seq": "MUTATED_DNA_1"},
        {"TF_name": "TF2", "mutated_protein_seq": "MUTATED_PROTEIN_2", "mutated_DNA_seq": "MUTATED_DNA_2"},
    ]


    # create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file_path = temp_file.name

    try:
        # call the function
        output(tfs_list, temp_file_path)

        # validate the content of the file
        with open(temp_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            result = list(reader)

        # assert that the result matches the expected output
        assert result == expected_output

    finally:
        # clean up the temporary file
        Path(temp_file_path).unlink()
 