# ImageTagger
tag images with days after inputed date

using python3
Dependencies

 PIL
 cv2
 imutils
  
how to use

```
im = ImageTagger(images_path='path-to-images-folder', start_time='YYYY:MM:DD HH:MM:SS', font_path='path-to-a-font')

im.tag_and_show()

```
then images with yellow text will fill your screen

```
im = ImageTagger(images_path='path-to-images-folder', start_time='YYYY:MM:DD HH:MM:SS', font_path='path-to-a-font')

im.slideshow('slideshow.avi')

```
will save a video ('slideshow.avi') of the tagged images

can only make slideshows with pictures with date metadata

Example exists in imageTaggerRunner.py
