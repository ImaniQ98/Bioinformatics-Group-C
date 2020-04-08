#!/usr/bin/env python
"""
Zeus is a command line program that takes forward and reverse reads in fastq format. The reads are processed with trimmomatic and a quality reports are generated using FastQC. The paired reads from trimmomatic are used for spades.py assembly.

Author: Jessie Arce
"""
import sys
import subprocess
import os

import annotate
import assemble

RESULTS_DIR = "zeus_ouput/"
ANNOTATE_DIR = RESULTS_DIR+"annos/"

def main():
        num_args = len(sys.argv[1:])
        if num_args == 4:
            forward_reads,reverse_reads,dbname,dbseqs = sys.argv[1:]
        else:
            print("useage: zeus.py <forward_reads> <reverse_reads> <dbname> <dbseqs>")
            exit()

        assemble.assemble_genome(
            forward_reads,
            reverse_reads,
            RESULTS_DIR
        )

        annotate.annotate_proteins(
            RESULTS_DIR+'spades_output/contigs.fasta',
            ANNOTATE_DIR,
            dbname,
            dbseqs
        )

if __name__ == "__main__":
    main()
