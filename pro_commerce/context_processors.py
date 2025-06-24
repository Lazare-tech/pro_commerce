from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Adresse, Category, Product,UserFavorite
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import AnonymousUser


def categories_processor(request):
    categories=Category.objects.all().prefetch_related('souscategories')

    return {'categories': categories}
#
def favorite_processor(request):
    
    if request.user.is_authenticated:
        favorite_products = UserFavorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_products=[]
    return{'favorite_products':favorite_products}
#
def paginator_processor(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 3)  # 20 produits par page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj':page_obj}
#

def admin_processor(request):
    products = []
    addresses = []

    # Vérifiez si l'utilisateur est authentifié avant de faire des requêtes
    if not isinstance(request.user, AnonymousUser):
        products = Product.objects.filter(utilisateur=request.user)
        addresses = Adresse.objects.filter(utilisateur=request.user)

    # Passez les produits et les adresses au contexte si l'utilisateur est authentifié
    context = {
        'products': products,
        'addresses': addresses,
    }
    
    return context