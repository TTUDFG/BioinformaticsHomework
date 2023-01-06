import sys
import numpy as np

string_F1 = sys.argv[1]
s = int(sys.argv[2])
r = int(sys.argv[3])
g = int(sys.argv[4])
string_F2 = sys.argv[5]


def dovetail_alignment(sequence1, sequence2):
    DP_matrix = np.empty((len(sequence2)+1,len(sequence1)+1,))
    DP_matrix[:] = np.nan
    # Gap has no penalty for first row (sequence1)
    for j in range(len(sequence1)+1):
        DP_matrix[0][j] = 0
    # Gap has no penalty for first column (sequence2)
    for i in range(len(sequence2)+1):
        DP_matrix[i][0] = 0

    # start filling DP_matrix with s, r and g
    for row_idx, row_element in enumerate(DP_matrix):
        for col_idx, col_element in enumerate(row_element):
            if row_idx != 0 and col_idx != 0:
                # check if the two sequences letter matches
                if sequence1[col_idx-1] == sequence2[row_idx-1]:
                    score = max(DP_matrix[row_idx-1][col_idx-1] + s, DP_matrix[row_idx][col_idx-1] + g, DP_matrix[row_idx-1][col_idx] + g)
                else:
                    score = max(DP_matrix[row_idx-1][col_idx-1] + r, DP_matrix[row_idx][col_idx-1] + g, DP_matrix[row_idx-1][col_idx] + g)
                DP_matrix[row_idx][col_idx] = score

    return DP_matrix


def get_dovetail_alignment_result_sequence(dovetail_matrix, sequence1, sequence2):
    alignment = ''
    columnmax_idx = np.argmax(dovetail_matrix[:,-1][1:])+1
    rowmax_idx = np.argmax(dovetail_matrix[-1][1:])+1
    columnmax = dovetail_matrix[:, -1][columnmax_idx]
    rowmax= dovetail_matrix[-1][rowmax_idx]
    if columnmax < 0 and rowmax < 0:
        return 'END'
    else:
        if columnmax > rowmax or columnmax == rowmax:
            alignment = sequence1 + sequence2[columnmax_idx:]
        else:
            alignment = sequence2 + sequence1[rowmax_idx:]
        return alignment


with open(string_F1, 'r') as infile:
    line_list = []
    for idx, line in enumerate(infile):
        line_list.append(line)

acceptable_sequence_idx_list = []
for idx, line in enumerate(line_list):
    if '>' in line:
        acceptable_sequence_idx_list.append(idx + 1)

acceptable_sequence_list = []
for idx, line in enumerate(line_list):
    if idx in acceptable_sequence_idx_list:
        acceptable_sequence_list.append(line_list[idx].replace('\n', ''))


# find fi and fj
max_score = float('-inf')
parents = [None, None]
removed_sequence_index = []
sequence_score_matrix = np.empty((len(acceptable_sequence_list),len(acceptable_sequence_list),))
sequence_score_matrix[:] = -np.inf

for i_idx, sequence in enumerate(acceptable_sequence_list):
    print('working on i_idx: %s' % i_idx)
    for j_idx, sequence in enumerate(acceptable_sequence_list):
        if i_idx < j_idx:
            DP_matrix = dovetail_alignment(acceptable_sequence_list[i_idx], acceptable_sequence_list[j_idx])
            new_score = max(DP_matrix[:, -1][np.argmax(DP_matrix[:, -1])], DP_matrix[-1][np.argmax(DP_matrix[-1])])
            sequence_score_matrix[i_idx][j_idx] = new_score
            # print(DP_matrix)
            if new_score > max_score:
                print('working on j_idx: %s' % j_idx)
                print('new_max_score: %s' % new_score)
                max_score = new_score
                new_merged_sequence = get_dovetail_alignment_result_sequence(DP_matrix,
                                                                             acceptable_sequence_list[i_idx],
                                                                             acceptable_sequence_list[j_idx])

                parents[0] = acceptable_sequence_list[i_idx]
                parents[1] = acceptable_sequence_list[j_idx]

print(sequence_score_matrix)

merged_sequence_count = 0
merged_sequence_score_list = np.array([])
merged_sequence_partner_list = []
remaining_seq = sequence_score_matrix.shape[0] - len(removed_sequence_index) + merged_sequence_count

