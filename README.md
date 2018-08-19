# A program for checking if certain courses are available

This is a program designed to be run on an idle computer like a raspberry pi or desktop, and checks periodically if a course has become available or it's status has changed.

## Prerequisites

Python 3 is required to run this program. 

urllib is one module that must be downloaded before running this program it can be downloaded by running:

```
python -m pip install urllib
```
It's also required to get a twilio account so a text can be sent to your phone when a course becomes available. Once you set up a twilio account you can add these environment variables to your bash_profile (or zprofile for zsh)  so the program can access them.

```
echo 'export TWILIO_ACCOUNT_SID="_your_account_sid_"' >> ~/.bash_profile
echo 'export TWILIO_AUTH_TOKEN="_your_auth_token_"' >> ~/.bash_profile
echo 'export TWILIO_NUMBER="_your_twilio_number_"' >> ~/.bash_profile
```

## Running the program

To run the program simply run 

```
python3 UBCCourseNotifierMain.py
```

and fill out the nessesary course info
 
