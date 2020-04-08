'''
The annotate.py module contains functions that call external programs blastp,makeblastdb, and prodigal.
'''
import subprocess
import os


ZEUS_DIR = os.path.dirname(os.path.realpath(__file__))
NEW_DB = ZEUS_DIR+'/db/'
REFSEQ_DB = ZEUS_DIR+'/db/refdb/bacteria'
PRODIGAL_PROTEINS = 'predicted_proteins.faa'
PRODIGAL_GENES = 'predicted_genes.txt'


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


def annotate_proteins(genome,outdir,dbname=None,dbseqs=None):

    os.mkdir(outdir)
    run_prodigal(genome,outdir)

    if dbseqs and dbname:
        makeblastdb(dbname,dbseqs)
        run_blastp(outdir+PRODIGAL_PROTEINS,NEW_DB+dbname,outdir)


    else:
        run_blastp(outdir+PRODIGAL_PROTEINS,REFSEQ_DB,outdir)







