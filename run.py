#!/usr/bin/env python3
import os
import datetime as dt
import urllib
import random
from PIL import Image, ImageFile, ImageDraw, ImageFont


# img_dir
home_dir = os.path.expanduser('~')
wp_dir = os.path.join(home_dir, '.wallpaper')
img_dir = os.path.join(home_dir, 'mediatheque/temp/')
wp_path = os.path.join(wp_dir, 'wp.png')



# grab NSIDC picture once a day
def fetch(url, img_path):
    imf = open(img_path, 'wb')
    with urllib.request.urlopen(url) as response:
        imf.write(response.read())

def fetchNSIDC(img_dir):
    img_dir = os.path.join(img_dir,'NSIDC')
    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)

    url = 'http://nsidc.org/data/seaice_index/images/n_extn_hires.png'
    img_name = dt.datetime.today().strftime("%Y%m%d")+'-NSIDC-Arctic-seaice_extent.png'
    fetch(url, os.path.join(img_dir, img_name))

fetchNSIDC(img_dir)

def init():
    ## options
    # "album_dir" is the directory containing the images for your photo album; please note that the path must be absolute (e.g. no "~") don't forget the last /
    # album_dir = "/home/megavolts/mediatheque/git/stacked_image_wallpaper/NSIDC/daily_extent"
    # wp_image="20141026-1856-NSIDC-Arctic.png"

    import tkinter as tk

    #wp_manager='nitrogen'
    screen = {}

    # screen resolution
    screen['res_x'] = tk.Tk().winfo_screenwidth()
    screen['res_y'] = tk.Tk().winfo_screenheight()

    # "w_max" and "h_max" are the maximum dimensions, in pixels, that you want the widget to be. The script will ensure that the photo album fits inside the box bounded by w_max and h_max  this is the "drop zone"
    screen['w_max'],screen['h_max']=res_x, int(res_y/3)

    # can images go out the drop zone (0=no, else =yes)? i.e; cutted on the border of the drop zone
    out_l = 0 # left
    out_r = 0 # right
    out_b = 0 # bottom
    out_t = 0 # top

    # "xc" and "yc" are the coordinates of the center of the photo album, relative to the top left corner of the Conky window, in pixels
    screen['xc'], screen['yc'] = int(res_x/2.), int(res_y/4.)

    # dispersion of the images around xc,yc (in pixels)
    screen['disp_x'] = int(2/3.*w_max)
    screen['disp_y'] = int(1/2.*h_max)


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
    # wp_bkgd="/home/megavolts/.config/wallpaper/wp_bkgd.png"

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


    # create black wallpaper
    bg = Image.new("RGBA", dim_screen, (255,0,0,255)) # 0 0 0 0
    bg.save(wp_path)

    pics = []
    for dirs, subdirs, files in os.walk(img_dir):
        for f in files:
            if os.path.splitext(f)[1].lower() in ('.jpg', '.png'):
                pics.append(os.path.join(dirs, f))

    if len(pics) > 10:
        pics = random.shuffle(pics)[0:10]
    return pics, screen
#    for p in pics:
pics, screen = init()
img_path = pics[0]

def prep_img(img_path):
    im=Image.open(img_path)
    im=im.convert("RGBA")
    im_w, im_h = im.size

    img_name=img_path.split(os.sep)[-1]
    if img_name.find('NSIDC-n'):
        img_date=dt.datetime(year=int(img_name[0:4]), month=int(img_name[4:6]), day=int(img_name[6:8]))
        title = img_date.strftime('%b  %d, %Y')
        im = im.crop([51,475,im_w-427,im_h-325])
    elif img_name.find('BRW'):
        img_date=dt.datetime(year=int(img_name[0:4]), month=int(img_name[4:6]), day=int(img_name[6:8]), hour=int(img_name[8:10]), minute=int(img_name[10:12]))
        title = img_date.strftime('%b  %d, %Y')
    else:
        title = None
    return im, title

