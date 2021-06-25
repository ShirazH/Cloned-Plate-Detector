from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException



#Array of regs for testing
# regs = ['ln09zzo','ty69jzl2','ty69jzl','kw13mxr','pz65byv']

print('')
def reg_check(found):
    path = 'C:\\uni_project\\final-year-project-vmmr-cmd\\yolo_gpu_large\\darknet\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    been_checked = []
    # rules = [
    #     found[r]['reg'][0].isalpha() == True,
    #     found[r]['reg'][1].isalpha() == True,
    #     found[r]['reg'][2].isdigit() == True,
    #     found[r]['reg'][3].isdigit() == True,
    #     found[r]['reg'][4].isalpha() == True,
    #     found[r]['reg'][5].isalpha() == True,
    #     found[r]['reg'][6].isalpha() == True
    # ]
    for r in range(0,len(found)):
        print("Current reg is " + str(found[r].reg))
        # print("Current reg is " + str(found[r]['reg']))
        # print("Len is ", len(found[r]['reg']))
        # https://stackoverflow.com/questions/36757965/how-to-have-multiple-conditions-for-one-if-statement-in-python
        try:
            if len(found[r].reg) == 7:
                rules = [
                    found[r].reg[0].isalpha() == True,
                    found[r].reg[1].isalpha() == True,
                    found[r].reg[2].isdigit() == True,
                    found[r].reg[3].isdigit() == True,
                    found[r].reg[4].isalpha() == True,
                    found[r].reg[5].isalpha() == True,
                    found[r].reg[6].isalpha() == True
                ]
                if all(rules):
                    if found[r].reg not in been_checked:
                    # if found[r]['reg'] not in been_checked:
                        if(len(been_checked) == 11):
                            print('checking limit reached')
                            break
                        been_checked.append(found[r].reg)
                        # been_checked.append(found[r]['reg'])
                        print('Checking plate '+str(r+1)+' of '+str(len(found))+': '+str(found[r].reg))
                        # print('Checking plate ' + str(r + 1) + ' of ' + str(len(found)) + ': ' + str(found[r]['reg']))
                        driver.get('https://www.check-mot.service.gov.uk/')
                        #(https://pythonbasics.org/selenium-wait-for-page-to-load/)
                        registration = found[r].reg
                        # registration = found[r]['reg']


                        #Wait for page to load then enter registration and click submit
                        timeout = 1
                        try:
                            element_present = EC.presence_of_element_located((By.ID, 'content'))
                            WebDriverWait(driver, timeout).until(element_present)
                        except TimeoutException as ex:
                            print(str(ex)+'Timeout exception')
                        finally:
                            print("Waiting for DVLA page to load")
                            #https://selenium-python.readthedocs.io/locating-elements.html
                            #The location and class of the input box changes on each refresh, so in order to find it we have to loop through
                            #all inputs and try to send the reg until it is successful
                            inputs = driver.find_elements_by_tag_name('input')
                            continueBt = driver.find_element_by_xpath('/html/body/main/div[3]/div/form/div/input')
                            running = True
                            for i in inputs:
                                if(running==True):
                                    try:
                                        #Send Reg
                                        i.send_keys(registration)
                                        #Click continue button
                                        continueBt.click()
                                        #Break out of loop once correct input is found
                                        running = False
                                    #if the current input is not interactble try the next one in the loop
                                    except ElementNotInteractableException:
                                        pass
                            #Wait for submission and return outcome
                            driver.implicitly_wait(0.5)
                            try:
                                if(driver.find_element_by_id('error-summary-heading')):
                                    print('The registration number '+str(found[r].reg)+' is invalid')
                                    # print('The registration number ' + str(found[r]['reg']) + ' is invalid')
                                    print('')
                                else:
                                    print("Reg is valid")
                            except NoSuchElementException:
                                print('No error during request')
                                #Get model
                                model = driver.find_element_by_xpath('/html/body/main/h1')
                                registration = registration.upper()
                                #Remove reg text before model
                                model = model.text.replace(registration,'')
                                #Remove whitespace
                                model = model.strip()
                                found[r].model = model
                                # found[r]['model'] = model
                                print("Make and model: "+model)
                                #Get color
                                try:
                                    # if driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div[1]/h2'):
                                    #     print("Gotcha")
                                    #     color = driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div[1]/h2')
                                    if driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[1]/h2'):
                                        color = driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[1]/h2')
                                except:
                                    color = driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div[1]/h2')
                                #Remove uneccessary text
                                color = color.text.replace('Colour','')
                                #Remove whitespace
                                color = color.strip()
                                found[r].color = color
                                # found[r]['color'] = color
                                print("Colour: "+color)
                                print('')
        except IndexError:
            print('Reg length is not equal to 7')
        if any(r == False for r in rules):
            print('Plate does not meet rules')
        else:
            # print(str(found[r]['reg'])+" has already been checked.")
            print(str(found[r].reg) + " has already been checked.")
    driver.quit()
    print('Finished checking all plates')
    return found

