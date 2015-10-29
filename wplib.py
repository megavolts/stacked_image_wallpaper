__author__ = 'megavolts'

import urllib


def fetch_image(url, img_path):
	import os

	# check input/output variable
	if not os.path.isdir(img_dir):  # create output directory if not present
		os.makedirs(img_dir)

	imf = open(os.path.join(img_dir,img_name),'wb')
	imf.write(urllib.request.urlopen(url).read())
	imf.close



def grabnsidc(img_dir, pole='Arctic'):
	if pole is 'Arctic':
		mark = 'n'
	elif pole is 'Antarctic' or pole is 'S':
		mark = 's'
	else:
		print('undefined polar region on Earth, choose Arctic or Antarctic')
		return

	url = 'http://nsidc.org/data/seaice_index/images/'+mark+'_extn_hires.png'
	img_name = dt.datetime.today().strftime("%Y%m%d")+'-NSIDC-Arctic-seaice_extent.png'
	imf = open(os.path.join(img_dir,img_name), 'wb')

	with urllib.request.urlopen(url) as response:
		imf.write(response.read())