def draw_image(img_path):
    import numpy as np
    # prep image

    im, title = prep_img(img_path)

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

    # draw border
    if t>0:
        x,y=im.size
        bsize=int(np.floor(max(x*t/100,y*t/100)))
        bg=Image.new("RGBA",(x+2*bsize,y+2*bsize), (255,255,255,255))
        bg.paste(im,(bsize,bsize))
        im=bg

    # print title
    if showtitle and title is not None:
        x, y = im.size
        font_size=int(0.02*res_y)
        bg=Image.new("RGBA", (x, int(font_size*1.4) ), (255, 255, 255,255))
        draw= ImageDraw.Draw(bg)
        font=ImageFont.truetype("/usr/share/fonts/TTF/DroidSansMono.ttf", size=font_size)
        w, h =draw.textsize(title, font=font)
        draw.text((int((x-w)/2),int((font_size*1.4-h)/2)), title, fill="black", font=font)
        w, h =bg.size
        temp=Image.new("RGBA", (x,y+h))
        temp.paste(im, (0,0))
        temp.paste(bg,(0,y))
        im=temp
        del temp

    # rotate image
    random.seed(os.times())
    if angle == 0:
        angle_rot = 0
    else:
        angle_rot = (random.randint(0,angle)*2-angle)
        angle_rot = 20
    im_rot=im.rotate(angle_rot,resample=Image.BICUBIC,expand=1)

    # draw shadow
    if s:
        x, y = im.size
        shadow_size=int(np.floor(max(x/4, y/4)))

        # find shadow start
        pix = np.array(im_rot)
        s_xh = np.where(pix[-1,:,0]==255)[0]
        s_0h = np.where(pix[:, 1, 0]==255)[0]
        s_wh = np.where(pix[:, -1, 0]==255)[0]

        w_c = s_xh[-1]-s_xh[0]
        if angle_rot >= 0:
            w_b = im_rot.size[0] - s_xh[-1]
            w_s = s_xh[0]
            h_b = im_rot.size[1] - s_wh[-1]
            h_s = s_0h[-1]
        else:
            w_b = s_xh[0]
            w_s = im_rot.size[0] - s_xh[-1]
            h_b = im_rot.size[1] - s_0h[-1]
            h_s = s_wh[-1]

