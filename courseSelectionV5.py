"""
Course Enrollment Checker/AutoEnroller for UW-Madison Course Search and Enroll

------------------ Version 5.0 Updates ------------------
- Initialized chrome driver in headless mode
    - Prevents chrome window from opening
    - Allows other apps to be used while script is running
- Added function to enroll in class if available
    - Once enrolled removes class from list of classes to watch
- Added ability to differentiate between class being closed and waitlist
    - Previously both were treated as class being closed
    - Will now try to enroll if class is waitlist as well

------------------ TODO ------------------

- Renable email sending (just some small info collection needed for API keys)
- Need to prevent crashes associated with a course on the watch list not in cart
- Need to clean up input methods (less hardcoding and more user input through terminal)
- Confirm a way to prevent crashes
    - Currently thinking crash occurs when page isn't fully loaded and script tries to find element
    - Another possibility is computer locks and script can't find element
        - Disable lock screen while running
    - Another is if MyUW times out and bot doesn't login again
        - Fix is to acces the public versin of course search and enroll, then email and login
          if a course is open and want to enroll
            - Would require an architectural rewrite since courses wouldn't be addded to cart and program
              then needs to search for them on its own

__________________ Instructions __________________
- Change netID and password to your own
- Change term code to current semester
- Change courseNumsToWatch and lectureNumsToWatch to classes you want to watch
- Run requirements.txt through terminal (pip3 install -r requirements.txt)
- Run script through terminal (python3 courseEnrollment.py)
----- Following two are optional unless you want to run program for extended period of time to check when course opens ------
- Prevent lock screen from turning on
- run 'sudo pmset disablesleep 1' to prevent mac from sleeping
    - run 'sudo pmset disablesleep 0' to re-enable sleep when done

@author Arihan Yadav
@version 5.0
@date 3/19/2024
"""

import time
import yagmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Login credentials:
netID = "xxx"      #Replace [xxx]@wisc.edu with your netID
password = ""               #Replace password with your MyUW password (the one associated with your NetID)

def initDriver (): #initialize chrome driver
    #uncomment below line and comment out the next 3 lines to run in non-headless mode (debugging purposes)
    #driver = webdriver.Chrome()

    #headless mode - chrome window does not open (allows other apps to be used while script is running)
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)

    print("Chrome driver initialized")
    return driver

def login (driver): #login to course selection - still need to redirect to current semester and then courses in cart
    print("Logging in...")

    driver.get("https://enroll.wisc.edu/my-courses")

    netID = driver.find_element(By.ID, "j_username")
    password = driver.find_element(By.ID, "j_password")
    submitButton = driver.find_element(By.NAME, "_eventId_proceed")

    netID.clear()
    netID.send_keys(netID) #enter netID
    password.clear()
    password.send_keys(password) #enter password

    submitButton.click() #click submit button

    print("Waiting for user to authenticate with Duo...")

    time.sleep(20) #wait for page to load and user to authenticate with Duo

    print("Logged in ... navigating to spring 2024 course selection cart ...")

    driver.get("https://enroll.wisc.edu/my-courses?term=1244") # 1244 is the term code for Spring 2024 - change as needed
    
    print("All set!")

    time.sleep(10)

