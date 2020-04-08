import os
import subprocess

def run_fastqc(forward_reads,reverse_reads,outdir):
    """Runs FastQC on forward and reverse reads.

    Arguments:
     forward_reads: filename of forward reads
     reverse_reads: filename of reverse reads
     outdir: directory for FastQC quality reports.

    Result:
     FastQC quality reports.
    """
    resultdir = outdir+'fastqc_report/'
    os.mkdir(resultdir)
    subprocess.run(["fastqc",forward_reads,reverse_reads,"-o",resultdir])

def run_spades(forward_reads,reverse_reads,outdir):
    """Runs spade.py
    Arguments:
     forward_reads: filename of forward reads
     reverse_reads: filename of reverse reads

    Results:
     spades.py assembly in spades_output directory.
    """
    command = ["spades.py","-1",forward_reads,"-2",reverse_reads,"--only-assembler","-o",outdir+"spades_output"]
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

def assemble_genome(forward_reads,reverse_reads,outdir):

    try:
        os.mkdir(outdir)
    except FileExistsError as error:
        print("Folder {} already exists.".format(outdir))
    else:

        ##for trimmomatic results
        base_Ffile = os.path.basename(forward_reads)
        base_Rfile = os.path.basename(reverse_reads)

        forward_paired = outdir+base_Ffile.replace('.','_paried.')
        forward_unpaired = outdir+base_Ffile.replace('.','_unparied.')
        reverse_paired = outdir+base_Rfile.replace('.','_paried.')
        reverse_unpaired = outdir+base_Rfile.replace('.','_unparied.')

        #trimmomatic
        run_trimmomatic(
            forward_reads,reverse_reads,
            forward_paired,forward_unpaired,
            reverse_paired,reverse_unpaired
        )

        #FastQC
        run_fastqc(forward_paired,reverse_paired,outdir)
        #spades.py
        run_spades(forward_paired,reverse_paired,outdir)
