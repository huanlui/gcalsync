# Google Calendar Synchronisation

Pyhton script that synchronises calendars between two Google Accounts. 

Python 3 is required. 

## How to install

```
pip3 install -r requirements.txt
```

## Credentials

1) Go to https://console.cloud.google.com/apis/credentials.
2) Set up a new project.

![Set up a new project](.README_images/new_project.png)

3) Choose any name (`gcal3` in the example) and don't select any organisation.

![Project name](.README_images/document_name.png)

4) Select OAuth consent screen, select `External` as User Type and click on create. 

![Consent screen](.README_images/consent_screen.png)

5) Set as app name to any name, eg. `gcalsync`. Only this name, user support email and developer contact information are mandatory.

![](.README_images/app_name.png)

6) Click on `Save and Continue`.

7) Then, in scopes, select `Add or remove scopes` and in `Manually add scopes` put this:

```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

8) Click on `Add to table` and then in `Update`.

9) Click on `Save and Continue`

10) In test users, add your own user (Google email).

11) Click on `Save and Continue`.

12) Go to Credentials, `Create Credentials`, select `OAuth client ID`.

![Credentials](.README_images/credentials.png)

13) Set application type to `Desktop app` and choose any application name. 

![](.README_images/credentials2.png)

14) Once created, click on the created credential.
 
 ![](.README_images/credential.png)
 
15) Click on the credential and download json file to the gcalsync directory, with a name format like this:

```
name.credentials.json
```

where `name` can be chosen by you to identify your account. 

![Download credentials](.README_images/download_json.png)

16) Repeat all the previous steps if you want to manage other accounts. 

## Run the application

The first time the application is run, a pop-up appears to verify your credentials. If a message indicates that Google has not
verified the application, click on `Continue`

![App verification](.README_images/app_verification.png)

Allow the permissions to edit calendars.

![](.README_images/permissions.png)

If you get a message like this, follow the instructions on it to enable calendar API.

![](.README_images/message.png)