def checkClass (driver, classNum, lectureDesired): #check if class is available
    print("Checking if class " + classNum + " with " + lectureDesired + " is available...")

    elementsFound = driver.find_elements(By.XPATH, '//button')

    courseButton = 0

    for element in elementsFound:
        if element.text.find(classNum) != -1: #add more ifs or change to arr for more classes
            courseButton = element

    if courseButton != 0:
        courseButton.click()
    else:
        print("Encountered bug - returning false to mitigate crash")
        return False

    time.sleep(1)

    elementsFound = driver.find_elements(By.XPATH, '//button')

    seeSectionButton = 0

    for element in elementsFound:
        if element.text.find("See sections") != -1: #open up the sections menu
            seeSectionButton = element

    if seeSectionButton != 0:
        seeSectionButton.click()
    else:
        print("Encountered bug - returning false to mitigate crash")
        return False

    time.sleep(2)

    x = driver.find_elements(By.XPATH, '//cse-pack-header')

    lecSection = 0

    for element in x:
        if element.text.find(lectureDesired) != -1: #checks if section is lecture wanted
            lecSection = element

    if lecSection != 0:
        lecSection.click()
    else:
        print("Encountered bug - returning false to mitigate crash")
        return False

    time.sleep(2)

    classAvailable = False #boolean to check if class is available

     #checks if the class is available - check_circle means available, warning means waitlist, report means closed
     #can enroll with either check_circle or warning
    if lecSection.text.find("check_circle") != -1:
        classAvailable = True
        print("Class " + classNum + " with " + lectureDesired + " is available!")
    elif lecSection.text.find("warning") != -1:
        classAvailable = True
        print("Class " + classNum + " with " + lectureDesired + " is available! (Waitlist)")
    else:
        print("Class " + classNum + " with " + lectureDesired + " is not available")

    return classAvailable

def reset(driver): #reset to course selection page
    driver.get("https://enroll.wisc.edu/my-courses?term=1244") # 1244 is the term code for Spring 2024 - change as needed
    time.sleep(3)

def shutdown (driver): #release chrome driver
    driver.quit()
    print("Chrome driver shutdown")
    
def sendEmailAlert(alert_str):
    SENDING_EMAIL_USERNAME = "xxx@gmail.com"
    SENDING_EMAIL_PASSWORD = "" # authentication code from google security settings
    RECIPIENT_EMAIL_ADDRESS = ""

    #Sends an email alert. The subject and body will be the same.
    yagmail.SMTP(SENDING_EMAIL_USERNAME, SENDING_EMAIL_PASSWORD).send(
        RECIPIENT_EMAIL_ADDRESS, alert_str, alert_str)
    
def tryEnroll(driver):
    elementsFound = driver.find_elements(By.XPATH, '//button')

    enrollButton = 0

    for element in elementsFound:
        if element.text.find("Enroll") != -1:
            enrollButton = element

    enrollButton.click()

    elementsFound = driver.find_elements(By.XPATH, '//button')

    enrollButton = 0

    for element in elementsFound:
        print(element.text)

        if element.text.find("Enroll") != -1:
            enrollButton = element

    if enrollButton != 0:
        enrollButton.click()
    else:
        print("Encountered bug - returning false to mitigate crash")
        return False
    
    time.sleep(10)
    
def checkAllCourses(driver, courseNumsToWatch, lectureNumsToWatch, previousResults):
    for i in range (len(courseNumsToWatch)):
        reset(driver) #reset to course selection page

        if checkClass(driver, courseNumsToWatch[i], lectureNumsToWatch[i]) != previousResults[i]:
            '''
            if not previousResults[i]: #if class was previously not available
                sendEmailAlert(courseNumsToWatch[i] + " " + lectureNumsToWatch[i] + " IS NOW OPEN!")
            else: #if class was previously available
                sendEmailAlert(courseNumsToWatch[i] + " " + lectureNumsToWatch[i] + " IS NOW CLOSED!")
            print("Email sent!")
            '''
            previousResults[i] = not previousResults[i]

            #if class is now available, try to enroll
            if previousResults[i] and courseNumsToWatch[i] != "352" and courseNumsToWatch[i] != "400": #not 352 since I'm using as a test class and not 400 since I need to manually swap sections
                tryEnroll(driver)



########### Call all functions above as needed ###########

#array elements must be paired with each other (indexes must correspond to each other)
courseNumsToWatch = ["354", "400", "352"] #array of course nums to watch
lectureNumsToWatch = ["LEC 002", "LEC 004", "LAB 301"] #array of lecture nums to watch (or any specifier to a section)
previousResults = [False, True, False] #array of booleans to check if class was available previously

driver = initDriver() # initialize chrome driver

login(driver) # login to course selection

for i in range (3000):
    checkAllCourses(driver, courseNumsToWatch, lectureNumsToWatch, previousResults)
    print("Checking all classes again in 30 seconds...")
    print("")
    time.sleep(30)

shutdown(driver) # close chrome driver
