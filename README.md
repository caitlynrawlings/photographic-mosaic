# photographic-mosaic

This repository contains a Python-based tool for generating photographic mosaics from a collection of images. A photographic mosaic is a large image composed of many smaller images. In this case the smaller images are recolored to match the colors of the main image.


## Installation  

Python 3.6+: Make sure Python is installed on your system.  

Clone the [repository](https://github.com/caitlynrawlings/photographic-mosaic) and cd into the project directory.

Install the required Python libraries using pip with either:  

```bash
  pip install -r requirements.txt
```
or

```bash
  pip install Pillow numpy
```
    
## Usage/Examples

There are three required user inputs. 
- The file path to the main image. 
- The file path to the directory containing sub images. 
- The file path where the resulting image will be saved.

These can be entered as command line args or if omitted, the user will be prompted to enter these values in the console. 

There is one additional option to make the sub images monochromatic that must be passed through the command line. Default behavior is non-monochromatic. View [Screenshots](#screenshots) for examples of these outputs.

### Command line args
Main image file path:
```bash
-mf --mainfile
```
Sub images directory path:
```bash
-sf --subimagesfolder
```
Saved image:
```bash
-s --save
```
Monochromatic flag:
```bash
-m --monochrome
```

### No command line args usage
```bash
python main.py
Enter main picture file path:
./example_main_image.png
Enter path to folder containing image files to be used for sub images:
./example_sub_images_dir
Enter path for where to save final image, including valid image extension:
./example_final_image.png

Resizing sub images
./example_sub_images_dir\not_valid_image_file.txt is not a valid image file and will not be used in output
continuing...
Recoloring sub images
Combining sub images
Saving final image
```

### Command line args usage

```bash
python main.py -mf ./example_main_image.png -sf ./example_sub_images_dir/ -s ./example_final_image.png

Resizing main image
Resizing sub images
./example_sub_images_dir/not_valid_image_file.txt is not a valid image file and will not be used in output
continuing...
Recoloring sub images
Combining sub images
Saving final image
```

Monochrome
```bash
python main.py -m -mf ./example_main_image.png -sf ./example_sub_images_dir/ -s ./example_monochrome_sub_images.png

Resizing main image
Resizing sub images
./example_sub_images_dir/not_valid_image_file.txt is not a valid image file and will not be used in output
continuing...
Recoloring sub images
Combining sub images
Saving final image
```


## Screenshots

Result with non-monochromatic sub images
![Non-monochromatic sub images](./example_final_image.png)

Result with monochromatic sub images
![Monochromatic sub images](./example_monochrome_sub_images.png)


## Acknowledgements

 - [Geeks for Geeks](https://www.geeksforgeeks.org/check-if-a-file-is-valid-image-with-python/)
