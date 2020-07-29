from image_metadata import ImageTagger

images_path = "" #./pictures
start_time = "" #2019:10:27 04:20:00
font_path = "" #c:/windows/fonts/arial.ttf
output_name = "" #slideshow.avi

im = ImageTagger(images_path, start_time, font_path)
# im.tag_and_show()
im.slideshow(output_name)

