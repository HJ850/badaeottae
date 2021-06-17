'''
Created on 2021. 3. 25

@author: lyh77
'''
from rest_framework import serializers
from bada.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields=('test','id')