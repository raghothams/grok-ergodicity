# 7 Steps to Deploy the app on Heroku

[Heroku](https://www.heroku.com) is a Cloud platform and is one of the easiest and fastest ways to deploy Python applications.

This document explains how to deploy this `streamlit` application on Heroku.

### Step 1: 3 Required files

**1 - `requirements.txt`**   
A standard file that lists all the libraries needed for the app.

**2 `setup.sh`**    
This is for Heroku when setting up the application.

This should have the following code

```
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

Replace `your-email@domain.com` with yours.

**3 `Procfile`**   
This is for Heroku when setting up the application.

This file should have the following code

```
web: sh setup.sh && streamlit run app.py
```

### Step 2: Create Heroku Account

Create a Heroku account [here](https://signup.heroku.com/).

### Step 3: Download Heroku CLI

Download the Heroku CLI [here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

### Step 4: Login to Heroku

Login to Heroku from the terminal (from the repo directory)

```
$ heroku login 
```

This will fire up the browser where you validate the credentials. Return to terminal.

### Step 5: Create a remote branch on Heroku
To deploy the application, first create a remote on Heroku by typing the following command

```
$ heroku create
```


### Step 6: Push code to Heroku
Now, push the code to Heroku using the following set of commands

```
$ git add .
$ git commit -m "streamlit app deploy on heroku"
$ git push heroku master
```

If you are on a `branch` rather than on master in your repository, replace the last line above with the following:

```
$ git push heroku yourbranch:master
```


### Step 7: Deploy on Heroku

There is no step 7. By end of the previous step, Heroku installs the required libraries and deploys the app. It returns the URL for your application.

