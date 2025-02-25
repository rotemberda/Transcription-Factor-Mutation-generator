import numpy as np
from random import choice
import csv, argparse, os.path
from collections import defaultdict    # for handeling count with dict



# all the representations of the amino acids
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

# the available methods
METHODS = ['convert', 'shift']


def main():
    # validate and get the file name and methods
    args = validate_inputs()

    # load the data
    tf_list = load_data(args.input_csv)

    # check which method to apply
    if args.method == "convert":
        output_file = args.input_csv[:-4] + "_" + args.mutation_targets + "_to_" + args.mutate_to +".csv"
        for tf in tf_list:
            convert(tf, args.mutation_targets, args.mutate_to)


    elif args.method == "shift":
        output_file = args.input_csv[:-4] + "_" + args.mutation_targets + "_" + args.method + ".csv"
        for tf in tf_list:
            shift(tf, args.mutation_targets)
        
    # create output
    output(tf_list, output_file)

class TF:
    # defining Transcription Factor class

    def __init__(self, name, full_protein, protein_DBD, full_DNA, DNA_DBD):
        self.name = name
        self.full_protein = full_protein
        self.protein_dbd = protein_DBD
        self.full_dna = full_DNA
        self.dna_dbd = DNA_DBD
    # automatically clean the dbd from the seq and setting IDRs seq
        self.clean_dbd()

    # convertin the seq from strings to arrays for easier editting
        self.string_to_array()
    
    def clean_dbd(self):
    # creat the idr sequence
        self.protein_idr = self.full_protein.replace(self.protein_dbd + "*", "")
        self.dna_idr = self.full_dna.replace(self.dna_dbd, "")[:-3]
    
    def string_to_array(self):
    # convert the sequences to be arrays for easeir manipulation
        self.full_protein = np.array(list(self.full_protein))
        self.full_dna = np.array([self.full_dna[i:i+3] for i in range(0, len(self.full_dna), 3)])
        self.protein_idr = np.array(list(self.protein_idr))
        self.dna_idr = np.array([self.dna_idr[i:i+3] for i in range(0, len(self.dna_idr), 3)])
    
    def assemble_mutated_sequence(self):
    # convert the idr back to a string and save the full mutated sequence
        self.mutated_protein = "".join(self.protein_idr.tolist()) + self.protein_dbd + "*"
        self.mutated_dna = "".join(self.dna_idr.tolist()) + self.dna_dbd + self.full_dna[-1]
        
    
def validate_inputs():
    # setting the CLA and validating inputs eith argparse

    parser = argparse.ArgumentParser(description="This program mutates a transcription factor sequence based on specified criteria")
    parser.add_argument('--input_csv', help = 'Input file name', required= True, type = str)
    parser.add_argument('--mutation_targets', help = 'A string of amino acids to mutate', required= True, type = str)
    parser.add_argument("--method", help="Mutation method to apply. Options: " + str(METHODS), required= True, choices=METHODS, type = str)
    parser.add_argument("--mutate_to", help="A target amino acid to mutate into", type = str)
    

    # parse the arguments
    args = parser.parse_args()

    # check if a target amino acid was provided if the convert method was applied
    if args.method == "convert" and not args.mutate_to:
        parser.error("A target amino acid must be specified with the 'convert' method.")
    
    # make sure the aminoacids are in uppercase format
    args.mutation_targets = args.mutation_targets.upper()
    args.mutate_to = args.mutate_to.upper() if args.method == "convert" else None

    # check that the mutation_targets indeed in the represent amino acids
    for aa in args.mutation_targets:
        if aa not in AMINO_ACIDS:
            parser.error(f"{aa} do not represent an amino acid.")

    # check that the mutate_to has one amino acid to mutate to
    if args.method == "convert" and (len(args.mutate_to) != 1 or (args.mutate_to not in AMINO_ACIDS)):
        parser.error("Usage: mutate_to argument needs to contain one character representing one amino acid.")

    # check if file exists
    filename = args.input_csv

    if not os.path.isfile(filename):
        exit(f"'{filename}' doesn't exists")

    # check if the file is a csv file
    if filename[-4:] != '.csv':
        exit(f"Usage: '{filename}' is not a .csv file")

    return args


def load_data(filename):
    # loads the TFs data from the file and returns a list of TFs

    # read the file
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        tf_list = []

        for row in reader:
            tf = TF(
                name= row["TF_name"].strip(),
                full_protein= row["protein_seq"].strip(),
                protein_DBD= row["protein_DBD_seq"].strip(),
                full_DNA= row["DNA_seq"].strip(),
                DNA_DBD= row["DNA_DBD_seq"].strip()
            )
            tf_list.append(tf)
    
    return tf_list

    
def most_common_codon(tf, aa):
    # gets an amino acid and tf's sequence and returning the most common codon for that amino acid
    codons = defaultdict(int)

    # iterates over all the aa of the idr
    for index in range(len(tf.full_protein)):
        if tf.full_protein[index] != aa:    # not the amino acid we are looking for
            continue

        codons[tf.full_dna[index]] += 1     # count the codon of the amino acid

    return max(codons, key = codons.get)   # return the most common codon


def convert(tf, aa_to_mutate, aa_mutate_to):
    #get a TF and mutate the amino acid to a different amino acid
    aa_to_mutate_list = list(aa_to_mutate)
    # craete a mask of all the places where the aa is found in the idr
    mask = np.isin(tf.protein_idr, aa_to_mutate_list)

    # mutate the protein
    tf.protein_idr[mask] = aa_mutate_to
    # mutate the dna based on the most frequent codon of that aa
    tf.dna_idr[mask] = most_common_codon(tf, aa_mutate_to)
    
    # assemble the full sequence
    tf.assemble_mutated_sequence()

    # succeeded in mutating the TF
    return True

def shift(tf, aa_to_shift):
    # gets a TF and which group of amino acids to apply the shift method on
    # and mutate the TF accordingly

    # initializing the move to 0
    move = 0
    mutated_protein = tf.protein_idr.copy()
    mutated_dna = tf.dna_idr.copy()

    # itirate over all AA by index
    for i in range(1, len(tf.protein_idr) - 1):
        if move == 1:                       # to skip shifing twice
            move = 0
            continue

        if tf.protein_idr[i] in aa_to_shift:     # if encouter aa_to_shift, move it up/down stream
            move = choice([-1, 1])               # randomly decide where to shift

            # doing the shifting
            mutated_protein[i], mutated_protein[i + move] = mutated_protein[i + move], mutated_protein[i]
            mutated_dna[i], mutated_dna[i + move] = mutated_dna[i + move], mutated_dna[i]

    
    tf.protein_idr = mutated_protein
    tf.dna_idr = mutated_dna
    # assemble the full sequence
    tf.assemble_mutated_sequence()

    # succeeded in mutating the TF
    return True


def output(tfs_list, output_file):
    # write a new file with the mutated TF and name it apropriatly

    # prepare a dict of the resulted mutations
    tfs_output = []
    for tf in tfs_list:
        tf_dict = {"TF_name": tf.name, "mutated_protein_seq": tf.mutated_protein, "mutated_DNA_seq": tf.mutated_dna}
        tfs_output.append(tf_dict)

    # create the output file
    with open(output_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames= list(tfs_output[0].keys()))

        writer.writeheader()
        writer.writerows(tfs_output)
    
    # print a messege that all had done
    print(output_file, "created successfully.")



if __name__ == "__main__":
    main()
