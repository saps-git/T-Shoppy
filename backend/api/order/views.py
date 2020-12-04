from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer
from .models import Order
from django.views.decorators.csrf import csrf_exempt

def validate_user_session(id, token): #function to validate user session (if he's logged in or not)
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk = id)
        if user.sessio_token == token:
            return True
        return False

    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def add(request, id, token): #to add items to cart
    if not validate_user_session(id, token): #calling function defined above to check if user session is validated or not
        return JsonResponse({'error':'Please re-login','code':'1'})
    
    if request.method == "POST":
        #extracting info from the request
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']

        total_pro = len(products.split(',')[:-1]) #splitting the products name with ','

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error' : 'User does not exist'})

        ordr = Order(user=user, product_names=products, total_products=total_pro, transaction_id=transaction_id, total_amount=amount)
        ordr.save()
        return JsonResponse({'success':True, 'error':False, 'mag':'Order Placed Successfully'})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer