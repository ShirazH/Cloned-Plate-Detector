#python main.py --video C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\input.mp4
import os
import argparse
import shutil
import sys
import plate_read as pr
import draw as d
import bulk_crop as bc
import check_plate as ct
import verification as vf

os.system('cmd /c "echo Starting"')

# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def vid_path(path):
    if os.path.isfile(path):
        return path
    else:
        os.system('cmd /c "echo Video not found, please enter full path to video and try again')
        sys.exit()
# Accept video file as required argument
parser = argparse.ArgumentParser(description='A program to detect cloned number plates')
parser.add_argument("--video", required=True, type=vid_path, help="Full path to video file")
args = parser.parse_args()

# Clear frames directory if exists, else create new
dir = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\frames'
if os.path.isdir(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)
    os.system('cmd /c "echo Cleared old frames"')
else:
    os.mkdir(dir)
    os.system('cmd /c "echo Creating frames directory"')

# Split video into 20 frames for every second of video length and add to frames directory
dir = dir + '\%03d.bmp'
get_frames = "ffmpeg -i " + args.video + " -r 17 " + dir
os.system(get_frames)
# Create train.txt of all frame file names for YOLO input parameter
create_train = r"dir C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\frames /s/b > C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\train.txt"
os.system(create_train)
os.system('cmd /c "echo Created train file for frames"')

# Detect plates and cars in frames via YOLO and return detected object coordinates in result.json and result_make.json
os.system('cmd /c "echo Starting plate detection')
find_plate = r"darknet detector test obj.data yolo-obj.cfg C:/uni_project/yolo_gpu_large/darknet/backup/yolo-obj_final.weights -dont_show -ext_output -out C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\result.json < C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\train.txt"
os.system(find_plate)
os.system('cmd /c "echo.')
os.system('cmd /c "echo Completed plate detection')
os.system('cmd /c "echo.')
os.system('cmd /c "echo Starting make and model detection')
find_make = r"darknet detector test make.data make.cfg make.weights -dont_show -ext_output -out C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\result_make.json < C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\train.txt"
os.system(find_make)
os.system('cmd /c "echo.')
os.system('cmd /c "echo Completed make and model detection')
os.system('cmd /c "echo.')


#Use bulk_crop.py to crop plates based on detected plate coordinates from result.json
bc.bulk_crop()

#Go through all crops and attempt to read plates and return as list with plate text and coordinates
found_complete = False
crops = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\crops.txt'
if os.path.isfile(crops):
    found = pr.plate_read()
    found_complete = True
    os.remove(crops)

# Use plates to get vehicle data from DVLA
check_complete = False
if found_complete:
    checked = ct.check_plate(found)
    check_complete = True

if check_complete:
    for plate in checked:
        print(plate.__dict__)
    #Compare predicted data vs data associated with registration details
    vf.verification(checked)
    #Draw vehicle data on relevant frames to show data gathered from reg
    d.draw(checked)
    #Combine edited frames back into video
    dir_img = dir
    dir = r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\frames'
    return_video = 'ffmpeg -framerate 10 -i ' + dir_img + ' ' + dir + r'\out.avi'
    os.system(return_video)

os.system('cmd /k "echo Finished"')



