"""
Zeus is a command line program that takes forward and reverse reads in fastq format. The reads are processed with trimmomatic and a quality reports are generated using FastQC. The paired reads from trimmomatic are used for spades.py assembly.

Author: Jessie Arce
"""
import sys
import subprocess
import os

RESULTS_DIR = "zeus_ouput/"
FASTQC_DIR = RESULTS_DIR+"fastqc_report/"


def run_fastqc(forward_reads,reverse_reads,outdir):
    """Runs FastQC on forward and reverse reads.

    Arguments:
     forward_reads: filename of forward reads
     reverse_reads: filename of reverse reads
     outdir: directory for FastQC quality reports.

    Result:
     FastQC quality reports.
    """
    os.mkdir(outdir)
    subprocess.run(["fastqc",forward_reads,reverse_reads,"-o",outdir])

def run_spades(forward_reads,reverse_reads):
    """Runs spade.py
    Arguments:
     forward_reads: filename of forward reads
     reverse_reads: filename of reverse reads

    Results:
     spades.py assembly in spades_output directory.
    """
    command = ["spades.py","-1",forward_reads,"-2",reverse_reads,"--only-assembler","-o",RESULTS_DIR+"spades_output"]
    subprocess.run(command)

def run_trimmomatic(forward_reads,reverse_reads,forward_paired_reads,forward_unpaired_reads,reverse_paired_reads,reverse_unpaired_reads):
    """
    Arguments:
     forward_reads: filename of forward reads
     reverse_reads: filename of reverse reads
     forward_paired_reads: trimmomatic result file for forward paired reads
     forward_unparied_reads: result file for forward unpaired reads
     reverse_paired_reads: result file for reverse paired reads
     reverse_paired_reads: result file for reverse unpaired reads

    Results:
     Four result files for forward and reverse reads both paired and unpaired.
    """

    command = [
        "trimmomatic","PE",
        forward_reads,reverse_reads,
        forward_paired_reads,forward_unpaired_reads,
        reverse_paired_reads,reverse_unpaired_reads,
        "LEADING:10","TRAILING:10","SLIDINGWINDOW:5:20"
    ]

    subprocess.run(command)

def zeus_pipline(forward_reads,reverse_reads):

    try:
        os.mkdir(RESULTS_DIR)
    except FileExistsError as error:
        print("Folder {} already exists.".format(RESULTS_DIR))
    else:

        ##for trimmomatic results
        base_Ffile = os.path.basename(forward_reads)
        base_Rfile = os.path.basename(reverse_reads)

        forward_paired = RESULTS_DIR+base_Ffile.replace('.','_paried.')
        forward_unpaired = RESULTS_DIR+base_Ffile.replace('.','_unparied.')
        reverse_paired = RESULTS_DIR+base_Rfile.replace('.','_paried.')
        reverse_unpaired = RESULTS_DIR+base_Rfile.replace('.','_unparied.')

        #trimmomatic
        run_trimmomatic(forward_reads,reverse_reads,forward_paired,forward_unpaired,reverse_paired,reverse_unpaired)
        #FastQC
        run_fastqc(forward_paired,reverse_paired,FASTQC_DIR)
        #spades.py
        run_spades(forward_paired,reverse_paired)

def main():
        forward,reverse = sys.argv[1:]
        zeus_pipline(forward,reverse)

if __name__ == "__main__":
    main()
