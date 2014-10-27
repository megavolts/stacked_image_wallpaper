__author__ = 'megavolts'

def fetch_image(url, img_dir, img_name):
	import os
	import urllib
	import datetime as dt

	# check input/output variable
	if not os.path.isdir(img_dir):  # create output directory if not present
		os.makedirs(img_dir)

	imf = open(img_dir+img_name,'wb')
	imf.write(urllib.urlopen(url).read())
	imf.close
