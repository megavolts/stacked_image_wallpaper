#!/usr/bin/env python2.7

import os
import sys
import datetime as dt
import wplib as wp
import wallpaper_V2 as wp2

# grab NSIDC picture once a day
img_dir='/home/megavolts/mediatheque/data/NSIDC/'
url = 'http://nsidc.org/data/seaice_index/images/n_extn_hires.png'
img_name = dt.datetime.today().strftime("%Y%m%d")+'-NSIDC-Arctic-seaice_extent.png'

wp.fetch_image(url, img_dir, img_name)

# fetch BRW radar on the 10s
img_dir='/home/megavolts/mediatheque/data/BRW/radar/'
url = 'http://feeder.gina.alaska.edu/radar-uaf-barrow-seaice-images/current/image'
img_name = dt.datetime.today().strftime("%Y%m%d-%H%M")+'-BRW-Radar.png'

wp.fetch_image(url, img_dir, img_name)

# fetch BRW webcam on the 5s
img_dir='/home/megavolts/mediatheque/data/BRW/webcam/'
url = 'http://feeder.gina.alaska.edu/webcam-uaf-barrow-seaice-images/current/image'
img_name = dt.datetime.today().strftime("%Y%m%d-%H%M")+'-BRW-webcam.png'
import ephem
o=ephem.Observer()
o.lat='71'
o.long='-156'
s=ephem.Sun()
s.compute()

if dt.date.today()<ephem.localtime(o.next_rising(s)).date():
	sunrise = ephem.localtime(o.previous_rising(s))
	sunset = ephem.localtime(o.previous_setting(s))
else:
	sunrise = ephem.localtime(o.next_rising(s))
	sunset = ephem.localtime(o.next_setting(s))

time = dt.datetime.now()
time = dt.datetime(2014,10,26,15,0,0)

if sunrise < time < sunset:
	wp.fetch_image(url, img_dir, img_name)

album_dir = "/home/megavolts/mediatheque/data/NSIDC/"
wp_image="20141026-NSIDC-Arctic-seaice_extent.png"
img_path = album_dir + wp_image
bg_path = '/home/megavolts/mediatheque/data/NSIDC/bg.png'

bg=wp2.wallpaper(img_path, bg_path)
bg.show()