'''
Created on 2021. 3. 25

@author: lyh77
'''

from django.urls import path, include

app_name='badaeottae'
urlpatterns = [
    path('',include('rest_framework.urls',namespace='rest_framework_category'))
]