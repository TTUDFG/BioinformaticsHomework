import random
import sys

string_F1 = sys.argv[1]
k = int(sys.argv[2])
p = float(sys.argv[3])
string_F2 = sys.argv[4]

with open(string_F1, 'r') as infile:
    line_list = []
    for idx, line in enumerate(infile):
        line_list.append(line)

original_sequence = ''

for idx, line in enumerate(line_list):
    if '>' in line:
        original_sequence = line_list[idx+1]

is_mutated = False

nucleotide_dict = {'A':1, 'C':2, 'G':3, 'T':4}
nucleotide_dict_reverse = {1:'A', 2:'C', 3:'G', 4:'T'}

new_nucleotide = ''
# Mutation section
for sequence_number in range(k):
    # decise if the letter mutate or not
    deletion_sequence_index = []
    replacement_sequence_dict = {}
    for idx, nucleotide in enumerate(original_sequence):
        mutation_decision = random.random()
        if mutation_decision < p:

            # letter is mutated, decise if it is being deleted or replaced
            deleted_decision = random.random()
            # replacement probability is 4p/5, deletion probability is p/5
            # replacement:deletion = 4:1 -> deletion probability is 20%
            if deleted_decision < 0.2:
                # letter will be deleted
                deletion_sequence_index.append(idx)
#                 print(deletion_sequence_index)
            else:
                # letter will be replaced
                # now, we will get the replacement nucleotide
                new_nucleotide_idx = nucleotide_dict[nucleotide]
                while new_nucleotide_idx == nucleotide_dict[nucleotide]:
                    new_nucleotide_idx = random.randint(1, 4)
                new_nucleotide = nucleotide_dict_reverse[new_nucleotide_idx]
                replacement_sequence_dict[idx] = new_nucleotide
#                 print(replacement_sequence_dict)

    # generate mutated sequence
    mutated_sequence = ''
    for idx, nucleotide in enumerate(original_sequence):
        if idx in deletion_sequence_index:
            pass
        elif idx in replacement_sequence_dict:
            mutated_sequence += new_nucleotide
        else:
            mutated_sequence += nucleotide
    outfile = open(string_F2, 'a')
    outfile.write('>mutated sequence number: %s\n' % sequence_number)
    outfile.write(mutated_sequence)
    outfile.write('\n')
    outfile.close()
