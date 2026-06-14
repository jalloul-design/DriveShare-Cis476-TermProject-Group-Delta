
Diagram 1: Class Diagram(User)
Description: This class diagram shows the structure of the authencation module for our Driveshare. 
It contains three main parts, The user class which stores the user information, the session manager class which 
is the singleton, tracks the current logged in user across the entire application. Last we have the 
Security questions which is our abstract class along with its three concrete subclasses which forms
the Chain for password recovery. 

![Class Diagram](class_diagram.png)

Diagram 2: Sequence Diagram(User Registration):
Description: Traces the flow of a new user registering. The form data goes from register.html -> routes.py -> registration.py, which checks if the email exists, then calls User.create_account() to hash the password and insert the new user into the database.
