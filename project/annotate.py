import sys
import subprocess
import os



REFSEQ_FILE = "refseqs/virproteins.fasta"
DATABASE_DIR = "blast_database/"
DATABASE_NAME = "virproteins"

#prodigal -i <contigs.fasta> -o <genes.txt> -a <proteins.fasta>
def run_prodigal(contig_file):
	command = ['prodigal','-i',contig_file,'-o','genes.txt','-a','proteins.fasta']

	subprocess.run(command)

#makeblastdb -in virproteins.fasta -dbtype "prot" -title "virproteins" -out "virproteins"
def makeblastdb():

	if not os.path.isdir(DATABASE_DIR):
		os.mkdir(DATABASE_DIR)

	command = ["makeblastdb","-in",REFSEQ_FILE,"-dbtype","prot","-title","virproteins","-out",DATABASE_DIR+DATABASE_NAME]
	
	subprocess.run(command)


#blast -db refseqs/virproteins.fasta -query proteins.fasta -out blast_results.xml -outfmt 5
def blastp():
	print(" Running blastp.....")

	command = ["blastp","-db",DATABASE_DIR+DATABASE_NAME,"-query",'proteins.fasta',"-out","blast_results.xml","-outfmt","5"]

	subprocess.run(command)
	print("Done.")

contigs = sys.argv[1]

run_prodigal(contigs)
makeblastdb()
blastp()
