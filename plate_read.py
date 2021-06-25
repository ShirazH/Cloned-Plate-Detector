import requests
import glob
from time import sleep
import json


#Define class for reg plate and all its accompanying details
class plate:
    def __init__(self, reg, accuracy, frame, crop, coords, model, color):
        self.reg = reg
        self.accuracy = accuracy
        self.frame = frame
        self.crop = crop
        self.coords = coords
        self.model = model
        self.color = color


def plate_read():
    # Open YOLO detection results file and convert to string, escape \ to prevent JSON decode error, then load back as json
    res = r"C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\result.json"
    with open(res) as f:
        strRes = f.read()
    newRes = strRes.replace('\\', '\\\\')
    d = json.loads(newRes)
    #Create list to store found plate details
    found_plates = []
    #Characters before and after frame and crop indices used to find the indices and remove leading zeroes
    frame_start = 's\\'
    frame_end = '_crop'
    crop_start = '_crop'
    crop_end = '.'
    #Set plate region
    regions = ['gb']


    #For each crop that contains a detected plate, send it to the plate reader and get back the registraion guess
    #and accuracy score, then find the frame and crop index from the crop file name and store these in the found_plates
    #list. Frame and crop indices are used to identify each unique plate from the results.json file that stores details
    #of plates detected by YOLO so that the coordinates can be extracted for use in drawing and labelling registration
    #and accuracy scores next to the plate in the images
    for path in glob.iglob(r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\crops\*.jpg'):
        #Add 1 second time delay for API request in order to make it work with multiple plates
        sleep(1)
        with open(path, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),
                files=dict(upload=fp),
                headers={'Authorization': 'Token bd9f81e974d819d39f86173a0ade5b7d6c396012'})
        #Return found plate details
        res = response.json().get('results')
        #Get guess accuracy score
        try:
            f_score = res[0].get('candidates')[0].get('score')
        except IndexError:
            f_score = '0'
            print('Cannot read plate: ' +str(path))
        #Only continue if plate was readable
        if(f_score!='0'):
            #Get guess for registraion
            try:
                f_reg = res[0].get('plate')
                print('Plate successfully read: '+str(path))
            except IndexError:
                f_reg = 'Unreadable'
            #Get frame index
            frame_cut = path[path.find(frame_start)+2:path.find(frame_end)]
            frame_index = frame_cut.lstrip("0")
            #Get crop index
            crop_index = path[path.find(crop_start)+5:path.find(crop_end)]
            #Store all plate specific details in found_plates list
            found_plates.append(plate(f_reg,f_score,frame_index,crop_index,None,'Unknown','Unknown'))


    #Cross compare found plate results with detected plate results in order to get bounding box coordinates for labelling purposes
    #For all read plates
    for x in range(0,len(found_plates)):
        #For all detected plates
        for i in range(0,len(d)):
            #If frame indices match
            if(str(d[i]['frame_id']) == found_plates[x].frame):
                #For each crop index
                for m in range(0,len(d[i]['objects'])):
                    #If crop indices match
                    if(str(m) == found_plates[x].crop):
                        #Get coordinates
                        found_plates[x].coords = d[i]['objects'][m]['relative_coordinates']
    for m in range(0,len(found_plates)):
        print(found_plates[m].__dict__)
    crops = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\crops.txt'
    with open(crops, "w+") as file:
        file.write('True')
    return found_plates