from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm, FollowForm
from .models import Ticket, UserFollows, Review
from itertools import chain
from django.db.models import CharField, Value, Q
from django.core.paginator import Paginator


@login_required
def ticket_create(request):
    ticket_form = TicketForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    context = {
        'ticket_form': ticket_form,
        }
    return render(request, 'reviews/create_ticket.html', context=context)


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():

            form.save()
            return redirect('feed')
    return render(request, 'reviews/update_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le ticket de la base de données
        ticket.delete()
        # rediriger vers le flux
        return redirect('feed')

    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required
def review_create(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = review_form.cleaned_data['rating']
            review.body = review_form.cleaned_data['body']
            review.save()
            return redirect('feed')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_review.html', context=context)


@login_required
def review_create_from_ticket(request, ticket_id):
    review_form = ReviewForm()
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = review_form.cleaned_data['rating']
            review.body = review_form.cleaned_data['body']
            review.save()
            return redirect('feed')
    context = {'review_form': review_form, 'ticket': ticket, }
    return render(request, 'reviews/create_review_from_ticket.html', context=context)


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_form = ReviewForm(instance=review)
    ticket = review.ticket

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()
            return redirect('feed')
    return render(request, 'reviews/update_review.html', {'review_form': review_form,
                                                          'ticket': ticket,
                                                          })


@login_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        review.delete()
        # rediriger vers la liste des groupes
        return redirect('feed')

    return render(request, 'reviews/delete_review.html', {'review': review})


def get_users_viewable_reviews(connected_user):
    following = [elm.followed_user for elm in UserFollows.objects.filter(user=connected_user)]
    following.append(connected_user)
    reviews = Review.objects.filter(user__in=following)
    my_tickets = Ticket.objects.filter(user=connected_user)
    reviews_to_my_tickets = Review.objects.filter(ticket__in=my_tickets)
    all_reviews = list(reviews) + list(reviews_to_my_tickets)
    all_ids = [elm.id for elm in all_reviews]
    return Review.objects.filter(id__in=all_ids)


def get_users_viewable_tickets(connected_user):
    following = [elm.followed_user for elm in UserFollows.objects.filter(user=connected_user)]
    following.append(connected_user)
    return Ticket.objects.filter(user__in=following)


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    ids_same_user = [review.ticket.id for review in reviews if review.user == review.ticket.user]

    tickets = get_users_viewable_tickets(request.user).exclude(id__in=ids_same_user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    tickets_and_reviews = sorted(chain(reviews, tickets), key=lambda tickets_and_reviews: tickets_and_reviews.time_created, reverse=True)

    paginator = Paginator(tickets_and_reviews, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reviews/feed.html', context={'page_obj': page_obj})


@login_required
def posts(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    ids_same_user = [review.ticket.id for review in reviews if review.user == review.ticket.user]

    tickets = Ticket.objects.filter(user=request.user).exclude(id__in=ids_same_user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(chain(reviews, tickets), key=lambda posts: posts.time_created, reverse=True)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reviews/posts.html', context={'page_obj': page_obj})


@login_required
def user_follows(request):
    form = FollowForm()
    user = request.user
    followers = user.followed_by.all()
    following = user.following.all()

    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user_follows = form.save(commit=False)
            user_follows.user = user
            user_follows.save()
            return redirect('subscriptions')

    return render(request, 'reviews/subscriptions.html', context=locals())


@login_required
def search_user(request):

    if request.method == 'POST':
        searched = request.POST['searched']
        users_to_follow = User.objects.filter(username__contains=searched)

        return render(request, 'reviews/search_user.html', {'searched': searched, 'users_to_follow': users_to_follow})
    else:

        return render(request, 'reviews/search_user.html', {})


@login_required
def follow(request, user_id):
    user = request.user
    user_to_follow = User.objects.get(id=user_id)
    following = user.following.all()
    message = ''

    if request.method == 'POST':
        try:
            if user_to_follow.id != user.id :
                UserFollows.objects.create(user=user, followed_user=user_to_follow)
                return redirect('subscriptions')
            else:
                message = 'Vous ne pouvez pas vous suivre vous-même.'
        except IntegrityError:
            message = 'Vous êtes déjà abonné à cet utilisateur.'
    return render(request, 'reviews/follow.html', {'user_to_follow': user_to_follow, 'message': message})


@login_required
def unfollow(request, followed_id):
    userfollows = UserFollows.objects.get(id=followed_id)  # nécessaire pour GET et pour POST

    if request.method == 'POST':
        # supprimer le followed de la base de données
        userfollows.delete()
        # rediriger vers la liste des abonnements
        return redirect('subscriptions')

    return render(request, 'reviews/unfollow.html', {'userfollows': userfollows})
