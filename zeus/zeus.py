"""
Run fastqc on reads
"""
import sys
import subprocess

import os

RESULTS_DIR = "zeus_ouput/"
FASTQC_DIR = RESULTS_DIR+"fastqc_reports/"


def run_fastqc(forward_reads,reverse_reads,outdir):
    subprocess.run(["fastqc",forward_reads,reverse_reads,"-o",outdir]))

def run_spades(forward_reads,reverse_reads):
    command = ["spades.py","-1",forward_reads,"-2",reverse_reads,"--only-assembler","-o","spades_output"]
    subprocess.run(command)

def run_trimmomatic(forward_reads,reverse_reads,forward_paried_reads,forward_unpaired_reads,reverse_paired_reads,reverse_paired_reads):

    command = [
        "trimmomatic","PE",
        forward_reads,reverse_reads,
        forward_paired_reads,forward_unpaired_reads,
        reverse_paired_reads,reverse_unpaired_reads,
        "LEADING:10","TRAILING:10","SLIDINGWINDOW:5:20"
    ]

    subprocess.run(command)



forward,reverse = sys.argv[1:]
