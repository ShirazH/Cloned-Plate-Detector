from PIL import Image
import json
import os
import shutil


def bulk_crop():
    # Open results and convert to string, escape back slashes in results to prevent jsondecode error, then load back as json
    # res = "result.json"
    res = r"C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\result.json"
    try:
        with open(res) as f:
            strRes = f.read()
            newRes = strRes.replace('\\','\\\\')
            d = json.loads(newRes)
    except FileNotFoundError:
        print("\n result.json not found, please make sure it's in the correct directory")
    # For entire results, check if 'objects' is not empty and if class name == 'Registration',then get bounding box coordinates
    else:
        # Clear crops directory if exists, else create new
        dir = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\crops'
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            os.mkdir(dir)
            print('Starting cropping of detected plates')
            os.system('cmd /c "echo Cleared old crops"')
        else:
            os.mkdir(dir)
            os.system('cmd /c "echo Creating crops directory"')
        # Using result.json coordinates, crop and save each detected number plate
        for i in range(0,len(d)):
            if(d[i]['objects']):
                for j in range(0,len(d[i]['objects'])):
                    if(d[i]['objects'][j]['name'] == 'Registration'):
                        coords = d[i]['objects'][j]['relative_coordinates']
                        center_x = coords['center_x']
                        center_y = coords['center_y']
                        box_width = coords['width']
                        box_height = coords['height']
                        # Open image
                        im = Image.open(str(d[i]['filename']))
                        # Size of the image in pixels (size of original image)
                        width, height = im.size
                        # Setting the points for cropped image
                        left_x = (center_x * width) - box_width*width/2
                        top_y = (center_y * height) - box_height*height/2
                        right_x = left_x + (box_width * width)
                        bottom_y = top_y + (box_height * height)
                        # Cropped image of above dimension
                        im1 = im.crop((left_x, top_y, right_x, bottom_y))
                        #Save image and create new name for each crop produced per frame
                        new_name = im.filename[0:-4] + '_crop' + str(j) + '.jpg'
                        new_name = new_name.replace('frames','crops')
                        im1 = im1.save(new_name,'JPEG')
        crops = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\crops.txt'
        with open(crops, "w+") as file:
            file.write('True')
        print('Created new crops')
