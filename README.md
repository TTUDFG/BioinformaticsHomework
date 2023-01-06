# BioinformaticsHomework
# CAP5510 - Bioinformatics Fall 2022,

# Programming Assignment

## Due date: 11 / 10 / 2022

## Upload your assignment on canvas as a tar-zip file.

## October 14, 2022

This is a programming assignment. The purpose is to gain experience on sequence
alignment. You can work in teams of up to three people (you can do it alone if you prefer).
In this homework, you will implement

1. Simulator for sequence generator
2. Simulator for sequence partitioning
3. Sequence assembler

The algorithms you need are available in my course slides atwww.cise.ufl.edu/~tamer/
teaching/fall2022/lectures(Slides 2). Below is a description of each of the three items
above.

Simulator for sequence generator. This program will generate a set of similar se-
quences as follows.
Input:

1. string:F 1 = input file name (this file contains one DNA sequence in FASTA format).
2. integer:k= number of sequences
3. real number:p= mutation probability in [0:1] interval
4. string:F 2 = output file name

Output: The program will outputknucleotide sequence in FASTA format. The first
sequence will be the input sequence. Nextk−1 sequences will be a copy of the first
sequence, but each nucleotide will be mutated as follows: (i) with probability 4p/5, replace
a mutant nucleotide with a randomly selected nucleotide. (ii) with probabilityp/5 delete
the nucleotide.


Simulator for sequence partitioning. This program will partition a set of sequences
in a given input file into small fragments as follows.
Input:

1. string:F 1 = input file name (this file will contain a set of DNA sequences in FASTA
    format).
2. integer:x= minimum fragment length
3. integer:y= maximum fragment length (x≤y)
4. integer:z= maximum ACCEPTABLE fragment length (x≤z≤y)
5. string:F 2 = output file name

Output:The program will read the sequences in the input file. This input file is the output
of the first program above. It will then partition each sequence into smaller fragments. The
length of each fragment is a random number in the range [x:y]. If the fragment length is
less than or equal toz, then you will write it in the output file. Otherwise, you will discard
that fragment. As you chop the sequences into small fragments, if there is a small piece
left with length less thanxat the end of the sequence, throw away that short fragment.
The output file will contain all fragments in FASTA format.

Sequence assembler. This program will assemble the fragments of sequences in a file
into one long sequence as follows.
Input:

1. string:F 1 = input file name (this file will contain DNA fragments in FASTA format)
2. integer:s= score for match (positive integer)
3. integer:r= penalty for replace (negative integer)
4. integer:g= penalty for delete/insert (negative integer)
5. string:F 2 = output file name

Output:The program will read the sequence fragments in the input file. This input file
is the output of the second program above. It will then combine fragments using a greedy
strategy as follows.

1. Align all fragmentsfiandfjwith each other using dovetail alignment and compute
    the alignment scorevi,j
2. Repeat
    (a) Merge the two fragmentsfiandfjwith the largest alignment scorevi,jinto a
       new fragmentf′, ifvi,j> 0
(b) Replacefiandfjwith the new fragmentf′and compute alignf′with all the
other fragments in the current set using dovetail alignment.
3. Until(one fragment is left in the set)OR(the largest alignment score is negative)
4. Write the longest fragment you assembled into output file in FASTA format.


Return. You will return your source code, executable, and a Readme file in a single
tar-zip file through Canvas. One submission per team is enough.

Final details.

- You can use any programming language. Make sure that the program runs on CISE
    linux machine. You can find the list of linux machines at CISE athttps://it.cise.
    ufl.edu/support/workstations/
- All three programsshould be your own implementation.Do NOT use existing
    code from online resources.
- Use the following names for the three programs abovehw-1, hw-2, hw-3, as the
    executable of your code. For example, a command line to partition a file (second
    program above) should look like
    > hw-2 inputfile 100 200 220 outputfile
    to partition the input into fragments of length between 100 and 150.
Here are some sample parameters you can use to test your code:
> hw-1 inputfile 10 0.005 outputfile
> hw-2 inputfile 100 200 220 outputfile
> hw-3 inputfile 1 -1 -3 outputfile


