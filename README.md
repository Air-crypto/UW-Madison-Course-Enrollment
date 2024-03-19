# UW-Madison-Course-Enrollment
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
