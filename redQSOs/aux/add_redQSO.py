#!/usr/bin/python

###	add_redQSO.py v2.1
###
### Jens-Kristian Krogager
###   12 October 2013
###
### version 2.1
### generates a javascript object
### instead of a new .html page
### for every new addition.

from argparse import ArgumentParser
from os import system, path
from operator import itemgetter
import numpy as np
import datetime

def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--density", default=150, help="Conversion pixel density [default: 150]")
	parser.add_argument("-f", action="store_true",
			help="Force upload if target already exists in database.")
	parser.add_argument("input", type=str,
			help="Input file to upload to redQSO database.")
	
	verbosity = parser.add_mutually_exclusive_group()
	verbosity.add_argument("-v", "--verbose", action="store_true")
	verbosity.add_argument("-q", "--quiet", action="store_true")
	
	args = parser.parse_args()
	
	validate_input(args)
	
	output_image = convert(args)
	
	update_data_object(args)
	
	upload(output_image,args)

### End of Main Program
################################################################


def validate_input(args):
	if args.input.split('.')[-1] not in ['eps','ps']:
		print "\n [ERROR]  Input file is not .eps or .ps format. Please provide correct input spectrum!\n"
		exit()

	if not args.f:
		infile = args.input.split('/')[-1]
		if path.isfile('/Users/krogager/Sites/redQSOs/images/'+infile.split('.')[0]+'.png'):
			print "\n [WARNING]  File already exists in database. Sure you want to proceed?"
			proceed = raw_input(" (yes / no) : ")

			while proceed not in ['y','Y','yes','YES','Yes','n','N','no','NO','No']:
				print "\n\t Invalid input! Please answer yes (y) or no (n)!"
				proceed = raw_input(" (yes / no) : ")

			if proceed in ['y','Y','yes','YES','Yes']:
				pass

			elif proceed in ['n','N','no','NO','No']:
				exit()

def convert(args):
	infile = args.input.split('/')[-1]
	out_dir = '/Users/krogager/Sites/redQSOs/images/'
	#out_dir = '' #for testing

	if len(infile.split('.')) == 2:
		output = out_dir+infile.split('.')[0]+'.png'
		convert_cmd = "convert -density {0} {1} -flatten {2}".format(args.density,
																args.input, output)
		if args.verbose:
			print ""
			print convert_cmd
		exit_stat = system(convert_cmd)

	else:
		print "Is this output filename correct?  ", '.'.join(infile.split('.')[:-1])+'.png'
		prompt = raw_input(" (y/n)  : ")
		if prompt in ['y','Y','yes','YES','Yes']:
			output = out_dir+'.'.join(infile.split('.')[:-1])+'.png'
			convert_cmd = "convert -density {0} {1} -flatten {2}".format(args.density,
																	args.input, output)
			if args.verbose:
				print ""
				print convert_cmd
			exit_stat = system(convert_cmd)

		else:
			print "Please give the desired output name:"
			output = raw_input("Output filename : ")
			if output[:-4] == '.png':
				output = out_dir+output
				convert_cmd = "convert -density {0} {1} -flatten {2}".format(args.density,
																	args.input, output)
				if args.verbose:
					print ""
					print convert_cmd
				exit_stat = system(convert_cmd)

			else:
				output = out_dir+output+'.png'
				convert_cmd = "convert -density {0} {1} -flatten {2}".format(args.density,
																	args.input, output)
				if args.verbose:
					print ""
					print convert_cmd
				exit_stat = system(convert_cmd)


	if exit_stat ==0 and not args.quiet:
		print "\n [OK]  Successfully converted input to {}\n".format(output)

	elif exit_stat != 0:
		print "\n [ERROR]  Converting input file to .png failed! Check input file.\n"
		exit()

	else:
		pass

	### COPY input to ~/Sites/redQSOs/spectra/
	if args.verbose:
		print "cp {} /Users/krogager/Sites/redQSOs/spectra/.".format(args.input)
	system("cp {} /Users/krogager/Sites/redQSOs/spectra/.".format(args.input))

	return output


