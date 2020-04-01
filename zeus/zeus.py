"""
Run fastqc on reads
"""
import sys
import subprocess

import os

RESULTS = "zeus_ouput/"

def run_fastqc(forward_read,reverse_reads):
    subprocess.run("fastqc {} {} -o {}".format(forward_read,reverse_reads,RESULTS),shell=True)

def run_spades(forward,reverse):
    command = ["spades.py","-1",forward,"-2",reverse,"--only-assembler","-o",RESULTS+"spades_output"]
    subprocess.run(command)

def run_pipline(forward,reverse):
    '''
    Example:

    SRA23433_1.fastq
    SRA32434_2.fastq

    Command structure:
    trimmomatic PE  SRA23433_1.fastq SRA23433_2.fastq
    SRA23433_1_paired.fastq SRA23433_1_unpaired.fastq
    SRA23433_2_paired.fastq SRA23433_2_unpaired.fastq
    LEADING:10 TRAILING:10 SLIDINGWINDOW:5:20

    Results of trimmomatic:
    SRA23433_1_paired.fastq SRA23433_1_unpaired.fastq
    SRA23433_2_paired.fastq SRA23433_2_unpaired.fastq

    '''

    if '/' in forward or '/' in reverse:
        index = len(forward)-forward[::-1].find('/')
        result_forward = forward[index:]
        result_reverse = reverse[index:]

    result_forward_paired = forward.replace(".","_paired.")
    result_forward_unpaired = forward.replace(".","_unpaired.")

    result_reverse_paired = reverse.replace(".","_paired.")
    result_reverse_unpaired = reverse.replace(".","_unpaired.")

    command = ["trimmomatic","PE",
               forward,reverse,
               result_forward_paired,result_forward_unpaired,
               result_reverse_paired,result_reverse_unpaired,
               "LEADING:10","TRAILING:10","SLIDINGWINDOW:5:20"]

    subprocess.run(command)
    run_fastqc(result_forward_paired,result_reverse_paired)
    run_spades(result_forward_paired,result_reverse_paired)


if not os.path.isdir(RESULTS):
    os.mkdir(RESULTS)

forward,reverse = sys.argv[1:]

#trim reads
run_pipline(forward,reverse)

