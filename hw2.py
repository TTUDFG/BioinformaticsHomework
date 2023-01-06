import random
import sys

string_F1 = sys.argv[1]
x = int(sys.argv[2])  # Minimum length
z = int(sys.argv[3])  # Acceptable length
y = int(sys.argv[4])  # Maximum length
string_F2 = sys.argv[5]
mutated_sequence = ''

with open(string_F1, 'r') as infile:
    line_list = []
    for idx, line in enumerate(infile):
        line_list.append(line)

mutated_sequence_idx_list = []
for idx, line in enumerate(line_list):
    if '>' in line:
        mutated_sequence_idx_list.append(idx + 1)

counter = 0
for idx, line in enumerate(line_list):
    if idx in mutated_sequence_idx_list:
        mutated_sequence = line_list[idx]
        # print(mutated_sequence)
        acceptable_sequence = []
        finish = False
        remained_sequence = ''
        cut_length = random.randint(x, y)


        def checklength(remained_sequence, cut_length):
            if len(remained_sequence) < cut_length:
                return False
            else:
                return True


        firstcheck = checklength(mutated_sequence, cut_length)
        while firstcheck:

            cut_sequence = mutated_sequence[0:cut_length - 1]
            if x <= cut_length <= z:
                acceptable_sequence.append(cut_sequence)
            remained_sequence = mutated_sequence[cut_length:]
            mutated_sequence = remained_sequence
            # print(len(mutated_sequence))
            cut_length = random.randint(x, y)
            firstcheck = checklength(remained_sequence, cut_length)
            # print(firstcheck)

        while not finish:
            if len(remained_sequence) < x or len(remained_sequence) > z:
                finish = True
            else:
                cut_length = random.randint(x, y)
                secondcheck = checklength(mutated_sequence, cut_length)
                while secondcheck:
                    cut_sequence = mutated_sequence[0:cut_length - 1]
                    if x <= cut_length <= z:
                        acceptable_sequence.append(cut_sequence)
                    remained_sequence = mutated_sequence[cut_length:]
                    cut_length = random.randint(x, y)
                    secondcheck = checklength(remained_sequence, cut_length)

        # print(acceptable_sequence)
        for individual_acceptable_sequence in acceptable_sequence:
            outfile = open(string_F2, 'a')
            outfile.write('>acceptable sequence number: %s\n' % counter)
            outfile.write(individual_acceptable_sequence)
            outfile.write('\n')
            outfile.close()
            counter += 1
