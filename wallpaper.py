#!/usr/bin/env python2.7
import os
import random
from PIL import Image
from PIL import ImageFile
from PIL import ImageDraw
from PIL import ImageFont
import datetime as dt
import time as time
import numpy as np
import sys





def title_def(img_path):
    name_flag=img_path.split(os.sep)[-1]
    if 'NSIDC-arctic_seaice_extent' in name_flag:
        date=dt.datetime(year=int(name_flag[-14:-10]), month=int(name_flag[-8:-7]), day=int(name_flag[-5:-4]))
        title=date.strftime('%b  %d, %Y')
    elif 'BRW-Radar'  in name_flag:
        date=dt.datetime(year=int(name_flag[-24:-20]), month=int(name_flag[-20:-18]), day=int(name_flag[-18:-16]), hour=int(name_flag[-15:-13]),minute=int(name_flag[-13:-11]))
        title=date.strftime('%b  %d, %Y: %H:%M')
    elif 'BRW-Webcam'  in name_flag:
        date=dt.datetime(year=int(name_flag[-17:-13]), month=int(name_flag[-13:-11]), day=int(name_flag[-11:-9]), hour=int(name_flag[-8:-6]),minute=int(name_flag[-6:-4]))
        title=date.strftime('%b  %d, %Y: %H:%M')
    else:
        title=None
    return title

def draw_image(img_path):
    # open image
    im=Image.open(img_path)
    im=im.convert("RGBA")

    # draw border
    if t>0:
        x,y=im.size
        bsize=int(np.floor(max(x*t/100,y*t/100)))
        bg=Image.new("RGBA",(x+2*bsize,y+2*bsize), (255,255,255,255))   
        bg.paste(im,(bsize,bsize))    
        im=bg

    # print title
    if showtitle and t>0 :
        title=title_def(img_path)
        if (title is None)=='False':
            x,y=im.size
            font_size=int(0.04*res_y)
            bg=Image.new("RGBA", (x, int(font_size*2) ), (255, 255,255,255))
            draw= ImageDraw.Draw(bg)
            font=ImageFont.truetype("/usr/share/fonts/TTF/DroidSansMono.ttf", size=font_size)
            w, h =draw.textsize(title, font=font)
            draw.text((int((x-w)/2),int((font_size*2-h)/2)), title, fill="black", font=font)
            w, h =bg.size
            temp=Image.new("RGBA", (x,y+h))
            temp.paste(im, (0,0))
            temp.paste(bg,(0,y))
            im=temp
            del temp

    # draw shadow
    if s:
        x,y=im.size
        ssize=int(np.floor(max(x/100,y/100)))
        shad=Image.new("RGBA",(x+ssize,y+ssize))
        shad.paste(im,(0,0))
        draw=ImageDraw.Draw(shad)
        for l in range(1,x+ssize+1):
            colour=(0,0,0,255*l/(x+ssize))
            draw.rectangle([(l,y),(l,y+ssize)],fill=colour)
        for l in range(1,y+ssize+1):
            colour=(0,0,0,255*l/(x+ssize))
            draw.rectangle([(x,l),(x+ssize,l)],fill=colour)
        im=shad

    # resize
    x,y=im.size
    if ((x>max_size) & (y>max_size)):
        if x<y:
           x_dim=int(random.randint(pc,100)*max_size/100)
           y_dim=int(x_dim*y/x)
           im.thumbnail((x_dim,y_dim),Image.ANTIALIAS)
        else:
           y_dim=int(random.randint(pc,100)*max_size/100)
           x_dim=int(y_dim*x/y)
           im.thumbnail((x_dim,y_dim),Image.ANTIALIAS)
        
    # rotate image
    random.seed(os.times())
    if angle == 0:
        angle_rot = 0
    else:
        angle_rot = (random.randint(0,angle)*2-angle)
    im=im.rotate(angle_rot,resample=Image.BICUBIC,expand=1) 
    return im
    
def image_stack(bg,im):
    w,h=im.size

    rand_x=0
    rand_y=0
    random.seed()
    rand_x=random.randint(0,2*disp_x)-disp_x
    random.seed()
    rand_y=random.randint(0,2*disp_y)-disp_y
    pos_x_ul=xc +rand_x- w/2
    pos_y_ul=yc +rand_y- h/2
    
    if out_l==0:
      pos_x_ul=max(0,np.absolute(pos_x_ul))
    if out_r==0:
        if pos_x_ul>(w_max-w):
            pos_x_ul=random.random()*(w_max-w)
    if out_t==0:
        pos_y_ul=max(0,np.absolute(pos_y_ul))
    if out_b==0:
        if pos_y_ul>(h_max-h):
            pos_y_ul=random.random()*(h-h_max)
    pos_x_ul=int(pos_x_ul)
    pos_y_ul=int(pos_y_ul)
    
    bg_im=Image.new("RGBA",(res_x,res_y), (0,0,0,0))   
    bg_im.paste(im,(pos_x_ul,pos_y_ul))
    im=bg_im
    
    bg.paste(im, (0,0),im)
    return bg
    
def update(dtime):
    init()
    filepath=[]
    extension=('.png','.jpg')
    for path, subdirs, files in os.walk(album_dir):
        for name in files:
            if os.path.splitext(name)[1].lower() in extension:
                if os.path.getctime(os.path.join(path, name))-time.time()<dtime:
                    filepath.append(os.path.join(path, name))                   
    random.shuffle(range(1,len(filepath)+1))
    
    # grab actual wallpaper
    if int(os.path.isfile(wp_bkgd))==0:
        try:
            wp_image
        except NameError:
            bg=Image.new("RGBA",(res_x,res_y))
        else:
            bg=wp_background(res_x,res_y,wp_image)
        bg.save(wp_bkgd)
    else:
        bg=Image.open(wp_bkgd)
        bg=bg.convert("RGBA")
        
    for ii in range(0, len(filepath)):
        img_path=filepath[ii]
        ImageFile.LOAD_TRUNCATED_IMAGES=True
        im=draw_image(img_path)
        bg=image_stack(bg,im)
    im.show()

def load():  
    init()
    #def get_file_to_use():
    filepath=[]
    extension=('.png','.jpg')
    for path, subdirs, files in os.walk(album_dir):
        for name in files:
            if os.path.splitext(name)[1].lower() in extension:
                filepath.append(os.path.join(path, name)) 
    random.shuffle(range(1,len(filepath)+1))
    
    # grab actual wallpaper
    if int(os.path.isfile(wp_bkgd))==0:
        try:
            wp_image
        except NameError:
            bg=Image.new("RGBA",(res_x,res_y))
        else:
            bg=wp_background(res_x,res_y,wp_image)
        bg.save(wp_bkgd)
    else:
        bg=Image.open(wp_bkgd)
        bg=bg.convert("RGBA")
        
    for ii in range(0, len(filepath)):
        img_path=filepath[ii]
        ImageFile.LOAD_TRUNCATED_IMAGES=True
        im=draw_image(img_path)
        bg=image_stack(bg, im)        
        
    im=bg
    im.show()
    print "wp loaded"

#def fetch_image(url, path, fname)
import os
import urllib
import datetime as dt
img_dir='/home/megavolts/mediatheque/data/NSIDC/'
url = 'http://nsidc.org/data/seaice_index/images/n_extn.png'

# check input/output variable
if not os.path.isdir(img_dir):  # create output directory if not present
	os.makedirs(img_dir)

imf = open(img_dir+dt.datetime.today().strftime("%Y%m%d-%H%M")+'-NSIDC-Arctic.png','wb')
imf.write(urllib.urlopen(url).read())
imf.close

