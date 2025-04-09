## Introduction ##
Newspaper is a Django web application, which manages newspapers for any organisation using them, i.e. a society, newscompany. It provides a section for visitors to view and download the main copy of the paper at that particular time. In addition, it provides previous copies that the visitor may want to view. Newspaper has a content manager system for normal users, which comprises of a section to upload, delete and select the main paper. Users may also change their passcode, initially from the default password, to whatever they wish. Newspaper has an administration system, where staff users have the ability to create and delete accounts, as well as rest user passwords.

## Distinctiveness and Complexity ##

### API Backend ###

- The API is made using django_rest_framework, unlike using a premade backend as in the course. This further builds upon what was used in the course, where the API was made using calls to Django's normal views and using Django's inbuilt JsonResponse to reply requests. With django_rest_framework the serialization was done using rest_frameworks's ModelSerializer class to make the serializers used in the response. In views.py, there is the use of Class-Based views (for the Accounts) as opposed to function based views that were being used throughout the course. This also restricted API calls to only Admin users, using Django's standard model permissions. In addition, django_rest decorators are used throughout. 

### API Frontend ###

- For the frontend I used the axios library to perform all the API calls. Unlike the course, where we used the csrf_exempt token, the csrf token, it is obtained using the method outlined in Django's documentation, is included in the headeers of the requests made to the API. The functions used are also Async-await functions in order for the next item to only be done when a response from the API is received.

### React in the Frontend ###

- Unlike the course, where are link was used to include react in the frontend, I have used React's recommended way of setting up a modular Javascript Environment using Vite and django-vite-plugin. Vite was configured using vite.config.js using Vite's official documentation and django-vite-plugin's documentation, as well as package.json according to vite's documentation. Roots were then used in all the jsx files in order to render different components coming from API calls. A consequence of this is 2 terminal environments are needed to run the application, one for the backend and the other for the frontend

### Database ###

- The application uses a PostrgeSQL, which is a production level database, as opposed to the default SQLite database used by Django. The database is configured according to Django's documentation in settings.py and works similar to how SQLite would due to Django's functionality. In settings.py all the sensitive information pertaining to the website use environment variables in order to not compromise security. The environment variables are loaded use load_dotenv() from dotenv module. The environemnt variables are stored in .env, which is not committed.

### Forms ###

- All the forms use crispy_forms on top of Django's Forms class to get bootstrap like forms without having to change any html. FormHelper() controls the rendering behavior of the form passed to the {% crispy %} tags, this is different to just the normal {{ example_form }} tags that were used in the normal Forms class. The class also allows inclusion buttons etc. placed in the python part of the form rather than the html, as shown in the example below
``` 
class newUserForm(forms.Form):
    username = forms.CharField()
    admin = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('newuser')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Submit'))
```

### Media File Handling ###

- The web application also manages media files, specifically pdfs, as part of the uploading and deleting newspaper articles. In urls.py the media roots are also added (in the way meant for development and not production). The file locations are stored using the file field in the Models class. This are then displayed using ```<iframe>``` with the pdf roots as the source. Different files are shown as the main file in the frame on the main page.

### Other Requirements ###

-  The web application is mobile responsive using ```     <meta name="viewport" content="width=device-width, initial-scale=1">```
- There are 2 models, papers and users.
- The web application uses django on the backend while using javascript on the backend
- Due to the additional features stated the project is more complext than previous projects

## Files ##

- **Vite.config.js** has the configuration for vite and for django_vite_plugin, including where all the static paths are.
- **Requirements.txt** contains all the python modules required by the application e.g. django_rest_framework and psycopg[binary] for PostgreSQL
- **package.json** contains dependencies required to fun the fronted of the project, the development dependencies and scripts required for running a building for production
- **.env** contains all the environment variables, that are to be hidden, there will be different for production and development

### Newspaper Subfolder ###
- **Settings.py** contains the configuration for our Django web application. Loading the environemnet variables, listing installed apps like theram and crispy_forms, holding the configuration to access the Postgre database, crispy_form settings, authentication settings, inlcuding the redirect url for unauthenticated users, and finally the X-Frame_Options to load the resource if request is from the same site.
- **urls.py** contains the admin urls and the urls for theram app.
- The rest of the files remain unchanged from when initially created by Django.