#        w_b = int(np.cos(angle_rot/180*np.pi)*x)
#        w_s = abs(int(np.sin(angle_rot/180*np.pi)*y))
#        w_c = im_rot.size[1]-w_s-w_b
#        h_b = abs(int(np.sin(angle_rot/180*np.pi)*x))
#        h_s = im_rot.size[0]-abs(int(np.cos(angle_rot/180*np.pi)*y))


        # shadow color
        colour= []
        for l in range (0, shadow_size):
            colour.append((255,0,0,255-int(255*l/(shadow_size))))

        #shadow corner
        shadow_c=Image.new("RGBA", (w_c,shadow_size),(0,0,0,0))
        draw=ImageDraw.Draw(shadow_c)
        for l in range( 0, shadow_size):
            draw.rectangle([(0,l),(shadow_c.size[0],l+1)], colour[l])
        shadow_c.save('/home/megavolts/Desktop/temp-corner.png')

        # shadow below
        shadow_b=Image.new("RGBA", (w_b,shadow_size), (0,0,0,0))
        draw = ImageDraw.Draw(shadow_b)
        for l in range(0, shadow_size):
            draw.rectangle([(0,l),(w_b,l+1)],colour[l])
        pix = np.array(shadow_b)
        for ix in range(0,w_b):
            a=(1+np.sign(angle_rot))/2-(255*(ix/shadow_b.size[0]))/255
            for iy in range (0, shadow_size-1):
                pix[iy,ix][3] = int(pix[iy,ix][3]*a)
        shadow_b=Image.fromarray(pix)
        shadow_b.save('/home/megavolts/Desktop/temp-bottom0.png')
        shift = int(np.sin(angle_rot/180*np.pi)*x)
        coeff = find_coeffs([(0, 0), (shadow_b.size[0], (1-np.sign(angle_rot))/2*shift), (shadow_b.size[0], shadow_b.size[1]+(1-np.sign(angle_rot))/2*shift),(0,shadow_b.size[1])],[(0, -(1+np.sign(angle_rot))/2*shift),(shadow_b.size[0],0),(shadow_b.size[0],shadow_b.size[1]),(0,shadow_b.size[1]-(1+np.sign(angle_rot))/2*shift)])
        shadow_b =shadow_b.transform((w_b, shadow_size+shift), Image.PERSPECTIVE, coeff, Image.BICUBIC)
        shadow_b.save('/home/megavolts/Desktop/temp-bottom.png')

        # shadow side
        shadow_s=Image.new("RGBA", (w_s,shadow_size), (0,0,0,0))
        draw = ImageDraw.Draw(shadow_s)
        for l in range(0, shadow_size):
            draw.rectangle([(0,l),(w_s,l+1)],colour[l])
        pix = np.array(shadow_s)
        for ix in range(0,h_b):
            a=(1-np.sign(angle_rot))/2+np.sign(angle_rot)*(255*(ix/shadow_s.size[0]))/255
            for iy in range (0, shadow_size-1):
                pix[iy,ix][3] = int(pix[iy,ix][3]*a)
        shadow_s=Image.fromarray(pix)
        shadow_s.save('/home/megavolts/Desktop/temp-side0.png')
        shift = int(np.cos(angle_rot/180*np.pi)*x)
        coeff = find_coeffs([(0, 0), (shadow_s.size[0], (1+np.sign(angle_rot))/2*shift), (shadow_s.size[0], shadow_s.size[1]+(1+np.sign(angle_rot))/2*shift), (0, shadow_s.size[1]+0)], [(0, -(1-np.sign(angle_rot))/2*shift), (shadow_s.size[0], 0), (shadow_s.size[0], shadow_s.size[1]), (0, shadow_s.size[1]-(1-np.sign(angle_rot))/2*shift)])
        shadow_s =shadow_s.transform((w_s, shadow_size+shift), Image.PERSPECTIVE, coeff, Image.BICUBIC)
        shadow_s.save('/home/megavolts/Desktop/temp-side.png')

        # shadow assembly
        sh_bg = Image.new("RGBA", (im_rot.size[0],im_rot.size[1]+shadow_size), (0, 0, 0, 0))
        if angle_rot >= 0:
            sh_bg.paste(shadow_s, (0, h_s), shadow_s)
            sh_bg.paste(shadow_c, (w_s,im_rot.size[1]), shadow_c)
            sh_bg.paste(shadow_b, (w_s+w_c, im_rot.size[1]-h_b), shadow_b)
        sh_bg.paste(im_rot, (0,0), im_rot)
        sh_bg.save('/home/megavolts/Desktop/temp.png')
        sh_bg.show()
    return im

def image_stack(bg,im, screen):
    w, h=im.size
    import numpy as np
    rand_x=0
    rand_y=0
    random.seed()
    rand_x=random.randint(0,2*screen['disp_x'])-screen['disp_x']
    random.seed()
    rand_y=random.randint(0,2*screen['disp_y'])-screen['disp_y']
    pos_x_ul=screen['xc'] +rand_x- w/2
    pos_y_ul=screen['yc'] +rand_y- h/2

    out_l, out_r, out_t, out_b = (0, 0, 0, 0)

    if out_l==0:
      pos_x_ul=max(0,np.absolute(pos_x_ul))
    if out_r==0:
        if pos_x_ul>(screen['w_max']-w):
            pos_x_ul=random.random()*(screen['w_max']-w)
    if out_t==0:
        pos_y_ul=max(0,np.absolute(pos_y_ul))
    if out_b==0:
        if pos_y_ul>(screen['h_max']-h):
            pos_y_ul=random.random()*(h-screen['h_max'])
    pos_x_ul=int(pos_x_ul)
    pos_y_ul=int(pos_y_ul)

    bg_im=Image.new("RGBA",(screen['res_x'],screen['res_y']), (0,0,0,0))
    bg_im.paste(im,(pos_x_ul,pos_y_ul))
    im=bg_im

    bg.paste(im, (0,0),im)
    return bg

bg2 = image_stack(bg, im, screen)
bg2.show()

import numpy as np

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)