from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Movie, Review, ReviewReport
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie, is_hidden=False).order_by('-date')
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)



@login_required
def report_review(request, id, review_id):
    if request.method != 'POST':
        return redirect('movies.show', id=id)

    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, movie=movie)

    # Optional: prevent self-reporting
    if review.user_id == request.user.id:
        messages.warning(request, "You cannot report your own review.")
        return redirect('movies.show', id=id)

    reason = request.POST.get('reason', '').strip()

    report, created = ReviewReport.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'reason': reason}
    )

    if created:
        review.is_hidden = True
        review.save(update_fields=['is_hidden'])
        messages.success(request, "Thanks—this review has been reported and is now hidden.")
    else:
        messages.info(request, "You already reported this review.")

    return redirect('movies.show', id=id)