found1 = [{'reg': 'yk65vso', 'accuracy': 0.907, 'frame': '1', 'crop': '0', 'coords': {'center_x': 0.641, 'center_y': 0.712544, 'width': 0.058885, 'height': 0.028185}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.901, 'frame': '1', 'crop': '1', 'coords': {'center_x': 0.806034, 'center_y': 0.627704, 'width': 0.047475, 'height': 0.021807}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.901, 'frame': '2', 'crop': '0', 'coords': {'center_x': 0.662361, 'center_y': 0.725366, 'width': 0.061, 'height': 0.030696}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.903, 'frame': '2', 'crop': '1', 'coords': {'center_x': 0.820828, 'center_y': 0.634781, 'width': 0.042806, 'height': 0.024029}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.904, 'frame': '2', 'crop': '2', 'coords': {'center_x': 0.410278, 'center_y': 0.523548, 'width': 0.015239, 'height': 0.010726}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.902, 'frame': '3', 'crop': '0', 'coords': {'center_x': 0.685907, 'center_y': 0.739965, 'width': 0.065396, 'height': 0.031526}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.903, 'frame': '3', 'crop': '1', 'coords': {'center_x': 0.836662, 'center_y': 0.639244, 'width': 0.047808, 'height': 0.021976}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.902, 'frame': '3', 'crop': '2', 'coords': {'center_x': 0.411595, 'center_y': 0.523724, 'width': 0.01502, 'height': 0.01175}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.906, 'frame': '4', 'crop': '0', 'coords': {'center_x': 0.70878, 'center_y': 0.757691, 'width': 0.06978, 'height': 0.038068}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.91, 'frame': '4', 'crop': '2', 'coords': {'center_x': 0.853325, 'center_y': 0.647967, 'width': 0.049725, 'height': 0.024271}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xb', 'accuracy': 0.897, 'frame': '4', 'crop': '3', 'coords': {'center_x': 0.41136, 'center_y': 0.524167, 'width': 0.014684, 'height': 0.010556}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.91, 'frame': '5', 'crop': '0', 'coords': {'center_x': 0.874588, 'center_y': 0.652528, 'width': 0.049834, 'height': 0.024905}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.906, 'frame': '5', 'crop': '2', 'coords': {'center_x': 0.738272, 'centera_y': 0.778306, 'width': 0.084186, 'height': 0.037004}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.902, 'frame': '5', 'crop': '3', 'coords': {'center_x': 0.41411, 'center_y': 0.523704, 'width': 0.015833, 'height': 0.009831}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.903, 'frame': '6', 'crop': '0', 'coords': {'center_x': 0.809736, 'center_y': 0.826299, 'width': 0.095286, 'height': 0.052048}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.893, 'frame': '6', 'crop': '1', 'coords': {'center_x': 0.917649, 'center_y': 0.668655, 'width': 0.048615, 'height': 0.021814}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'rj63bfa', 'accuracy': 0.769, 'frame': '6', 'crop': '2', 'coords': {'center_x': 0.016679, 'center_y': 0.492939, 'width': 0.019518, 'height': 0.012691}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xri', 'accuracy': 0.602, 'frame': '6', 'crop': '3', 'coords': {'center_x': 0.417931, 'center_y': 0.52473, 'width': 0.015176, 'height': 0.008829}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'yk65vso', 'accuracy': 0.905, 'frame': '7', 'crop': '0', 'coords': {'center_x': 0.856007, 'center_y': 0.859331, 'width': 0.098331, 'height': 0.04966}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'eu60eoc', 'accuracy': 0.906, 'frame': '7', 'crop': '1', 'coords': {'center_x': 0.94059, 'center_y': 0.679894, 'width': 0.054985, 'height': 0.023628}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.868, 'frame': '7', 'crop': '2', 'coords': {'center_x': 0.419664, 'center_y': 0.527578, 'width': 0.019199, 'height': 0.009841}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xb', 'accuracy': 0.862, 'frame': '8', 'crop': '1', 'coords': {'center_x': 0.423264, 'center_y': 0.530453, 'width': 0.014633, 'height': 0.010008}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbi', 'accuracy': 0.9, 'frame': '9', 'crop': '0', 'coords': {'center_x': 0.428041, 'center_y': 0.533801, 'width': 0.016036, 'height': 0.012379}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbl', 'accuracy': 0.845, 'frame': '10', 'crop': '0', 'coords': {'center_x': 0.432981, 'center_y': 0.536222, 'width': 0.018075, 'height': 0.013042}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbl', 'accuracy': 0.864, 'frame': '11', 'crop': '0', 'coords': {'center_x': 0.435938, 'center_y': 0.53793, 'width': 0.015936, 'height': 0.011358}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'dk66ln', 'accuracy': 0.886, 'frame': '11', 'crop': '1', 'coords': {'center_x': 0.490492, 'center_y': 0.521714, 'width': 0.016329, 'height': 0.008439}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.879, 'frame': '12', 'crop': '0', 'coords': {'center_x': 0.440566, 'center_y': 0.544157, 'width': 0.019443, 'height': 0.011583}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'dk66lnf', 'accuracy': 0.887, 'frame': '12', 'crop': '1', 'coords': {'center_x': 0.493286, 'center_y': 0.523801, 'width': 0.014603, 'height': 0.0088}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.859, 'frame': '13', 'crop': '0', 'coords': {'center_x': 0.446284, 'center_y': 0.547988, 'width': 0.019777, 'height': 0.012233}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.824, 'frame': '14', 'crop': '0', 'coords': {'center_x': 0.451449, 'center_y': 0.55087, 'width': 0.027179, 'height': 0.013011}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbi', 'accuracy': 0.883, 'frame': '15', 'crop': '0', 'coords': {'center_x': 0.456274, 'center_y': 0.554277, 'width': 0.021411, 'height': 0.01178}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.851, 'frame': '16', 'crop': '0', 'coords': {'center_x': 0.464189, 'center_y': 0.55932, 'width': 0.024633, 'height': 0.012589}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.793, 'frame': '16', 'crop': '1', 'coords': {'center_x': 0.389963, 'center_y': 0.504538, 'width': 0.014827, 'height': 0.010893}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kgglhf', 'accuracy': 0.793, 'frame': '16', 'crop': '2', 'coords': {'center_x': 0.507342, 'center_y': 0.528454, 'width': 0.01624, 'height': 0.01081}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xb', 'accuracy': 0.898, 'frame': '17', 'crop': '0', 'coords': {'center_x': 0.472414, 'center_y': 0.563165, 'width': 0.022463, 'height': 0.014457}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19wup', 'accuracy': 0.855, 'frame': '17', 'crop': '1', 'coords': {'center_x': 0.389894, 'center_y': 0.506888, 'width': 0.014444, 'height': 0.009505}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kgglhf', 'accuracy': 0.727, 'frame': '17', 'crop': '2', 'coords': {'center_x': 0.511552, 'center_y': 0.529878, 'width': 0.01488, 'height': 0.010523}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.881, 'frame': '18', 'crop': '0', 'coords': {'center_x': 0.483088, 'center_y': 0.567684, 'width': 0.027823, 'height': 0.013901}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.904, 'frame': '19', 'crop': '0', 'coords': {'center_x': 0.495048, 'center_y': 0.575961, 'width': 0.028843, 'height': 0.012541}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.907, 'frame': '20', 'crop': '0', 'coords': {'center_x': 0.502683, 'center_y': 0.580935, 'width': 0.03133, 'height': 0.015114}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.819, 'frame': '20', 'crop': '1', 'coords': {'center_x': 0.399187, 'center_y': 0.51007, 'width': 0.01523, 'height': 0.009822}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.904, 'frame': '21', 'crop': '0', 'coords': {'center_x': 0.51655, 'center_y': 0.589659, 'width': 0.033025, 'height': 0.013621}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19yup', 'accuracy': 0.781, 'frame': '21', 'crop': '1', 'coords': {'center_x': 0.404356, 'center_y': 0.510848, 'width': 0.013929, 'height': 0.009684}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.907, 'frame': '22', 'crop': '0', 'coords': {'center_x': 0.533244, 'center_y': 0.597962, 'width': 0.033774, 'height': 0.016127}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.878, 'frame': '23', 'crop': '0', 'coords': {'center_x': 0.411057, 'center_y': 0.515034, 'width': 0.015346, 'height': 0.009457}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.885, 'frame': '23', 'crop': '1', 'coords': {'center_x': 0.551326, 'center_y': 0.608201, 'width': 0.038198, 'height': 0.016842}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.891, 'frame': '24', 'crop': '0', 'coords': {'center_x': 0.413677, 'center_y': 0.519165, 'width': 0.015412, 'height': 0.010331}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbl', 'accuracy': 0.865, 'frame': '24', 'crop': '1', 'coords': {'center_x': 0.560768, 'center_y': 0.61444, 'width': 0.035719, 'height': 0.017494}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.841, 'frame': '25', 'crop': '0', 'coords': {'center_x': 0.41749, 'center_y': 0.52063, 'width': 0.015228, 'height': 0.010834}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.905, 'frame': '25', 'crop': '1', 'coords': {'center_x': 0.585549, 'center_y': 0.632995, 'width': 0.045903, 'height': 0.020436}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.902, 'frame': '26', 'crop': '0', 'coords': {'center_x': 0.61404, 'center_y': 0.650541, 'width': 0.049703, 'height': 0.023018}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.891, 'frame': '26', 'crop': '2', 'coords': {'center_x': 0.419743, 'center_y': 0.524347, 'width': 0.015996, 'height': 0.010189}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.905, 'frame': '27', 'crop': '0', 'coords': {'center_x': 0.647613, 'center_y': 0.675002, 'width': 0.052244, 'height': 0.025852}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.914, 'frame': '28', 'crop': '0', 'coords': {'center_x': 0.66702, 'center_y': 0.688635, 'width': 0.051587, 'height': 0.025994}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.896, 'frame': '28', 'crop': '2', 'coords': {'center_x': 0.425775, 'center_y': 0.527532, 'width': 0.01746, 'height': 0.009321}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.907, 'frame': '29', 'crop': '0', 'coords': {'center_x': 0.716426, 'center_y': 0.720952, 'width': 0.06575, 'height': 0.031293}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kp1744ly', 'accuracy': 0.624, 'frame': '29', 'crop': '1', 'coords': {'center_x': 0.016873, 'center_y': 0.5187, 'width': 0.024031, 'height': 0.0136}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.888, 'frame': '29', 'crop': '2', 'coords': {'center_x': 0.430472, 'center_y': 0.530244, 'width': 0.019849, 'height': 0.011718}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.901, 'frame': '30', 'crop': '0', 'coords': {'center_x': 0.779449, 'center_y': 0.765002, 'width': 0.070957, 'height': 0.037568}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kf17aly', 'accuracy': 0.747, 'frame': '30', 'crop': '1', 'coords': {'center_x': 0.023481, 'center_y': 0.517689, 'width': 0.027447, 'height': 0.013955}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.897, 'frame': '30', 'crop': '2', 'coords': {'center_x': 0.436083, 'center_y': 0.53486, 'width': 0.01698, 'height': 0.011421}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.877, 'frame': '31', 'crop': '0', 'coords': {'center_x': 0.870931, 'center_y': 0.821835, 'width': 0.093739, 'height': 0.044469}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kf17ulv', 'accuracy': 0.788, 'frame': '31', 'crop': '1', 'coords': {'center_x': 0.030719, 'center_y': 0.516944, 'width': 0.023912, 'height': 0.014202}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.892, 'frame': '31', 'crop': '2', 'coords': {'center_x': 0.439139, 'center_y': 0.538028, 'width': 0.017689, 'height': 0.012172}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'ad59xbu', 'accuracy': 0.705, 'frame': '32', 'crop': '0', 'coords': {'center_x': 0.931079, 'center_y': 0.85874, 'width': 0.089891, 'height': 0.054718}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kf17ulv', 'accuracy': 0.905, 'frame': '32', 'crop': '1', 'coords': {'center_x': 0.036409, 'center_y': 0.51513, 'width': 0.023887, 'height': 0.014038}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.887, 'frame': '32', 'crop': '2', 'coords': {'center_x': 0.443447, 'center_y': 0.538113, 'width': 0.018215, 'height': 0.01223}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'pk19vup', 'accuracy': 0.884, 'frame': '33', 'crop': '0', 'coords': {'center_x': 0.449019, 'center_y': 0.543177, 'width': 0.020936, 'height': 0.010034}, 'model': 'Unknown', 'color': 'Unknown'},
{'reg': 'kf17uly', 'accuracy': 0.827, 'frame': '33', 'crop': '1', 'coords': {'center_x': 0.041957, 'center_y': 0.512028, 'width': 0.020348, 'height': 0.010834}, 'model': 'Unknown', 'color': 'Unknown'}]

# print(found[0].reg)