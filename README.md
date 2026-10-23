# canvas_apps
Apps for Canvas using the API

The canvas_apps folder is a library of tools that the various programs use.

# How to Connect
```
from canvas_apps.connect import connect
canvas = connect(INSTITUTION)
```
Here, `INSTITUTION` is the institution URL, as in `INSTITUTION.instructure.com`. To connect, you will need to have an API key from the appropriate Canvas instance as a text file in the same folder as the script you are using. The file names are test_key.txt, beta_key.txt, and main_key.txt. To prevent accidental changes to the production (main) instance, you will need to confirm that you really want to use that key when you select it.

# OmniTool

The OmniTool is an organizational device that makes it easier for me to add programs. The programs can also be called separately if you wanted to run them on their own.

## Setup_Tool.py

Run this program first!

This program creates a the course_data and config folders. Inside the config folder is a file called config.json, and this file stores various pieces of data that the programs might need. For example, when you store the API keys, they will appear in this document. Note that nothing here is encrypted, and so you should not share this folder if you're giving a copy of the program to someone else.

You need to store a valid API key before you will be able to build the course list (since the course list is retrieved from Canvas). The search string searches course titles, and here are a couple useful search patterns:
 * FaXX and SpXX: Under the Nevada State University naming convention, this will get the courses for Fall 20XX and Spring 20XX.
 * SUBJECT COURSE_NUMBER: For example, "MATH 120". Note that the space is required for Nevada State University courses because of the naming convention.

# Applications

## Announcement_Loader.py

Load announcements from one course and redeploy them (with post delays) in another course.

## Discussion_Post_Counter.py

This program counts the number of posts made by students in all discussion topics.

## Due_Date_Adjuster.py

This program adjusts the due dates of assignments using a CSV file. The program will both generate a blank CSV file to be filled in and upload it.

## Last_Participation_Checker.py

This program finds the student's last submission and due date of the last assignment submitted. This can be used to identify a student's last participation in the course.

## Participation_Grader.py

Grades an assignment based on participation. Full credit if there is a submission and no credit if there is not.

## Text_Entry_Fast_Grader.py

Quickly grade assignments that use the online text entry box for student submissions.
