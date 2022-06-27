## MVT Framework
  1. Model - Data Access Layer
      1. Data Objects for the database(ORM)
  2. Template - Presentation Layer
      1. What The User Sees
  3. View - Business Logic
      1. Urls Send HTTPResponse
      2. Views REspond with HTTP Request
## Files
1. wsgi.py - webserver gateway interface - actual server
2. urls.py - url routing to project
   1. project urls.py use `include` function from `django.urls` to inlclude the urls.py file for an application
   2. if there are id endpoints, that must be passed to the view as a paramenter
3. asgi - asynchronous calls
4. settings.py - core project ocnfiguration regarding app installs, urls formatting,database formatting, etc 
   1. Update application definitions in `INSTALLED_APPS` for example, `base.apps.BaseConfig`
      ```    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
      ```

## App Files

1. `views.py` - where your application views go
   1. use render to render templates to views
   2. On saving models you can use form save or the create option for the model
      1. 
2. `apps.py` - provides application configuration
   1. app will have its own views that are passed here from `base.views.View`
3. `urls.py` - where your url patterns for the app resides, configuration endpoint with views
   1. `path('room/<str:pk>/', views.room, name="room")` -- name allows us to change the path without updating the template. use name when loading url href. ex. `"{% url 'user-profile' room.host.id %}"`
4. `models.py` - where your orm for django database will reside
   1. Datatypes
      1. `CharField(max_length=200)`
      2. `TextField(null=True, blank=True)`
      3. `DateTimeField(auto_now=True)` - auto updates date field on text
         1. `auto_now_add=True` - timestamp set when created
      4. `models.ForeignKey(Room, on_delete=models.CASCADE)` - adding a foreign key for a many to one relationship established by child model
      5. you can query the foreign key that is connected to the object you query
      6. can fetch set of child as follows: `messages = Room.message_set.all()`
5. `admin.py` - where you register your models to site so you can view it in admin dashboard
6. `forms.py` - similar to django serializers, you create meta and specify fields
   1. create user creation form that overrides forms or inherits from them. These can be imported into your views

## Templates Directory in Root

1. Where your template directory is for your html/css
   1. Make sure to update `TEMPLATES` configuration in project `settings.py`
2. Template Inheritence
   1. create a html template and then use include to use it on other html pages
      1. `{% include 'navbar.html' %}`
      2. Split divs into component htmls that can be included in other page content
   2. main.html where common includes exist
      1. `{% extends 'main.html' %}`
3. App templates
   1. Must create template folder/{name of app} - required
      1. specify app folder in template in
         1. ``render(request, 'base/home.html', {'rooms': rooms})``
4. Main templates
   1. reusuable stuff for project that are extended in app templates
5. Block content 
   1. create common content in main.html and use the block content specifically to add items in relation for your page or child content
   2. `{{request.META.HTTP_REFERER}}` - redirects to where they came from

### Django Templates

1. variables - two curly braces, `{{}}`
2. Tags - loops, logic, filters. csrf_token `{%%}`
   1. `{{% for x in render_variable %}}`
3. Can pass variables using render function
   1. `render(request, 'home.html', {'rooms': rooms})`
4. Concatenate url
   1. `"{% url 'delete-room' room.id %}"`
5. Query URL
   1. `"{% url 'home' %}?q={{topic.name}}"`
6. Query filter requires input 
   1. View requires the following
```python 
   q = request.GET.get('q') if request.GET.get('q') != None else ''
   rooms = Room.objects.filter(
      Q(topic__name__icontains=q) | 
      Q(name__icontains=q) |
      Q(description__icontains=q))
```
# set input as place holder for searches to filter
```html
<form method="GET" action="{% url 'home' %}">
    <input type="text" name="q" placeholder="Search Rooms..."/>
</form>

```
# HREF a query for search bar
```html
<a href="{% url 'home' %}?q={{topic.name}}">{{topic.name}}</a>
```

## Commands

  1. `django-admin` - shows subcommands 
  2. `django-admin startproject <name_of_project>` - creates project
  3. `python manage.py startapp <name_of_app>` - creates application
  4. `python manage.py runserver` - runs application
  5. `python manage.py makemigrations` - when changes are made to model or view (stages migrations)
  6. `python manage.py migrate` - migrate changes
     1. builds database for us
  7. `python manage.py createsuperuser` - creates superuser


## Order of operations
1. Create a Model
2. Migrate the model
3. Create response views which can be either views, view templates, or functional views
4. Specify urls that match response view function requirements
   1. id will have id parameter for response
5. Create template for the view at application level
   1. leverage template inheritence and ability to pass context from render


## Authentication

1. Django built in session
2. Navigate to chrome console and go to `application->cookies` to view session
3. Do not call login view as login as it is a function in django
4. `from django.contrib.auth.decorators import login_required` if user is not logged in add this decorator
5. Steps completed
   1. Create login and logout page and views
   2. Check if authenticated in both views and templates
   3. Show info or template componants based on auth status
   4. redirect when user is authenticated or if user requires auth for that page
   5. use context for login and registration options

## chat crud

1. Steps completed
   1. Create POST options to get inputs for messages
2. Haven't complted
   1. Option to edit messages

## django messages

1. `from django.contrib import messages`
2. `https://docs.djangoproject.com/en/4.0/ref/contrib/messages/`


## Static files

1. Like Templates create root static files with styles and image folder
2. Create a variable `STATICFILES_DIRS = [BASE_DIR / 'static']` in settings.json
3. load static using following: `{% load static %}` and must be set for each main template html page to use static folder. everything else will be configured via `block content`
4. reference stylesheet similar to url and template `    <link rel="stylesheet" type='text/css' media='screen' href="{% static 'styles/main.css' %}">` 
5. To add images `<img src="{% static 'images/image.png' %}">`
6. To add user upload images


## Prebuilt Templates



```html
<div class="form__group">
<label for="room_topic">Enter a Topic</label>
{% comment %} List topic for dropdown which must match datalist id {% endcomment %}
<input required name="topic" type="text" value="{{room.topic.name}}" list="topic-list" />
<datalist id="topic-list">
   <select id="room_topic">
      {% for topic in topics %}
      <option value="{{topic.name}}">{{topic.name}}</option>
      {% endfor %}
   </select>
</datalist>
</div>
```

## DRF

1. Can create a new application or a new folder in existing app called `api` which includes
   1. `views.py` - 
   2. `__init__.py`
   3. `urls.py` - api paths that are added to project urls
   4. `serializers.py` - similar to model form 
2. `pip install djangorestframework` and add `rest_framework` to `settings.json` of project

## Uploading images
1. PIP install pillow
2. ` <form class="form" method="POST" action="" enctype="multipart/form-data">` - enctype must be specified to upload image
3. `form = UserForm(request.POST, request.FILES, instance=user)` - request files from image