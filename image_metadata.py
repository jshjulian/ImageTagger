from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import PIL.ExifTags
import cv2, numpy, imutils

from os import listdir
from os.path import isfile, join
import time
from datetime import datetime, timedelta

class ImageTagger():
	def __init__(self, images_path, start_time, font_path):
		self.time = start_time
		self.images_path = images_path
		self.font_path = font_path
		self.images = None
		
	def _get_images(self):
		dir_of_pics = [f for f in listdir(self.images_path) if isfile(join(self.images_path, f))]

		ordered_pics = []
		for pic in dir_of_pics:
			if pic.split('.')[-1].lower() == 'jpg' or pic.split('.')[-1].lower() == 'jpeg' or pic.split('.')[-1].lower() == 'png':
				image = Image.open(self.images_path+'/'+pic)
				try:
					image.getexif()[306]
					ordered_pics.append(image)
				except:
					continue
		ordered_pics.sort(key=lambda x: x.getexif()[306])
		self.images = ordered_pics
		return ordered_pics

	def _tag_images(self, list_of_pics):
		day_zero = self.time
		# day_zero = "2019:10:27 04:20:00"
		zero_object = datetime.strptime(day_zero, '%Y:%m:%d %H:%M:%S')
		for i in range(len(list_of_pics)):
			p = list_of_pics[i]
			try:
				date_string = (p.getexif()[306])
				date_object = datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')

				td = date_object - zero_object
				dif = td / timedelta(days = 1)
				# print (dif)
				days = int(dif)
				dif_hours = (dif - days) * 24
				hours = int(dif_hours)
				dif_minutes = (dif_hours-hours) * 60
				minutes = int(dif_minutes)

				dif_text = "{0} days {1} hours and {2} minutes".format(days, abs(hours), abs(minutes))
				if days < 0:
					dif_text = "T" + dif_text
			except Exception as e:
				dif_text = "No time info found"
				print (e)

			exif = {
			    PIL.ExifTags.TAGS[k]: v
			    for k, v in p._getexif().items()
			    if k in PIL.ExifTags.TAGS
			}
			try:
				o = (exif['Orientation'])
				if o == 6:
					list_of_pics[i] = p.rotate(-90)

			except:
				print ('No known orientation')

			w = exif['ExifImageWidth']
			h = exif['ExifImageHeight']
			x = int (w *.15)
			y = int (h * .83)

			draw = ImageDraw.Draw(list_of_pics[i])
			
			text_size = 0
			fs = 0

			while text_size < (w * .7):
				font = ImageFont.FreeTypeFont(font=self.font_path, size=fs)
				text_size = draw.textsize(dif_text, font)[0]
				fs += 1
			# print (fs-1)
			draw.text((x-1, y-1),dif_text,(0,0,0), font=font)
			draw.text((x+1, y-1),dif_text,(0,0,0), font=font)
			draw.text((x-1, y+1),dif_text,(0,0,0), font=font)
			draw.text((x+1, y+1),dif_text,(0,0,0), font=font)
			draw.text((x, y),dif_text,(255,255,0), font=font)
		self.images = list_of_pics
		return list_of_pics

	def _show_pics(self, list_of_pics):
		for im in list_of_pics:
			im.show()
			im.close()

	def tag_and_show(self):
		self._tag_images(self._get_images())
		self._show_pics(self.images)

	def slideshow(self, outfile_name, seconds_per_image = 1):
		four_letter = "XVID"
		fourcc = cv2.VideoWriter_fourcc(*four_letter)
		fps = 1

		x = 0
		y = 0
		if self.images == None:
			list_of_pics = self._tag_images(self._get_images())
		else:
			list_of_pics = self.images
		for pic in list_of_pics:
			if (pic.size[0] > x):
				x = pic.size[0]
			if (pic.size[1] > y):
				y = pic.size[1]
		vw = cv2.VideoWriter(outfile_name, fourcc, fps, (x,y))
		

		for i in range(len(list_of_pics)):
			pic = list_of_pics[i]
			print (i+1)

			l_img = numpy.zeros((y,x,3), numpy.uint8)
			x_offset=y_offset=0
			
			s_img = cv2.cvtColor(numpy.array(pic), cv2.COLOR_RGB2BGR)
			if (s_img.shape[0] > s_img.shape[1]):
				s_img = imutils.resize(s_img, height=y)
			else:
				s_img = imutils.resize(s_img, width=x)
			x_offset = (x-s_img.shape[1])//2
			y_offset = (y-s_img.shape[0])//2
			l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

			for _ in range(seconds_per_image * fps):
				vw.write(l_img)

		vw.release()





	