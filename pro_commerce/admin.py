from django.contrib import admin
from .models import Category,Product,Adresse,User,Subcategory,UserFavorite, ProductVariant
from django.utils.safestring import mark_safe  # Importer mark_safe

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('username','password','telephone')
admin.site.register(User,UserAdmin)
#
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'ville','categorie', 'sous_categorie', 'utilisateur','adresse')
    list_filter = ('categorie', 'utilisateur')
    search_fields = ('nom', 'description')

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'photo','ville')
        }),
        ('Détails du produit', {
            'fields': ('prix', 'stock', 'categorie', 'sous_categorie', 'utilisateur','adresse')
        }),
    )
admin.site.register(Product, ProductAdmin)


#
class AdresseAdmin(admin.ModelAdmin):
    list_display=('ville','quartier','repere','contact','utilisateur')
admin.site.register(Adresse,AdresseAdmin)
#

class SubcategoryInline(admin.TabularInline):  # Vous pouvez utiliser StackedInline pour un affichage différent
    model = Subcategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom','slug','photo')
    search_fields = ('nom',)
    inlines = [SubcategoryInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)  # Si vous souhaitez également une entrée distincte pour les sous-catégories
#
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display=('user','product','added_at')
admin.site.register(UserFavorite,UserFavoriteAdmin)
#



# Admin pour les variantes de produits
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'thumbnail', 'photo_variant')
    list_filter = ('product',)  # Filtrer par produit
    search_fields = ('product__nom',)  # Recherche par nom du produit

    # Personnalisation de l'affichage dans le formulaire
    fieldsets = (
        (None, {
            'fields': ('product', 'photo_variant')
        }),
    )

    # Afficher une miniature de l'image dans la liste
    def thumbnail(self, obj):
        if obj.photo_variant:
            return mark_safe(f'<img src="{obj.photo_variant.url}" style="width: 50px; height: auto;" />')

        return ''
    thumbnail.short_description = 'Aperçu'
    thumbnail.allow_tags = True

    # Personnalisation de l'affichage
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si l'objet existe (modification)
            return ['photo_variant']  # Rendre photo_variant non modifiable
        return super().get_readonly_fields(request, obj)

    # Configurer l'affichage de la liste
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')  # Pré-charger le produit

    # Optionnel : Tri par défaut
    ordering = ('product',)