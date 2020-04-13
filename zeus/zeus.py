#!/usr/bin/env python
"""
Zeus is a command line program that takes forward and reverse reads in fastq format. The reads are processed with trimmomatic and a quality reports are generated using FastQC. The paired reads from trimmomatic are used for spades.py assembly.

Author: Jessie Arce
"""
import sys
import argparse
import subprocess
import os

import annotate
import assemble

RESULTS_DIR = "zeus_ouput/"
ANNOTATE_DIR = RESULTS_DIR+"annos/"

def main():
    parser = argparse.ArgumentParser(description="Assembles and annotates genome given a set of proteins.")
    parser.add_argument("F",
                        type=str,
                        metavar="<forward reads>",
                        help="Forward reads in FastQ format."
                        )
    parser.add_argument("R",
                        type=str,
                        metavar="<reverse reads>",
                        help="Reverse reads in FastQ format."
                        )
    parser.add_argument("dbname",
                        type=str,
                        metavar="<database name>",
                        help="Name for the blast databse.")

    parser.add_argument("dbseqs",
                        type=str,
                        metavar="<database sequences>",
                        help="Set of reference proteins.")

    args = parser.parse_args()


    assemble.assemble_genome(
        args.F,
        args.R,
        RESULTS_DIR
    )

    annotate.annotate_proteins(
        RESULTS_DIR+'spades_output/contigs.fasta',
        ANNOTATE_DIR,
        args.dbname,
        args.dbseqs
    )

if __name__ == "__main__":
    main()
