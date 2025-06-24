from django.urls import path
import rating.views
from django.conf.urls.static import static
from django.conf import settings
#
app_name="rating"
urlpatterns = [

 path('product/<int:product_id>/add_review/', rating.views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', rating.views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', rating.views.delete_review, name='delete_review'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