# import sys
# np.set_printoptions(threshold=sys.maxsize)
# do while loop
while remaining_seq > 1:
    print('remaining_seq: %s' % remaining_seq)
    # get max entry row and column
    # if new merged sequences are created, take those into account
    if merged_sequence_score_list.any():
        print('-----------------------debug1')
        print('sequence_score_matrix:')
        print(sequence_score_matrix)
        print('merged_sequence_score_list')
        print(merged_sequence_score_list)
        # if max score envolve at least one new merged sequence
        print('np.amax(merged_sequence_score_list): %s' % np.amax(merged_sequence_score_list))
        print('np.amax(sequence_score_matrix): %s' % np.amax(sequence_score_matrix))

        partner_row_index = np.argmax(merged_sequence_score_list)//sequence_score_matrix.shape[0]
        row_index = partner_row_index + sequence_score_matrix.shape[0]
        col_index = merged_sequence_partner_list[partner_row_index][np.argmax(merged_sequence_score_list)%sequence_score_matrix.shape[0]]
        print('np.argmax(merged_sequence_score_list): %s' % np.argmax(merged_sequence_score_list))
        print('row_index: %s' % row_index)
        print('col_index: %s' % col_index)
        get_merged_seq_index = row_index - sequence_score_matrix.shape[0]
        print('get_merged_seq_index: %s' % get_merged_seq_index)
        for increment in range(sequence_score_matrix.shape[0]):
            merged_sequence_score_list[sequence_score_matrix.shape[0]*get_merged_seq_index+increment] = -np.inf

        if col_index+1 > sequence_score_matrix.shape[0]:
            get_merged_seq_index = col_index - sequence_score_matrix.shape[0]
            print('get_merged_seq_index: %s' % get_merged_seq_index)
            for increment in range(sequence_score_matrix.shape[0]):
                merged_sequence_score_list[sequence_score_matrix.shape[0]*get_merged_seq_index+increment] = -np.inf
        else:
            sequence_score_matrix[col_index] = -np.inf
            sequence_score_matrix[:, col_index] = -np.inf
        print('sequence_score_matrix:')
        print(sequence_score_matrix)
        print('merged_sequence_score_list')
        print(merged_sequence_score_list)

    else:
        print('-----------------------debug2')
        row_index = np.argmax(sequence_score_matrix)//sequence_score_matrix.shape[0]
        col_index = np.argmax(sequence_score_matrix)%sequence_score_matrix.shape[0]
        print('row_index: %s' % row_index)
        print('col_index: %s' % col_index)
        sequence_score_matrix[row_index] = -np.inf
        sequence_score_matrix[:, row_index] = -np.inf
        sequence_score_matrix[col_index] = -np.inf
        sequence_score_matrix[:, col_index] = -np.inf

    # row and column are also the two merging sequence indexes
    DP_matrix = dovetail_alignment(acceptable_sequence_list[row_index], acceptable_sequence_list[col_index])
    print(DP_matrix)
    new_merged_sequence = get_dovetail_alignment_result_sequence(DP_matrix,
                                                                 acceptable_sequence_list[row_index],
                                                                 acceptable_sequence_list[col_index])

    print('Parent 1: %s' % acceptable_sequence_list[row_index])
    print('Parent 2: %s' % acceptable_sequence_list[col_index])
    print('new_merged_sequence: %s' % new_merged_sequence)
    if new_merged_sequence == 'END':
        print('All values are negative while loop ends')
        break
    # remove those two parent sequences
    removed_sequence_index.append(row_index)
    removed_sequence_index.append(col_index)

    # add new merged sequence for comparison
    acceptable_sequence_list.append(new_merged_sequence)

    # get dovetail score for new merged sequence
    new_merged_sequence_list = []
    new_merged_sequence_partner_list = []
    for seq_idx, sequence in enumerate(acceptable_sequence_list):
        # sequence won't compare to removed sequences
        if seq_idx not in removed_sequence_index:
            # sequence won't compare to itself
            if seq_idx+1 != len(acceptable_sequence_list):
                DP_matrix = dovetail_alignment(new_merged_sequence, acceptable_sequence_list[seq_idx])
                new_score = max(DP_matrix[:, -1][np.argmax(DP_matrix[:, -1])], DP_matrix[-1][np.argmax(DP_matrix[-1])])
                new_merged_sequence_list.append(new_score)
                new_merged_sequence_partner_list.append(seq_idx)
                if new_score > max_score:
                    print('working on j_idx: %s' % j_idx)
                    print('new_max_score: %s' % new_score)
                    max_score = new_score
    if len(new_merged_sequence_list) < sequence_score_matrix.shape[0]:
        while len(new_merged_sequence_list) < sequence_score_matrix.shape[0]:
            new_merged_sequence_list.append(float('-inf'))
            new_merged_sequence_partner_list.append(None)
    merged_sequence_score_list = np.concatenate((merged_sequence_score_list, np.array(new_merged_sequence_list)), axis=0)
    merged_sequence_partner_list.append(new_merged_sequence_partner_list)
    merged_sequence_count = len(acceptable_sequence_list) - sequence_score_matrix.shape[0]
    remaining_seq = sequence_score_matrix.shape[0] - len(removed_sequence_index) + merged_sequence_count

if new_merged_sequence == 'END':
    lognest_fragment_length = 0
    longest_idx = -1
    for fragment_idx, fragment in enumerate(acceptable_sequence_list[sequence_score_matrix.shape[0]:]):
        if len(fragment) > lognest_fragment_length:
            longest_idx = fragment_idx
    final_fragment = acceptable_sequence_list[sequence_score_matrix.shape[0]:][longest_idx]
else:
    final_fragment = acceptable_sequence_list[-1]

outfile = open(string_F2, 'a')
outfile.write('>final assembled sequence\n')
outfile.write(final_fragment)
outfile.write('\n')
outfile.close()