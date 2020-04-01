"""
Run fastqc on reads
"""
import sys
import subprocess

def run_fastqc(forward_read,reverse_reads):
    subprocess.run("fastqc {} {}".format(forward_read,reverse_reads),shell=True)

forward,reverse = sys.argv[1:]
