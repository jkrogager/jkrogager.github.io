#!/usr/bin/python
from argparse import ArgumentParser
from os import system
from operator import itemgetter
import numpy as np
import datetime

def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--density", default=150)
	parser.add_argument("input", type=str,
			help="Input file to upload to redQSO database.")

	verbosity = parser.add_mutually_exclusive_group()
	verbosity.add_argument("-v", "--verbose", action="store_true")
	verbosity.add_argument("-q", "--quiet", action="store_true")

	args = parser.parse_args()

	output_image = convert(args)

	generate_html(args)

	upload(output_image,args)


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

	return output

	
def generate_html(args):
	from glob import glob
	"""Generating observed data webpage "data.html" from spectra located in source directory.
	"""

	path = '/Users/krogager/Sites/redQSOs/'
	specList = glob(path+'images/*.png')
	
	sdss = np.genfromtxt(path+'SDSS_redQSOs.csv', delimiter=',', missing_values='null',
			filling_values='-1', names=True, dtype="S13,i8,i8,f4,f4,f4,f4,f4,f4,f4,f4,i4")
	
	html = open(path+'data.html','w')
	#html = open('data.html','w') #for testing ONLY
	html.write("<!DOCTYPE html>\n")
	html.write("<html>\n")
	html.write("<head>\n")
	html.write("\t<title>Red Quasar Survey: Data</title>\n")

	### Style Options:	
	html.write("\t<style>\n")
	html.write("\thtml {font-family: Arial, Helvetica, sans-serif; color:#444;}\n")
	html.write("\ttd, th {padding:8px; vertical-align:top; border: 1px solid #DDD;\n")
	html.write("\t\tborder-collapse:collapse;}\n")
	html.write("\ttd {font-size:9pt;}\n")
	html.write("\tth {font-size:11pt;}\n")
	html.write("\th1 {text-align:center;}\n")
	html.write("\theader {text-align:center; padding:10px; border: 1px solid #CCC;\n")
	html.write("\t\tbackground:#EEE;}\n")
	html.write("\tnav {color:#777; word-spacing:50px; font-size:10pt; font-variant:small-caps;}\n")
	html.write("\ttable {border-collapse:collapse;}\n")
	html.write("\ttable.center {margin-left:auto; margin-right:auto;}\n")
	html.write("\t.date {font-size:8pt;color:#BBB;}\n")
	html.write("\t.credits {font-size:9pt;color:#555;}\n")
	html.write("\t</style>\n")
	html.write("</head>\n\n")
	
	### HTML BODY
	html.write("\t<body>\n")
	html.write("\t<header>\n")
	html.write("\t\t<h1>Red Quasars</h1>\n\n")
	html.write("\t<nav>\n")
	html.write("\t\t<a href=\"../redQSOs.html\">Main</a>\n")
	html.write("\t\t<a href=\"data.html\">Data</a>\n")
	html.write("\t\t<a href=\"rsample.html\">r&lt;19</a>\n")
	html.write("\t</nav>\n")
	html.write("\t</header>\n")
	html.write("\t<article style=\"padding:5px;\">\n")
	html.write("\t\t<p style=\"text-align:center;\"> \
			Observed spectra of candidate quasars from SDSS and UKIDSS photometry.</p>\n")
	html.write("\t\t<p style=\"text-align:center;font-size:10pt;\"> \
			The overplotted lines indicate an unreddened (<font color=\"#00F\">blue</font>) \
			and reddened (<font color=\"#F00\">red</font>) composite QSO template.</p>\n")
	html.write("\t\t<p style=\"text-align:center;font-size:10pt;\"> \
			Click on a spectrum to view full size.</p>\n")
	html.write("\t<table class=\"center\">\n")
	
	html.write("\t<tr>\n")
	html.write("\t<th>Spectrum</th>\n")
	html.write("\t<th>SDSS DR9</th>\n")
	html.write("\t</tr>\n")
	
	for spectrum in specList:
		id = (spectrum.split('/')[-1]).split('.')[0]
		img_file = './images/'+id+'.png'
		row = (sdss['id']==id).nonzero()
		CQ = sdss[row]
		img = "<a href=\"{0}\"> <img src=\"{0}\" width=400> </a>".format(img_file)
		if len(CQ) > 0:
			url = "<a href=\"http://skyserver.sdss3.org/dr9/en/tools/explore/obj.asp?ra="\
				+str(CQ['ra'][0])+"&dec="+str(CQ['dec'][0])+"\">info</a>"
		else:
			url = "<a href=\"http://skyserver.sdss3.org/dr9/en/tools/explore/obj.asp?ra=0\
				&dec=0\">info</a>"
	
		html.write("\t<tr>\n")
		html.write("\t\t<td>%s</td>\n" %img)
		html.write("\t\t<td>%s</td>\n" %url)
		html.write("\t<tr>\n")
	
	html.write("\t</table>\n\n")
	html.write("\t<br>\n")
	
	html.write("\t<p class=\"credits\">Created by Jens-Kristian Krogager, \
	DARK Cosmology Centre, Copenhagen University</p>\n")
	now = datetime.datetime.now()
	html.write("\t<p class=\"date\">"+now.strftime("%B %d %Y")+"</p>\n")
	
	html.write("\t</article>\n")
	html.write("\t</body>\n")
	html.write("</html>")
	html.close()

	if not args.quiet:
		print "\n [OK]  Successfully updated data.html \n"


def upload(img, args):
	sync1 = "rsync {} krogager@dark-cosmology.dk:~/Sites/redQSOs/images/.".format(img)
	sync2 = "rsync /Users/krogager/Sites/redQSOs/data.html krogager@dark-cosmology.dk:~/Sites/redQSOs/."
	
	if args.verbose:
		print ""
		print sync1
	exit1 = system(sync1)

	if exit1 == 0 and not args.quiet:
		print "\n [OK]  Successfully uploaded image to server\n"
	elif exit1 != 0:
		print "\n [ERROR] Connection to server refused. Check connection and VPN."
		exit()
	else:
		pass

	if args.verbose:
		print ""
		print sync2

	exit2 = system(sync2)
	if exit2 == 0 and not args.quiet:
		print "\n [OK]  Successfully uploaded data.html to server\n"
	elif exit2 != 0:
		print "\n [ERROR] Connection to server refused. Check connection and VPN."
		exit()
	else:
		pass

if __name__ == "__main__":
	main()
