from django.contrib import admin
from .models import ReviewRating

# # Register your models here.
# class ReviewRatingAdmin(admin.ModelAdmin):
#     list_display=['produit','user','subject','review','rating','ip','status','created_at','updated_at']
# admin.site.register(ReviewRating,ReviewRatingAdmin)
# #

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user','review', 'produit', 'rating', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'user__username', 'produit__header')
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status=True)
    approve_comments.short_description = 'Approuver les commentaires sélectionnés'

    def disapprove_comments(self, request, queryset):
        queryset.update(status=False)
    disapprove_comments.short_description = 'Désapprouver les commentaires sélectionnés'

admin.site.register(ReviewRating, ReviewRatingAdmin)