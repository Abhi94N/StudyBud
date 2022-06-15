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

## App Files

1. `views.py` - where your application views go
   1. use render to render templates to views
2. `apps.py` - provides application configuration
   1. app will have its own views that are passed here from `base.views.View`
3. `urls.py` - where your url patterns for the app resides, configuration endpoint with views
   1. `path('room/<str:pk>/', views.room, name="room")` -- name allows us to change the path without updating the template
4. `models.py` - where your orm for django database will reside
   1. Datatypes
      1. `CharField(max_length=200)`
      2. `TextField(null=True, blank=True)`
      3. `DateTimeField(auto_now=True)` - auto updates date field on text
         1. `auto_now_add=True` - timestamp set when created
      4. `models.ForeignKey(Room, on_delete=models.CASCADE)` - adding a foreign key for a many to one relationship established by child model
      5. you can query the foreign key that is connected to the object you query
5. `admin.py` - where you register your models to site so you can view it in admin dashboard
6. `forms.py` - similar to django serializers, you create meta and specify fields

## Templates Directory in Root

1. Where your template directory is for your html/css
   1. Make sure to update `TEMPLATES` configuration in project `settings.py`
2. Template Inheritence
   1. create a html template and then use include to use it on other html pages
      1. `{% include 'navbar.html' %}`
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