#!/usr/bin/python
import os, sys
import argparse
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import re
from xml.etree import ElementTree
from libnmap.parser import NmapParser

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
# Path to be created
#path = "./"

#os.mkdir( path, 0755 );

#print "Path is created"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("\n")
cprint(figlet_format('Justhck', font='roman'),
       'magenta', attrs=['bold'])
       
parser = argparse.ArgumentParser(description='Justhck: Hack it Simple')

parser.add_argument('-n', action='store',
			dest='machine_name',
			help='The machine name')
			 
parser.add_argument('-i', action='store',
			dest='machine_ip',
 			help='the machine IP address')

parser.add_argument('-S', action='store_true',
			default=False,
			dest='scan',
			help='Perform a nmap scan (nmap -p- -sV -oX nmap_report.xml  <machine.ip>) and saves the result')

parser.add_argument('-E', action='store_true',
			default=False,
			dest='search_exploit',
			help='Perform an exploit search for every service running on the machine and save a result')

parser.add_argument('--version', action='version',
                    version='Justhck v1.0')

results = parser.parse_args()

if (results.machine_name == None):
	print(bcolors.WARNING+"[Justhck] You need to specify the machine name to proceed!"+bcolors.ENDC)
	
elif not (os.path.isdir("./"+(str(results.machine_name)))):
	print(bcolors.OKBLUE + "[Justhck] Creating directory structure...")
	path = "./"+str(results.machine_name)
	mode = 0o755
	os.mkdir(path, mode)
	subdir = "./"+str(results.machine_name)+"/recon"
	os.mkdir(subdir, mode)
	print(bcolors.OKGREEN +"[Justhck] Directories succesfully created!" + bcolors.ENDC)
else:
	path = "./"+str(results.machine_name)
	mode = 0o755
	subdir = "./"+str(results.machine_name)+"/recon"
	
if(results.scan):
	print(bcolors.OKBLUE + "[Justhck] Performing nmap scan..." + bcolors.ENDC)
	if not (os.path.isfile("./"+(str(results.machine_name)+"/recon/nmap_report.xml"))):
		#f = open("./"+ str(results.machine_name) + "/recon/nmap_report.txt", "w")
		os.popen('nmap -sV '+str(results.machine_ip) + ' -oX ' + './'+str(results.machine_name)+'/recon/nmap_report.xml')
		#f.write(stream.read(100000))
		#f.close()
		print(bcolors.OKGREEN + "[Justhck] Scan succesfully saved on ./" + str(results.machine_name) + "/recon/nmap_report.xml" + bcolors.ENDC)
		with open ('./' + str(results.machine_name) + '/recon/nmap_report.xml', 'rt') as file: #ElementTree module is opening the XML file
    			tree = ElementTree.parse(file)
		#Lists in order to store Additional information, Product and version next to the port information.
		list_product=[]
		list_version=[]
		list_extrainf=[]
		for node in tree.iter('service'):
			product = node.attrib.get('product')
			version = node.attrib.get('version')
			extrainf = node.attrib.get('extrainfo')
			list_product.append(product)
			list_version.append(version)
			list_extrainf.append(extrainf)
		
		for i in range(0, len(list_product)):
			if not(list_product[i] == None or list_version[i] == None or list_extrainf[i] == None ):
				print(bcolors.OKGREEN + "Service name: "+ list_product[i] + " " + list_version[i] +" | Extra info:" + list_extrainf[i] + bcolors.ENDC)
	else:
		print(bcolors.OKGREEN + "[Justhck] Skipping... The scan was already performed..." + bcolors.ENDC)
		print(bcolors.OKBLUE + "[Justhck] Services detected on the machine:")
		
		with open ('./' + str(results.machine_name) + '/recon/nmap_report.xml', 'rt') as file: #ElementTree module is opening the XML file
    			tree = ElementTree.parse(file)
		#Lists in order to store Additional information, Product and version next to the port information.
		list_product=[]
		list_version=[]
		list_extrainf=[]
		for node in tree.iter('service'):
			product = node.attrib.get('product')
			version = node.attrib.get('version')
			extrainf = node.attrib.get('extrainfo')
			list_product.append(product)
			list_version.append(version)
			list_extrainf.append(extrainf)
		
		for i in range(0, len(list_product)):
			if not(list_product[i] == None or list_version[i] == None or list_extrainf[i] == None ):
				print(bcolors.OKGREEN + "Service name: "+ list_product[i] + " " + list_version[i] +" | Extra info:" + list_extrainf[i] + bcolors.ENDC)
		
if(results.search_exploit):
	print(bcolors.OKBLUE + "[Justhck] Performing the search of exploits on the scanned services..."+ bcolors.ENDC)
	availiable_exploits = os.popen('searchsploit --nmap ./'+str(results.machine_name)+'/recon/nmap_report.xml', "w") # we search the service name and version
	#print(availiable_exploits.read(10000))
	
