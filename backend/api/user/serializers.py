from rest_framework import serializers
from django.contrib.auth.hashers import make_password #for hashing passwords
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser

class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data): #data incoming from the front end, to create a user
        password = validated_data.pop('password', None) #popping the 'password' key and it's value pair from the validated data dictionary, as password has to be set differently
        instance = self.Meta.model(**validated_data) #unpacking all the required key value pairs from the dictionary(validated_data) in variable instance, as defined by the self.Meta.model below(fields in Meta class in the last)

        if instance is not None: #since it is validated from views, hence if it is not none
            instance.set_password(password) #using 'set_password' method to set the password of the user
        instance.save() #saving the instance in the DB
        return instance

    def update(self, instance, validated_data): #data incoming from the front end, to update any field of a user
        for attr, value in validated_data.items(): # for all the attr, values in the dict(validated_data), accessed by .items() method
            if attr == 'password': # if the attr is password
                instance.set_password(value) #then save the value (passowrd) via the set_password 
            else:
                setattr(instance, attr, value) #for all other methods save by setattr method
            
        instance.save() #saving the instance in the DB
        return instance


    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only':True}} #extra_kwargs = extra parameter that we want to modify in the DB, here we set the password to write_only
        fields = ('name', 'email', 'password', 'phone', 'gender', 'is_active', 'is_staff', 'is_superuser') #'is_active', 'is_staff', 'is_superuser' inherited from parent class