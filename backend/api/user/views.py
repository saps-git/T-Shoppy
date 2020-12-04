from rest_framework import viewsets
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re
from rest_framework.permissions import AllowAny
# Create your views here.

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range (97, 123)] + [str(i) for i in range (10)]) for _ in range(length))

@csrf_exempt #adding the csrf token to allow request from other origin(React)
def signin(request):
    if not request.method == 'POST': #if method not POST, error
        return JsonResponse({'error': 'Send a post request with a valid parameter'})
    
    # put email and password in variables
    username = request.POST['email'] 
    password = request.POST['password']

    print(username)
    print(password)

    #validation of username and password to allow to login
    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username): #if username doesn't matches the Regex, error
        return JsonResponse({'error':'Enter a valid mail'})

    if len(password) < 3:
        return JsonResponse({'error':'Password needs to be atleast 3 charecters'})

    UserModel = get_user_model() #user model from djnago.contirb.auth, to fetch the models

    try:
        user = UserModel.objects.get(email=username) #taking the object whose email matches the request username, if there's none then except

        if user.check_password(password): #checking the password with check_password method. if not then error below
            usr_dict = UserModel.objects.filter(email=username).values().first() #passing all the values of the object of the requested username in usr_dict
            usr_dict.pop('password') #poppin the password parameter as we don't want to pass it forward

            #checking the session token
            if user.session_token != "0": #if session token is not zero, means already logged in
                user.session_token = "0" #make the session token zero
                user.save() #save
                return JsonResponse({'error':'Previous session exist'}) #error message

            #if session token is zero, that is if not logged in
            token = generate_session_token() #generate a token from the above defined method
            user.session_token = token #setting the token
            user.save()
            login(request, user) #logging in the user
            return JsonResponse({'token':token, 'user':usr_dict}) #passing the token and the user details

        else:
            return JsonResponse({'error':'Invalid Passwords'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid Email'})

def signout(request, id): #id is passed so after the logout, with the help of the id, we can make changes to the DB, like making the session_token 0
    logout(request) #loging out

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id) #grabbing the object by the id
        user.session_token = "0" #setting the session_token to 0
        user.save() 
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid user ID'})

    return JsonResponse({'success':'Logout success'}) #after session token is 0, return success message

class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]