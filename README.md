# Web Chat Application
## Technologies used:
**Backend:**
1. Django

**Frontend:**
1. JavaScript
2. HTML 
3. CSS
4. Bootstrap

**Database:**
1. MySQL Lite

A short video in which I showcase my project: https://youtu.be/SyBDWVyyfa4

## Project Description:
This is a Real Time Web Chat Application. For real time communication between server and client Websocket are implemented using Django Channels package which allows to use WebSockets and other non-HTTP protocols in the Django site. The regular http requests and javascript fetch api are also used in this project.

This app allows user to do text chatting with other users individually or do group text chatting with many users. Users have the option to create new groups add contacts to their groups and assign any of the group member admin rights to the group. The admins of the group will be able to add or remove group members just like in Whatsapp.

## Files Description:
**These are some of the new files which are not found in regular Django project:**

1. **routing.py**: 
this file is a Django Channels routing configuration that is similar to a Django url.py file, in that it tells Channels what code to run when a websocket connection request is received by the Channels server.

2. **Consumers.py**: 
When Django accepts an HTTP request, it consults the root url.py to lookup a view function, and then calls the view function to handle the request. Similarly, when Channels accepts a WebSocket connection, it consults the routing.py file to lookup a consumer, and then calls various functions on the consumer to handle events from the connection. So, this file contains all the methods to handle the websocket connections for example a method for handling incoming message from a client would transfer the message to the recipient group or individual and simultaneously save the message in the database all this would be happening in real time.

The rest of the files are same as in regular Django project

3. **Views.py**: 
It contains 11 methods to handle all the http requests and the fetch requests from javascript for example addcontact and register method.

4. **models.py**:
It contains total 8 models including the user model.

      1. user
      2. contacts
      3. groups
      4. groupcontact
      5. usermessages
      6. notifications
      7. groupadmin
      8. groupcreator
      
5. **Templates/Chat folder**:
This folder contains all the html files for each page including the layout.html

    1. index.html: 
    This is the index page where user can see all his contacts and groups and can create new group or add new contact. <br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Index_page.png?raw=true)<br/><br/>
    2. group.html:
    This is the group_chat page where user can see all the group chat and send text to group<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Group_chat_page1.png?raw=true)<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Group_chat_page2.png?raw=true)<br/><br/>
    4. login.html:
    This is the login page<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Login_page.png?raw=true)<br/><br/>
    5. register.html:
    This is the register page<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Register_page.png?raw=true)<br/><br/>
    6. room.html:
    One to One chat page<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Chatting_page.png?raw=true)<br/><br/>
    7. setting.html:
    Group Settings page<br/><br/>
    ![index page](https://github.com/ahmadrazakhawaja/chat-application/blob/master/cs50-web-screenshots/Group_settings_page.png?raw=true)<br/><br/>

6. **static/chat folder**:
This folder contains the styles.css stylesheet for the entire site and the **very important chat.js** javascript file which contains the code to initiate the websockets and use fetch api at the client side and handle all client side interactivity. Bootstrap is also used to style the frontend and make it mobile responsive although not which focus is given to styling and asthetics as more focus was on backend services and on handling all the data in real time.

A channel layer is used in this app which allows multiple consumer instances to talk with each other, and with other parts of Django. We will use a channel layer that uses Redis as its backing store. Each client that connects to the application is assigned a unique channel name through which he is communicated all the receiving messages.

## How to Run the Application
`git clone https://github.com/ESWZY/cs50web-final-project.git`

`cd cs50web-final-project`

`pip install -r requirements.txt`

In order to run this app locally we need to start a redis server. I start the redis server inside docker container using the command:

`docker run -p 6379:6379 -d redis:5`

After redis server has started then you can normally start the app using the command:

`Python3 manage.py runserver`

Run these following commands to migrate database.

`python manage.py makemigrations`

`python manage.py migrate`


## Deployment

The application is deployable to Heroku. But we have to change the Database from SQL Lite to Heroku Post gre SQL. We also need redis store for channel layer for that we can use the Heroku Redis addon. Since redis addon requires a verified account on Heroku using the credit card details I was not able to use the addon and hence The Websocket Functionality is currently not active hence messages cant be delivered.

Here is the link to deployed website: https://cs50wchat.herokuapp.com/

Please note that currently messaging service is not active because I can’t use the Heroku Redis addon.
