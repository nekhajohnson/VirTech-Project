"""
Run fastqc on reads
"""
import sys
import subprocess

import os

RESULTS = "vir_output/"

def run_fastqc(forward_read,reverse_read):
	subprocess.run("fastqc {} {} -o {}".format(forward_read,reverse_read,RESULTS),shell=True)

def run_spades(forward,reverse):
        command = ["spades.py","-1",forward,"-2",reverse,"--only-assembler","-o",RESULTS+"spades_output"]
        subprocess.run(command)


def run_pipeline(forward,reverse):
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

	if '/' in forward or '/' in reverse:
		index = len(forward)-forward[::-1].find('/')
		result_forward = forward[index:]
		result_reverse = reverse[index:]

	result_forward_paired = forward.replace(".","_paired.")
	result_forward_unpaired = forward.replace(".","_unpaired.")
	result_reverse_paired = reverse.replace(".","_paired.")
	result_reverse_unpaired = reverse.replace(".","_unpaired.")

	command = ["trimmomatic","PE",forward,reverse,result_forward_paired,result_forward_unpaired,result_reverse_paired,result_reverse_unpaired,"LEADING:10","TRAILING:10","SLIDINGWINDOW:5:20"]
	subprocess.run(command)
	run_fastqc(result_forward_paired,result_reverse_paired)
	run_spades(result_forward_paired,result_reverse_paired)

if not os.path.isdir(RESULTS):
	os.mkdir(RESULTS)

forward,reverse = sys.argv[1:]

#trim reads
run_pipeline(forward,reverse)