def update_data_object(args):
	import pickle as p
	from astLib import astCoords
	from glob import glob
	
	### ALL QSOs observed and added to the web:
	allQSOs = glob('/Users/krogager/Sites/redQSOs/images/*.png')
	observedQSOs = []
	for qso in allQSOs:
		name = qso.split('/')[-1].split('.')[0]
		observedQSOs.append(name)
	
	SDSS = p.load(open('/Users/krogager/Projects/redQSOs/OptNIR/SDSS_phot.p'))

	metaData = np.genfromtxt('/Users/krogager/Projects/redQSOs/QSO_sampleData.txt', delimiter='\t',
			dtype={'names':['name', 'z', 'Ab', 'IR', 'BAL', 'nored', 'SMC', 'other',
						'noabs', 'narrow', 'strong', 'weak', 'intervening'],
			   'formats':['S11','f8','f8']+['i8' for i in range(10)]})
	
	
	js_out=[]
	for id,objID,ra,dec,type,u,e_u,g,e_g,r,e_r,i,e_i,z,e_z,specObjID,redshift,primTarget in SDSS:
		ra_hex = astCoords.decimal2hms(ra,':')
		dec_hex = astCoords.decimal2dms(dec,':')
		if id in observedQSOs:
			obs = 1
		else:
			obs = 0

		if id in metaData['name']:
			ij = metaData['name'].tolist().index(id)
			spec_z = metaData['z'][ij]
			Ab = metaData['Ab'][ij]
			BAL =   int(metaData['BAL'][ij])
			nored = int(metaData['nored'][ij])
			SMC =   int(metaData['SMC'][ij])
			other = int(metaData['other'][ij])
			noabs = int(metaData['noabs'][ij])
			narrow= int(metaData['narrow'][ij])
			strong= int(metaData['strong'][ij])
			weak =  int(metaData['weak'][ij])
			DLA =   int(metaData['intervening'][ij])
		else:
			spec_z = -1
			Ab = -1
			BAL = 0
			nored =0
			SMC = 0
			other =0
			noabs =0
			narrow=0
			strong=0
			weak = 0
			DLA = 0

		js_out.append("'%s': {id:%d, sid:%d, ra:%f, dec:%f, ra_hex:'%s', dec_hex:'%s', redshift:%s,\
u:%.2f, g:%.2f, r:%.2f, i:%.2f, z:%.2f, obs:%i, spec_z:%.2f, Ab:%.2f, BAL:%i,nored:%i,SMC:%i,other:%i,\
noabs:%i,narrow:%i,strong:%i,weak:%i,DLA:%i}" \
			%(id,objID,specObjID,ra,dec,ra_hex,dec_hex,redshift,u,g,r,i,z,obs,spec_z,Ab,BAL,nored,SMC,other,\
				noabs,narrow,strong,weak,DLA) )
	
	
	js = open('/Users/krogager/Sites/redQSOs/redQSOs_data.js','w')
	now = datetime.datetime.now()
	js.write("//Last update:\n")
	js.write("var last_update='"+now.strftime("%B %d %Y")+"';\n\n")
	
	js.write("var observedQSOs=['")
	js.write("','".join(observedQSOs))
	js.write("'];\n")
	
	js.write("\n")
	
	js.write("var redQSOs={\n")
	js.write(',\n'.join(js_out))
	js.write("};\n")
	js.close()

	if not args.quiet:
		print "\n [OK]  Successfully updated redQSOs_data.js \n"

def upload(img, args):
	if args.quiet:
		opt = '-q'
	else:
		opt = ''

	sync1 = "scp {} {} krogager@dark-cosmology.dk:~/Sites/redQSOs/images/.".format(opt,img)
	sync2 = "scp "+opt+" /Users/krogager/Sites/redQSOs/redQSOs_data.js krogager@dark-cosmology.dk:~/Sites/redQSOs/."
	
	if args.verbose:
		print ""
		print "  "+sync1
		print "\n\tUploading file:"
	exit1 = system(sync1)

	if exit1 == 0 and not args.quiet:
		print "\n [OK]  Successfully uploaded image to server\n"
	elif exit1 != 0:
		print "\n [ERROR] Connection to server refused. Check connection and VPN.\n"
		exit()
	else:
		pass


	if args.verbose:
		print ""
		print "  "+sync2
		print "\n\tUploading file:"
	exit2 = system(sync2)

	if exit2 == 0 and not args.quiet:
		print "\n [OK]  Successfully uploaded data.html to server\n"
	elif exit2 != 0:
		print "\n [ERROR] Connection to server refused. Check connection and VPN.\n"
		exit()
	else:
		pass


if __name__ == "__main__":
	main()
