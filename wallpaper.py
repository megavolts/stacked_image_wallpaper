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


def init():
    ## options
    # "album_dir" is the directory containing the images for your photo album; please note that the path must be absolute (e.g. no "~") don't forget the last /
    album_dir = "/home/megavolts/mediatheque/github/wallpaper_rotate/NSIDC/daily_extent"
    #wp_image=["/mnt/data/mediatheque/graphisme/bds/Loisel/clo06.jpg"]
    
    # screen resolution
    #wp_manager='nitrogen'
    res_x,res_y=1400,800
    
    # "w_max" and "h_max" are the maximum dimensions, in pixels, that you want the widget to be. The script will ensure that the photo album fits inside the box bounded by w_max and h_max  this is the "drop zone"
    w_max,h_max=res_x, int(res_y/3)
    
    # can images go out the drop zone (0=no, else =yes)? i.e; cutted on the border of the drop zone
    out_l = 0 # left
    out_r = 0 # right
    out_b = 0 # bottom
    out_t = 0 # top
    
    # "xc" and "yc" are the coordinates of the center of the photo album, relative to the top left corner of the Conky window, in pixels
    xc, yc = int(res_x/2.), int(res_y/4.)
    
    # dispersion of the images around xc,yc (in pixels)
    disp_x = int(2/3.*w_max)
    disp_y = int(1/2.*h_max)
    
    # pictures are resized to fit the drop zone, but they can be smaller than the drop zone if pc <=100
    # max_size are the maximum length of the short edge
    max_size=int(res_y/4)
    pc = 75
    
    # "t" is the thickness of the frame, in % of the photo (0 = no frame)
    t = 1
    
    # "s" is to draw a shadow on the bottom right side of the image (true/false) has to be improve with rotation of picture
    s ='true'
    
    showtitle='true'
    
    # angle is the maximum angle of rotation of the image, in degrees (0-180).
    angle = 20
    
    # filename of the image created by the script
    wp_bkgd="/home/megavolts/.config/wallpaper/wp_bkgd.png"
    
    if w_max>res_x:
        w_max=res_x
    if h_max>res_y:
        h_max=res_y
    
    
    
    
    # clean variable 
    #del datapath,extension,outputpath,outputfn,files,name,path,subdirs,a
    
    #wallpaper=["/mnt/data/mediatheque/graphisme/bds/Loisel/clo05.jpg","/mnt/data/mediatheque/graphisme/girly/red_star_girl.jpg"]
    #
    ### wallpaper
    #home_dir=os.path.expanduser("~")
    #
    #if wp_manager=='nitrogen':
    #    wp_config="/.config/nitrogen/bg-saved.cfg"
    #    with open(home_dir+wp_config) as wpfile:
    #        for num,line in enumarte (wpfile,1):
    #            if 'xin_1' in line:
    #                lin_flag=line
    #                return 1
    #    
#

# wallpaper background
def wp_background(res_x,res_y,wallpaper):
    for ii_im in [0,len(wallpaper)-1]:
        im_temp=Image.open(wallpaper[ii_im])
        im_temp=im_temp.convert("RGBA")
        w,h=im_temp.size
        if w>res_x | h>res_y:
            im_temp.thumbnail((res_x,res_y),Image.ANTIALIAS)
        elif int(float(w)/res_x>0.6) & int(float(h)/res_y>0.6):
            scale=max(float(w)/res_x,float(h)/res_y)
            w=int(w/scale)
            h=int(h/scale)
            im_temp=im_temp.resize((w,h),Image.ANTIALIAS)
            bg=Image.new("RGBA",(res_x,res_y))
            bg.paste(im_temp,((res_x-w)/2,(res_y-h)/2))
            im_temp=bg
        else:
            bg=Image.new("RGBA",(res_x,res_y))
            bg.paste(im_temp,((res_x-w)/2,(res_y-h)/2))
            im_temp=bg
    return im_temp
    
def title_def(img_path):
    name_flag=img_path.split(os.sep)[-1]
    if 'NSIDC-arctic_seaice_extent' in name_flag:
        date=dt.datetime(year=int(name_flag[-14:-10]), month=int(name_flag[-8:-7]), day=int(name_flag[-5:-4]))
        title=date.strftime('%b  %d, %Y')
    elif 'BRW_radar'  in name_flag:
        date=dt.datetime(year=int(name_flag[-24:-20]), month=int(name_flag[-20:-18]), day=int(name_flag[-18:-16]), hour=int(name_flag[-15:-13]),minute=int(name_flag[-13:-11]))
        title=date.strftime('%b  %d, %Y: %H:%M')
    elif 'BRW_webcam'  in name_flag:
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
    
