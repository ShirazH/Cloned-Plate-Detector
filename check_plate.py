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


def check_plate(found):
    path = 'C:\\uni_project\\final-year-project-vmmr-cmd\\yolo_gpu_large\\darknet\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    been_checked = []

    for r in range(0,len(found)):
        print("Current reg is " + str(found[r].reg))
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
                        if(len(been_checked) == 11):
                            print('Checking limit reached')
                            #If plates already checked grab details for other instances where reg matches
                            for z in range(0, len(been_checked)):
                                if str(been_checked[z]) == str(found[r].reg):
                                    for y in range(0, len(found)):
                                        if str(found[y].reg) == been_checked[z]:
                                            found[r].model = found[y].model
                                            found[r].color = found[y].color
                                            break
                            break
                        been_checked.append(found[r].reg)
                        print('Checking plate '+str(r+1)+' of '+str(len(found))+': '+str(found[r].reg))
                        driver.get('https://www.check-mot.service.gov.uk/')
                        registration = found[r].reg
                        #(https://pythonbasics.org/selenium-wait-for-page-to-load/)
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
                                    if driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[1]/h2'):
                                        color = driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[1]/h2')
                                except:
                                    color = driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div[1]/h2')
                                #Remove uneccessary text
                                color = color.text.replace('Colour','')
                                #Remove whitespace
                                color = color.strip()
                                found[r].color = color
                                print("Colour: "+color)
                                print('')
                    # If reg has already been checked grab previously found vehicle details and store
                    else:
                        print('This reg has already been checked')
                        print('')
                        for z in range(0,len(been_checked)):
                            if str(been_checked[z]) == str(found[r].reg):
                                for y in range(0,len(found)):
                                    if str(found[y].reg) == been_checked[z]:
                                        found[r].model = found[y].model
                                        found[r].color = found[y].color
                                        break
                #Reg doesn't meet the standard UK reg layout of AB12 CDE
                else:
                    print('Reg does not meet character position rules')
            #Doesn't meet standard UK plate character length
            else:
                print('Reg is not 7 characters long')
                print('')
        except IndexError:
            print('Reg length is not equal to 7')
    driver.quit()
    print('Finished checking all plates')
    print('')
    return found
