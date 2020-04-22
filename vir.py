"""
Vir command line program
"""

import sys
import subprocess
import os


RESULTS_DIR = "virulent_output/"
FASTQC_DIR = RESULTS_DIR+"fastqc_report/"
DATABASE_DIR = RESULTS_DIR+"database_files/"


def run_fastqc(forward_reads,reverse_reads,outdir):
	os.mkdir(outdir)
	subprocess.run(["fastqc",forward_reads,reverse_reads,"-o",outdir])

def run_spades(forward_reads,reverse_reads):
        command = ["spades.py","-1",forward_reads,"-2",reverse_reads,"--only-assembler","-o",RESULTS_DIR+"spades_output"]
        subprocess.run(command)


def run_trimmomatic(forward_reads,reverse_reads,forward_paired_reads,forward_unpaired_reads,reverse_paired_reads,reverse_unpaired_reads):
	'''
	Example:
        SRR11535172_1.fastq
        SRR11535172_2.fastq

	Command structure:
        trimmomatic PE SRR11535172_1.fastq SRR11535172_2.fastq
        SRR11535172_1_paired.fastq SRR11535172_1_unpaired.fastq
        SRR11535172_2_paired.fastq SRR11535172_2_unpaired.fastq
        LEADING:10 TRAILING:10 SLIDINGWINDOW:5:20

	Result of trimmomatic:
        SRR11535172_1_paired.fastq SRR11535172_1_unpaired.fastq
        SRR11535172_2_paired.fastq SRR11535172_2_unpaired.fastq
	'''

	command = ["trimmomatic","PE",forward_reads,reverse_reads,forward_paired_reads,forward_unpaired_reads,reverse_paired_reads,reverse_unpaired_reads,"LEADING:10","TRAILING:10","SLIDINGWINDOW:5:20"]

	subprocess.run(command)


def run_prodigal():
	command = ['prodigal','-i','spades_output/contigs.fasta','-o','genes.txt','-a',RESULTS_DIR+'predicted_proteins.fasta']
	subprocess.run(command)

def makeblastdb(database_name=None,database_sequences=None):

	if not os.path.isdir(DATABASE_DIR):
		os.mkdir(DATABASE_DIR)

	if not database_name and not database_sequences:
		database_name="virproteins"
		database_sequences="refseq/virproteins.fasta"

	command = ["makeblastdb","-in",database_sequences,"-dbtype","prot","-title",database_name,"-out",DATABASE_DIR+database_name]

	subprocess.run(command)

#blast -db refseq/virproteins.fasta -query proteins.fasta -out blast_results.xml -outfmt 5
def blastp(database_name):
	print(" Running blastp.....")

	command = ["blastp","-db",DATABASE_DIR+database_name,"-query",RESULTS_DIR+'predicted_proteins.fasta',"-out","blast_results.xml","-outfmt","5"]

	subprocess.run(command)
	print("Done.")

def vir_pipeline(forward_reads,reverse_reads,database_name="virproteins",database_seqs="refseq/virproteins.fasta"):


	try:
		os.mkdir(RESULTS_DIR)
	except FileExistsError as error:
		print("Folder {} already exists.".format(RESULTS_DIR))
	else:

		base_Ffile = os.path.basename(forward_reads)
		base_Rfile = os.path.basename(reverse_reads)

		forward_paired = RESULTS_DIR+base_Ffile.replace(".","_paired.")
		forward_unpaired = RESULTS_DIR+base_Ffile.replace(".","_unpaired.")
		reverse_paired = RESULTS_DIR+base_Rfile.replace(".","_paired.")
		reverse_unpaired = RESULTS_DIR+base_Rfile.replace(".","_unpaired.")

		run_trimmomatic(forward_reads,reverse_reads,forward_paired,forward_unpaired,reverse_paired,reverse_unpaired)
		run_fastqc(forward_paired,reverse_paired,FASTQC_DIR)
		run_spades(forward_paired,reverse_paired)

		#out is located in spades_output/contigs.fasta
		#return predicted_proteins.fasta
		run_prodigal()

		#makeblastdb
		makeblastdb(database_name,database_seqs)

		#runblastp
		blastp(database_name)

def main():
	forward,reverse,database_name,database_seqs = sys.argv[1:]
	vir_pipeline(forward,reverse,database_name,database_seqs)

if __name__ == "__main__":
	main()

