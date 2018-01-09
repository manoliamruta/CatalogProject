README.md
-----------------------------------------------------------------------
Project Description
-----------------------------------------------------------------------
This project is a web application that provides a list of items within 
a variety of categories and integrated third party user registration 
and authentication. Authenticated users have the ability to add, 
edit, and delete their own items.


-----------------------------------------------------------------------
Dependencies
-----------------------------------------------------------------------

1.  Install Vagrant and VirtualBox. 
2.  Clone the catalog project.
3.  Launch the Vagrant VM (by typing vagrant up in the directory 
    /vagrant from the terminal).
4.  Type vagrant ssh to log in to VM.
5.  Type cd /vagrant/.
6.  Move to the catalog directory by using cd catalog.

-----------------------------------------------------------------------
View Catalog App
-----------------------------------------------------------------------

1.  Execute the database_setup.py file by typing python 
    database_setup.py at the prompt.
2.  Execute the lotsofitems.py file by typing python lotsofitems.py 
    at the prompt.
3.  Execute the application.py file by typing python application.py 
    at the prompt.
4.  Open browser and visit the http://localhost:8000 to access the 
    Catalog App.
5.  When a user adds a Category, their is a image field. They can 
    download the image and place it in the /static folder and then 
    specify the path as /static/filename in the field provided.

