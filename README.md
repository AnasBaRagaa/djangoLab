# djangoLab
Using CBV for the CMP416 lab11&amp;12


Hello guys

For the new Django users that are using Django for the project ,like myself, I found extremely helpful to use class based views (CBV) for all the CRUD functionalities.
Unfortunately we only covered Detail and list view in class. With CBVs, you do not need to create html form or worry about any database operations, You can have your entire view with 5 lines of code. However, the challenging part was that we might need to not show all the model fields in the form, for example the owner field, so the solution to this problem was having a form class with minimal code and specifying the fields there and customizing the lock for the fields if needed. 
Another problem is that the form looks ugly with standard html, so I used django-crispy-forms and it does all the work with one line for you. 
I found also extremely helpful to have your own CBVs base classes for your own customization, for example enforcing login and check if the user is the owner of the record, and extend them for each view needed with minimal code. 
I am sorry if my explanation is not clear but I put everything in a Django project based on the last lab and you can go over it and see it in action with the commented code. I am not an expert so not everything is correct. I used multiple sources. Also, this might not helpful for your project but in my case it saved me hundreds  of liens

Note:
The lab code is inside 'phonebook'


'django_countries' is an   open source package from : https://pypi.org/project/django-countries/

'widget_tweaks' is an   open source package : https://pypi.org/project/django-widget-tweaks/

'crispy_forms'is an   open source package from : https://pypi.org/project/django-crispy-forms/#description
    

