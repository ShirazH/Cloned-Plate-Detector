import json
from PIL import Image, ImageDraw, ImageFont


def verification(found_plates):
    print('Comparing predicted data with plate data')
    print('')
    path = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\frames\001.bmp'
    im = Image.open(str(path))
    ratio_w = im.size[0]
    ratio_h = im.size[1]
    res = r"C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\result_make.json"
    with open(res) as f:
        str_res = f.read()
    new_res = str_res.replace('\\', '\\\\')
    d = json.loads(new_res)

    #Go through results of make and model detection
    for i in range(0,len(d)):
        #If car is detected in frame
        if d[i]['objects']:
            #For each of the detected plates
            for j in range(0,len(found_plates)):
                #If the frame of the detected plate and detected car make match
                if str(d[i]['frame_id']) == str(found_plates[j].frame):
                    #Compare the coordinates to see if number plate is within bounding box for car
                    #Firstly calculate each corner coordinate of box around car
                    for k in range(0,len(d[i]['objects'])):
                        car_coords = d[i]['objects'][k]['relative_coordinates']
                        car_cx = car_coords['center_x'] * ratio_w
                        car_cy = car_coords['center_y'] * ratio_h
                        car_w = car_coords['width'] * ratio_w
                        car_h = car_coords['height'] * ratio_h
                        x1 = car_cx - car_w / 2
                        y1 = car_cy - car_h / 2
                        x2 = car_cx + car_w / 2
                        y2 = car_cy + car_h / 2
                        #Get center coordinates of plate
                        plate_cx = found_plates[j].coords['center_x'] * ratio_w
                        plate_cy = found_plates[j].coords['center_y'] * ratio_h
                        #Check if plate center coordinates sit within coordinates for car bounding box
                        if plate_cx > x1 and plate_cx < x2 and plate_cy > y1 and plate_cy < y2:
                            print('From predictions: ')
                            print('Predicted make and model is: ' + str(
                                d[i]['objects'][k]['name']) + ' Actual make and model from reg is: ' + str(
                                found_plates[j].model))
                            print('')
