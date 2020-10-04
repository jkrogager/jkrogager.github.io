from os import system
from glob import glob

all_files = glob('CQ*.eps*')

for figure in all_files:
	output = '../images/'+figure.split('.')[0]+'.png'
	command = "convert -density 200 {0} -flatten {1}".format(figure, output)

	system(command)

