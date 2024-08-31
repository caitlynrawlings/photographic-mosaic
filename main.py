from PIL import Image
import numpy as np
import os
import argparse

def image_of_images(main_image_path, sub_images_folder, final_image_path, monochrome):
    """
    Creates image from recolored sub images and save that image to final_image_path

    Params:
        - main_image_path ~ string : path to image to be recreated
        - sub_images_folder ~ string : path to folder with sub images
        - final_image_path ~ string : path to where the final image with be saved
                needs to be valid image file name + extension
        - monochrome ~ bool : if the sub images should be monochrome
    """
    print_progress("Resizing main image")
    # resize image to be 200 pixels in the longest direction
    image = Image.open(main_image_path)
    width, height = image.size
    divisor = max(width, height) // 200
    image = image.resize((max(width // divisor, 1), max(height // divisor, 1)))

    print_progress("Resizing sub images")

    # iterate through sub_images_folder and put all the image objects in an array
    sub_images = []
    for filename in os.listdir(sub_images_folder):
        file_path = os.path.join(sub_images_folder, filename)
        
        if not os.path.isfile(file_path): # Check if it's a file
            print(file_path + " is not a file and will not be used in output")
            print("continuing...")
        elif not is_valid_image_pillow(file_path): # Check if valid image
            print(file_path + " is not a valid image file and will not be used in output")
            print("continuing...")
        else:
            sub_images.append(make_square(file_path, monochrome))
    
    print_progress("Recoloring sub images")

    # turn main image to 2d array of rgb vallues
    pixels = np.array(image)

    # Initialize the 2D array to store recolored sub-images
    sub_images_arr = [[None for _ in range(len(pixels[0]))] for _ in range(len(pixels))]
    sub_images_idx = 0

    # iterate through the 2d array of the main image
    # and recolor the sub_images and add to image 2d array
    for r_idx, row in enumerate(pixels):
        for c_idx, _ in enumerate(row):
            sub_images_arr[r_idx][c_idx] = adjust_to_target_avg(sub_images[sub_images_idx], row[c_idx])
            sub_images_idx = (sub_images_idx + 1) % len(sub_images)

    print_progress("Combining sub images")

    # combine images
    final_image = combine_images(sub_images_arr)

    print_progress("Saving final image")

    final_image.save(final_image_path, optimize=True, quality=95)

def make_square(image_path, monochrome):
    """
    Returns a squared 50x50 pixel image

    Params:
        - image_path ~ string : path of image to get edited version of
        - monochrome ~ bool : if the image should be monochrome
    
    Returns: 
        - Image : the edited version of inputted image. Image is greyed 
                if monochrome parameter is true
    """
    image = None
    if monochrome:
        image = Image.open(image_path).convert('L').convert('RGB')
    else:
        image = Image.open(image_path).convert('RGB')

    new_dim = min(image.size)
    image = image.crop((0, 0, new_dim, new_dim)).resize((50, 50))
    
    return image

def combine_images(image_array):
    """
    Takes inputted images and combines them into 1 image

    Params:
        - image_array ~ Image[Image[]] : 2d array of Images.
            Each image must be square and all muct share the same dimensions.
            Each row in array is array of images that become one
            row of the output image with the next row being appended
            below that
    
    Returns: 
        - Image : combination of inputted images
    """
    # Get the number of rows and columns in the array
    num_rows = len(image_array)
    num_cols = len(image_array[0])
    
    # Get the dimensions of the first image (assuming all images are the same size)
    image_width, image_height = image_array[0][0].size
    
    # Calculate the dimensions of the combined image
    combined_width = num_cols * image_width
    combined_height = num_rows * image_height
    
    # Create a new image with the combined dimensions
    combined_image = Image.new('RGB', (combined_width, combined_height))
    
    # Paste each image into the correct location
    for row in range(num_rows):
        for col in range(num_cols):
            image = image_array[row][col]
            combined_image.paste(image, (col * image_width, row * image_height))
    
    return combined_image 

def adjust_to_target_avg(image, target_color):
    """
    Takes inputted image and alters the colors to have an average of
    a given target_color

    Params:
        - image_array ~ Image : image to get altered version of
    
    Returns: 
        - Image : recolored image
    """
    # Convert the image to array
    image_data = np.array(image)

    # Calculate the average color
    current_avg_color = np.mean(image_data, axis=(0, 1))

    # Handle potential zero values in current_avg_color
    current_avg_color = np.where(current_avg_color == 0, 1, current_avg_color)

    # Compute scaling factor for each channel
    scaling_factors = np.array(target_color)[:3] / current_avg_color

    # Adjust pixel values
    adjusted_image_data = np.clip(image_data * scaling_factors, 0, 255).astype(np.uint8)
    
    # Convert back to PIL image
    adjusted_image = Image.fromarray(adjusted_image_data)
    
    return adjusted_image

# got code from 'https://www.geeksforgeeks.org/check-if-a-file-is-valid-image-with-python/'
def is_valid_image_pillow(file_name):
    """
    Checks if file is commpatable with Image from PIL

    Params:
        - file_name ~ string : name of file
    
    Returns: 
        - boolean : if the image is valid image file
    """
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False
    
def print_progress(progress_message):
    """
    Prints progress message to console while images are being processed

    Params:
        - progress_message ~ string : message to print
    """
    print(progress_message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='image_of_images',
                        description='Save an image file that is created from recolored subimages'
    )

    parser.add_argument("-mf", "--mainfile", help="Main file")
    parser.add_argument("-sf", "--subimagesfolder", help="Sub images folder")
    parser.add_argument("-s", "--save", help="Path to save to")
    parser.add_argument("-m", "--monochrome", help="Use to make the subimages monochromatic", action='store_true')

    args = parser.parse_args()
    
    main_file_path = args.mainfile
    if not main_file_path:
        print("Enter main picture file path:")
        main_file_path = input()
    
    sub_folder_path = args.subimagesfolder
    if not sub_folder_path:
        print("Enter path to folder containing image files to be used for sub images:")
        sub_folder_path = input()

    final_image_name = args.save
    if not final_image_name:
        print("Enter path for where to save final image, including valid image extension:")
        final_image_name = input()

    print("\n")

    image_of_images(main_file_path, sub_folder_path, final_image_name, args.monochrome)

