from django.urls import path
import pro_commerce.views
from pro_commerce.views import custom_404_view  # Assurez-vous que cette vue existe dans views.py
from django.conf.urls.static import static
from django.conf import settings

# Gestion de l'erreur 404
handler404 = custom_404_view

app_name = "pro_commerce"

urlpatterns = [
    path('', pro_commerce.views.homepage, name='homepage'),
    path('details/product/<int:product_id>/', pro_commerce.views.detail, name='product_detail'),
    path('contact/', pro_commerce.views.contacts, name='contact'),  # Ajout du '/' final
    path('apropos/', pro_commerce.views.about, name='apropos'),  # Ajout du '/' final

    path('categorie/<slug:category_slug>/', pro_commerce.views.products_by_category, name='products_by_category'),
    path('sous-categorie/<slug:subcategory_slug>/', pro_commerce.views.products_by_subcategory, name='products_by_subcategory'),
    path('toggle-favorite/<int:product_id>/', pro_commerce.views.favorite, name='toggle_favorite'),
    path('favorites/', pro_commerce.views.favorite_list, name='liste_favoris'),
    path('annonce/', pro_commerce.views.annonce, name='annonce'),

    # ------------------------------------------------------------------------------
    # PRODUCT
    # ------------------------------------------------------------------------------
    path('add-product/', pro_commerce.views.add_product, name='add_product'),
    path('<int:pk>/update/', pro_commerce.views.product_update, name='update_product'),
    path('<int:pk>/delete/', pro_commerce.views.product_delete, name='delete_product'),
    path('dashboard_seller/', pro_commerce.views.product_admin, name='dashboard'),

    # ------------------------------------------------------------------------------
    # ADRESSE
    # ------------------------------------------------------------------------------
    path('create/', pro_commerce.views.adresse_create, name='create_adresse'),
    path('addresses/', pro_commerce.views.user_addresses, name='user_addresses'),
    path('addresses/create/', pro_commerce.views.adresse_create, name='create_adresse'),
    path('addresses/update/<int:pk>/', pro_commerce.views.update_address, name='update_adresse'),
    path('addresses/delete/<int:pk>/', pro_commerce.views.delete_address, name='delete_adresse'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
