# canvas_apps
Apps for Canvas using the API

The canvas_apps folder is a library of tools that the various programs use.

# How to Connect
```
canvas = connect(INSTITUTION)
```
Here, `INSTITUTION` is the institution URL, as in `INSTITUTION.instructure.com`. To connect, you will need to have an API key from the appropriate Canvas instance as a text file in the same folder as the script you are using. The file names are test_key.txt, beta_key.txt, and main_key.txt. To prevent accidental changes to the production (main) instance, you will need to confirm that you really want to use that key when you select it.

# Setup Tools

## Course_List_Generator.py

Run this program first! This will first create a `course_data` folder that will contain all the inventory files for the various scripts. Then it will ask for a search string for the courses that you want to have easy access to. (For example, you can use "Fa26" to search for Fall 2026 courses under the NSU course naming convention.) These courses will be stored in a file called courses.csv for future usage.

## Inventory_Generator.py

This program will create (or recreate) the course inventory for all of the classes in the courses.csv file. It should take less than a minute per course.

# Applications

## Discussion_Post_Counter.py

This program counts the number of posts made by students under a discussion topic.

## Due_Date_Adjuster.py

This program adjusts the due dates of assignments using a CSV file. The program will both generate a blank CSV file to be filled in and upload it.

## Last_Participation_Checker.py

This program finds the student's last submission and due date of the last assignment submitted. This can be used to identify a student's last participation in the course.

## Participation_Grader.py

Grades an assignment based on participation. Full credit if there is a submission and no credit if there is not.
