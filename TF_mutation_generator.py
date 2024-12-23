import numpy as np
from random import choice
import re
import csv
import argparse
import os.path
from collections import defaultdict    # for handeling count with dict

'''
left to do:
* write the output function
* write the main function
* write the testing program
* create a requirements.txt file
'''



def main():
    # validate and get the file name and methods
    args = validate_inputs()

    # load the data
    tf_list = load_data(args.input_csv)

    # 








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
        self.dna_idr = self.full_dna.replace(self.dna_dbd[:-3], "")
    
    def string_to_array(self):
    # convert the sequences to be arrays for easeir manipulation
        self.full_protein = np.array(list(self.full_protein))
        self.full_dna = np.array([self.full_dna[i:i+3] for i in range(0, len(self.full_dna), 3)])
        self.protein_idr = np.array(list(self.protein_idr))
        self.dna_idr = np.array([self.dna_idr[i:i+3] for i in range(0, len(self.dna_idr), 3)])
    
def validate_inputs():
    # setting the CLA and validating inputs eith argparse

    parser = argparse.ArgumentParser(description="This program mutates a transcription factor sequence based on specified criteria")
    parser.add_argument('--input_csv', help = 'Input file name', required= True, type = str)
    parser.add_argument('--mutation_targets', help = 'A string of amino acids to mutate', required= True, type = str)
    parser.add_argument("--mutate_to", help="A target amino acid to mutate into", type = str)
    parser.add_argument("--method", help="Mutation method to apply", type = str)

    # Parse the arguments
    args = parser.parse_args()

    # check if at least one of the mutation methods were provided
    if not (args.mutate_to or args.method):
        parser.error("At least one of --mutate_to or --method must be provided.")
    
    # check that the nutate_to has one amino acid to mutate to
    if args.mutate_to and len(args.mutate_to) != 1:
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
            tf = TF(name= row["TF_name"], full_protein= row["protein_seq"], protein_DBD= row["protein_DBD_seq"], full_DNA= row["DNA_seq"], DNA_DBD= row["DNA_DBD_seq"])
            tf_list.append(tf)
    
    return tf_list

    
def most_common_codon(tf, aa):
    # gets an amino acid and tf's sequence and returning the most common codon for that amino acid
    codons = defaultdict(int)

    # iterates over all the aa of the idr
    for index in range(len(tf.protein_idr)):
        if tf.protein_idr[index] != aa:    # not the amino acid we are looking for
            continue

        codons[tf.dna_idr[index]] += 1     # count the codon of the amino acid

    return max(codons, key = codons.get)   # return the most common codon


def aa_to_aa(tf, aa_to_mutate, aa_mutate_to):
    # mutate the amino acid to a different amino acid

    # craete a mask of all the places where the aa is found in the idr
    mask = np.isin(tf.protein_idr, aa_to_mutate)

    # mutate the protein
    tf.protein_idr[mask] = aa_mutate_to
    # mutate the dna based on the most frequent codon of that aa
    tf.dna_idr[mask] = most_common_codon(tf, aa_mutate_to)
    
    # succeeded in mutating the TF
    return True

def shift(tf, aa_to_shift):
    # gets the TF and which group of amino acids to apply the shift method on
    # and mutate the tf accordingly

    # initializing the move to 0
    move = 0

    # itirate over all AA by index
    for i in range(1, len(tf.protein_idr)):
        if move == 1:                       # to skip shifing twice
            move = 0
            continue

        if tf.protein_idr[i] in aa_to_shift:     # if encouter aa_to_shift, move it up/down stream
            move = choice([-1, 1])               # randomly decide where to shift

            # doing the shifting
            tf.protein_idr[i], tf.protein_idr[i + move] = tf.protein_idr[i + move], tf.protein_idr[i]
            tf.dna_idr[i], tf.dna_idr[i + move] = tf.dna_idr[i + move], tf.dna_idr[i]

            '''
            ## optional- check to see if creating clusters
            if re.search(fr'[{"".join(aa_to_shift)}]{{5,}}', "".join(tf.protein_idr.tolist())):
                # if created a cluster of hydrophobics, cancel the switch
                tf.protein_idr[i], tf.protein_idr[i + move] = tf.protein_idr[i + move], tf.protein_idr[i]
                tf.dna_idr[i], tf.dna_idr[i + move] = tf.dna_idr[i + move], tf.dna_idr[i]
            '''

    # succeeded in mutating the TF
    return True

def output(tf):
    # write a new file with the mutated TF and name it apropriatly
    ...



if __name__ == "__main__":
    main()