### Theram Subofolder ###

- **Admin.py** contains the models that should be registered for the Django Admin website i.e Users and Papers
- **Forms.py** contains 4 forms, all containing. NewPaper, which is used to upload files and submit those files. loginForm is used to login users into their accounts using username and password. passwordForm is used to change the users passwords. NewUser is used to create a new user with a username and a checkbox if they are a admin or not admin. All four of these classes have the self.helper attribute which is an instantiation of the FormHelper class. This attribute is used to set various parts of the form.
- **models.py** contains two models. Users which inherits Abstract User. Papers which contains a file field, paper, a boolean field, main (if true then this is the default main), a date time field for when the article was published.
- **serializers.py** Uses django_rest_frameworks ModelSerializer class. These have a limited access to information using ```fields``` to determine which fields can be accessed.
- **urls.py**  Contains urls for all the views and for the class views using ```views.ExampleClassView.as_view()``` as well as the media routes in  ```static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)```
- **views.py** contains the function index, returns the main page.  

    Login when receiving a get request, renders the login html template with the login_form. When Login receives a post request, it checks for a valid form, then sets a new password if the confirm password and password are the same and redirects back to the original url if any of the checks are failed. 

    Logout simply logs the user out.
    
    Change password returns the changepassword template, with the password form, if received a get request. If received a post request, changepassword checks if the form is valid. It then checks if the passwords are the same, then changing the passwords and authenticating the user to keep them logged in.
    
    The function new user requires not only the user be authenticated but the user be an admin user. For get requests, th template is returned along with the newuser form. For a post request, the form is chekced to be valid, then a check of the boolean value admin, if true a superuser is created if false a normal user is created.
    
    Accounts returns a template of accounts only for get requestsf.
    
    AccountsView is a class based view that handles the requests that come from the accounts page. A user needs to be admin authenticated in order to make requests to this view. If a get request, a list of all the users is returned. If a post request, the username is taken from the request and a new user is created, if a delete request, the username is taken from the request and the user is deleted.
    
    When a get request is sent to Collections it returns the html template with all the papers. When a post request is sent to collections, it checks if the user is authenticate then changes the boolean value for all the other papers to false, and the paper sent in the post request['main'] is set to true and made the main paper.

    The next function, latest, is part of the django_rest_framework api, when a call is received it returns the paper with main as true, which can be changed in collection but automatically set to the last uploaded paper.

    The last function, delete, returns all the papers when a get request is called. When a post request is called it deletes the paper in Post['main'] from the database and deletes from the folder where it is kept

- Templates  
    Accounts.html is where are shown in a table. And uses accounts.jsx through the vite tags
    
    Collection.html displays the papers. It slices the filename of the paper to use as the name displayed on the html page. For authenticated users there is a make main button that submits a hidden value.

    Delete.html contains a similar structure, but the form posted to delete view.

- Static  
    Accounts.jsx uses axios to fetch all the users in TableFunc, which uses the Async Await syntax in order to only form the table after the request is completed. There is an event listener for DOMContentLoaded that renders the TableFunc output in the root. GetCookie is obtained from Django's official documentation in order to obtain the csrf token. Reset user posts a request to the "api/accounts", sending the username in the post request. The delete user sends a delete request to "api/accounts/{username}", then calls TableFunc at the end to gwt the new updated table.

    In index.jsx, LatestPDF sends a get request to "/latest" and then returns an ```<iframe>``` and then renders the output in the root.

    Password.js has an event listener for value change on both ```<input>``` variables and checks if both match and only enables the button when both values are equal.

## Future Development ##
My aim is to make Newspaper production ready, using docker, kubernetes, production leve file storage like Amazon s3 and autotests then eventually hosting the website on a platform.

## Running application ##
1. pip install -r requirements.txt
2. npm install axios
3. npm install django-vite-plugin
3. npm run dev in one terminal
4. manage.py runserver in another terminal