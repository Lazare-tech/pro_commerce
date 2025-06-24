from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404
from pro_commerce.models import *
from rating.models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.



####################
@login_required
def rate(request, product_id: int, rating: int):
    product = get_object_or_404(Product, id=product_id)
    review, created = ReviewRating.objects.update_or_create(
        produit=product,
        user=request.user,
        defaults={'rating': rating}
    )
    if not created:
        review.save()  # Save the review if it was updated
    return redirect('pro_commerce:product_detail', product_id=product_id)

####################
def rate(request, service_id: int, rating: int) -> HttpResponse:
    post = Product.objects.get(id=service_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return render(request,'pro_commerce/pro_commerce/base.html')
####################
####################
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.produit = product
            review.user = request.user
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()
            messages.success(request, 'Votre commentaire a été ajouté.')
            return redirect('pro_commerce:product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'pro_commerce:add_review.html', {'form': form, 'product': product})

####################
@login_required

def edit_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id)  # Récupérer l'avis à modifier
    product_id = review.produit.id  # Récupérer l'ID du produit

    
    if request.method == 'POST':
        # Récupérer le contenu du formulaire
        content = request.POST.get('content')

        # Mettre à jour l'avis
        review.review = content  # Met à jour le contenu de l'avis
        review.save()  # Sauvegarder les modifications dans la base de données

        # Rediriger vers la page de détail du produit après la sauvegarde
        return redirect('pro_commerce:product_detail', product_id=product_id)

    # Pour une requête GET, rediriger vers la page de détail du produit sans faire de modification
    return redirect('pro_commerce:product_detail', product_id=product_id)

# ####################
@login_required


def delete_review(request, review_id):
    # Récupérer l'avis ou lever une erreur 404 s'il n'existe pas
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)  
    product_id = review.produit.id  # Récupérer l'ID du produit
    review.delete()  # Supprimer l'avis
    messages.success(request, 'Votre commentaire a été supprimé.')  # Message de succès
    return redirect('pro_commerce:product_detail', product_id=product_id)  # Redirection vers le détail du produit
    # Si la méthode n'est pas POST, ne rien rendre ici (il est supposé que l'utilisateur clique sur le lien de suppression)
