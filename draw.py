from PIL import Image, ImageDraw, ImageFont
import glob


def draw(plates):
    found = plates
    #Set character start and end for getting frame indices from image file names
    p_start = 's\\'
    p_end = '.'
    #Create dictionary for tracking how many times each frame has already been drawn on, this is used for updating y
    #positions of writing
    draw_count = {}
    #For all read plates
    for r in range(0,len(found)):
        # https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
        #For each frame from the video
        for path in glob.iglob(r'C:\uni_project\final-year-project-vmmr-cmd\yolo_gpu_large\combining\frames\*.bmp'):
            #Get frames indices for video frames and see if they match the frame the plate was taken from
            frame_cut = path[path.find(p_start)+2:path.find(p_end)]
            frame_index = frame_cut.lstrip("0")
            if(str(found[r].frame) == str(frame_index)):
                #Update draw count for each frame, this is used for tracking y positioning of text written on the frame
                if int(frame_index) in draw_count:
                    draw_count[int(frame_index)] += 1
                else:
                    draw_count[int(frame_index)] = 0
                #Accuracy of plate reading
                acc = int(found[r].accuracy*100)
                #All vehicle data gathered from plate reading that is displayed at the top of the frame
                car_stats = str(found[r].reg)+' '+str(acc)+'% '+str(found[r].model)+' '+str(found[r].color)
                #Open the matched frame and calculate coordinates for bbox of each found plate
                im = Image.open(str(path))
                img1 = ImageDraw.Draw(im)
                cx = found[r].coords['center_x']*im.size[0]
                cy = found[r].coords['center_y']*im.size[1]
                w = found[r].coords['width']*im.size[0]
                h = found[r].coords['height']*im.size[1]
                x1 = cx - w/2
                y1 = cy - h/2
                x2 = cx + w/2
                y2 = cy + h/2
                shape = [x1,y1,x2,y2]
                img1.rectangle(shape, fill =None, outline ="cyan", width=5)
                #Convert frame and crop ids so that they match the naming format of cropped images so that we can open
                #plate crops and overlay them on the current frame
                f_id = str(found[r].frame)
                while(len(f_id)<3):
                    f_id = '0'+f_id
                c_id = found[r].crop
                crop_path = 'C:\\uni_project\\final-year-project-vmmr-cmd\\yolo_gpu_large\\combining\\crops\\'+f_id+'_crop'+str(c_id)+'.jpg'
                plate_cr = Image.open(crop_path)
                # Set font and write car details at top of current frame along with crop of plate
                font = ImageFont.truetype('ariblk.ttf', 50)
                im.paste(plate_cr,(0,font.getsize(car_stats)[1]*draw_count[int(frame_index)]))
                img1.text((plate_cr.size[0]+20,(font.getsize(car_stats)[1]*draw_count[int(frame_index)])-15),car_stats, font = font, fill="magenta")
                #Overwrite image
                im.save(path)
                print('Updated frame')
    print('Drawing and labelling complete for all frames')

