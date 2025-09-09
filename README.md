PWS Application : https://maharani-anindya-project2.pbp.cs.ui.ac.id/

1. Explain how you implemented the checklist above step-by-step
I started by creating a new Django project and an app main. after that, I register the main application on the project, by adding 'main' inside settings.py. Then, I add a urls.py file inside the main app, and link it in project2/urls.py with path('', include('main.urls')) so requests to the root URL are directed to the main application.
Next, I create a model in models.py called Product with all required attributes: name, price, description, thumbnail, category, is_featured. then, I ran makemigrations to create model migrations, ran migrate to apply migrations to the local database. 
After that, I registered the model in admin.py.
In views.py, I create a function called show_main to fetch all products from the database and include data such as the app name, my name, my class.
Then, I make a templates to loop through the product list and display each item. If none exist, loop through {% empty %} 
after that, I create routing in urls.py of the main app to map the function in views.py 
finally, using the PWS terminal, I ran migrate, and created a superuser. Then I logged in to /admin/ on the deployed site, added products, and confirmed the homepage displayed them.

2. Create a diagram showing the client request to the Django-based web application and its response, and explain the relationship between urls.py, views.py, models.py, and the HTML file in the diagram.

        HTTP Request         →     URLS (urls.py)
                                          ↓
Model (models.py) ← read/write data → views.py → HTTP Response (HTML)
                                          ↑
                                      main.html


3. Explain the role of settings.py in a Django project!
The settings.py file configures the Django project by defining apps, middleware, templates, database connections, static files, and security options. It serves as the project's main configuration, making sure the application works properly in both development and production settings. 

4. How does database migration work in Django?
In Django, migrations handle database schema updates. running makemigrations generates instructions based on model changes, and migrate applies them so the database stays consistent with the models. 

5. In your opinion, among all existing frameworks, why is the Django framework chosen as the starting point for learning software development?
Because it is beginner friendly, and it provides an all-in-one framework with built-in features such as ORM, authentication, and an admin interface, which makes it simpler for beginners to get started.

6. Do you have any feedback for the teaching assistant for Tutorial 1 that you previously completed?
The instructions were quite clear and easy to follow, which made it helpful for understanding the basics of Django. 
