'''
The annotate.py module contains functions that call external programs blastp,makeblastdb, and prodigal.
'''
import subprocess
import os

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML


ZEUS_DIR = os.path.dirname(os.path.realpath(__file__))
PRODIGAL_PROTEINS = 'predicted_proteins.faa'
PRODIGAL_GENES = 'predicted_genes.txt'

#Directory to hold blast database
NEW_DB = ZEUS_DIR+'/db/'

def run_prodigal(genome,outdir):
    '''Run prodigal for gene prediction and protein translations.

    Argument:
     genome: genome/contig/scaffolds to use as input to prodigal.
             Default, value is the contigs returned from spades.
    Returns:
     Creates two files, predicited_genes.txt and predicted_proteins.faa.
    '''
    command = [
        'prodigal','-i',genome,'-o',outdir+PRODIGAL_GENES,
        '-a',outdir+PRODIGAL_PROTEINS
    ]

    subprocess.run(command)

def makeblastdb(dbname,dbseqs):
    '''Create blast database with makeblastdb command from blast+.

    Arguments:
     dbname: name for blast database
     dbseqs: name of file makeblastdb will use to build database.

    Returns:
     makeblastdb output files in the db directory
    '''
    command = [
        'makeblastdb','-hash_index','-in',dbseqs,'-dbtype','prot',
        '-title',dbname,'-out',NEW_DB+dbname
    ]

    subprocess.run(command)

def run_blastp(query,dbname,outdir):
    '''Run blastp command. The query is predicted proteins or other proteins and the database
       is the refseq database, unless a different database is supplied.

    Argument:
     query: protein set to search against blast database
     dbname: blast database name

    Returns:
     XML file of blast results.
    '''
    command = [
        "blastp","-db",dbname,"-query",query,
        '-evalue','1e-16','-max_target_seqs','2',
        '-out',outdir+"blast_results.xml","-outfmt","5"
    ]

    print("Running blastp..")
    subprocess.run(command)
    print("Done")

def seq_lookup_table(fasta_file):
    '''

    '''
    lookup_table = {}
    for record in SeqIO.parse(fasta_file,"fasta"):
        lookup_table[record.id] = record.seq
    return lookup_table

def go_through(blast_record):
    '''

    '''
    prot_functions = []
    for alignment in blast_record.alignments:
        title = alignment.title
        index = title.find("sp") if "sp" in title else 0
        prot_function = title[title.find(" ",index):title.find('OS')]
        prot_functions.append(prot_function)
    return prot_functions

def hits_from_blast_results(result_file):
    '''

    '''
    with open(result_file) as blast_file:
        blast_records = NCBIXML.parse(blast_file)

        hits = {}
        for blast_record in blast_records:
            query = blast_record.query
            query = query[:query.find("#")].strip(" ")
            protein_functions = go_through(blast_record)
            if protein_functions:
                hits[query] = protein_functions[0]
    return hits

def label_proteins(predicted_proteins_file,blast_result_file,outfile):
    lookup_table = seq_lookup_table(predicted_proteins_file)
    hits = hits_from_blast_results(blast_result_file)

    annotations = []
    for i,item in enumerate(hits.items()):
        fasta_id,predicted_function = item
        seq = lookup_table[fasta_id]
        new_record = SeqRecord(
            id="zeus{}".format(i),
            description="zeus{} {}".format(i,predicted_function),
            seq=seq
        )
        annotations.append(new_record)
    SeqIO.write(annotations,outfile,"fasta")





def annotate_proteins(genome,outdir,dbname,dbseqs):

    if not os.path.isdir(NEW_DB):
        os.mkdir(NEW_DB)

    os.mkdir(outdir)
    run_prodigal(genome,outdir)
    makeblastdb(dbname,dbseqs)
    run_blastp(outdir+PRODIGAL_PROTEINS,NEW_DB+dbname,outdir)
    label_proteins(outdir+PRODIGAL_PROTEINS,
                   outdir+"blast_results.xml",
                   outdir+"zeus_annotations.faa"
                   )







