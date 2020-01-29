import os
import subprocess
import tempfile
from pdf2image import convert_from_path
from PIL import Image


#os.chdir(curdir)
#toppm = r"C:\Program Files\poppler-0.68.0\bin\pdftoppm.exe"
myfile = 'oxford.pdf'
destination = 'cut_result/'
tempfolder = ''
f_page = 90
l_page = 101
gap = 200
xstep = 460
ystep = 662

#subprocess.Popen('"%s" -png "%s" out' % (toppm, myfile))	convert to png instead of ppm, -f first page, -l last page, -r resolution (default 150)
with tempfile.TemporaryDirectory() as path:
	converted_imgs = convert_from_path(myfile, first_page  = f_page, last_page = l_page) #output_folder = tempfolder


def cutme(mypath = destination):
	if not os.path.exists(destination): 
		os.makedirs(destination)

	idict,wdict = {},{}
	counter, n_counter = 0,0

	for n in range(len(converted_imgs)):
		if not n%2:
			for x in range(4):
				for y in range(4):
					mx = xstep * x + gap
					my = ystep * y
					img2 = converted_imgs[n].crop((mx, my, mx+xstep, my+ystep))
					idict[counter] = img2.transpose(Image.ROTATE_270)
					counter +=1
		else:
			img = converted_imgs[n].transpose(Image.ROTATE_180)	
			__,sh = img.size
			for x in range(4):
				for y in range(4):
					mx = xstep * x + gap
					my = sh - ystep - ystep * y
					img2 = img.crop((mx, my, mx+xstep, my+ystep))
					wdict[n_counter] = img2.transpose(Image.ROTATE_270)
					n_counter+=1

	for x in idict.keys():
		idict[x].save(mypath + str(x+1) + '.png')
	for x in wdict.keys():
		wdict[x].save(mypath + str(x+1) + '-1.png')


if __name__ == '__main__':
	cutme()

