from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm, FollowForm
from .models import Ticket, UserFollows, Review
from itertools import chain
from django.db.models import CharField, Value
from django.core.paginator import Paginator

""" Function Based Views for reviews """


@login_required
def ticket_create(request):
    ticket_form = TicketForm()  # we include the ticket form

    if request.method == 'POST':  # check the request type
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():  # this method results in validation and cleaning of the form data
            ticket = ticket_form.save(commit=False)  # we don't save yet in the database
            ticket.user = request.user
            ticket.save()
            return redirect('feed')  # we redirect the user to the feed page using a name of view
    context = {
        'ticket_form': ticket_form,
        }
    return render(request, 'reviews/create_ticket.html', context=context)
# the context contains the data we will use in the template


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)  # prepopulate the form with an existing ticket
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
        # delete the ticket from the database with a Django built-in function
        ticket.delete()
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
            review.rating = review_form.cleaned_data['rating']  # after the validation process,
            review.body = review_form.cleaned_data['body']  # Django returns a dictionary which contains cleaned data
            review.save()
            return redirect('feed')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_review.html', context=context)


@login_required
def review_create_from_ticket(request, ticket_id):  # we use the ticket id to target the desired ticket
    review_form = ReviewForm()
    ticket = get_object_or_404(Ticket, id=ticket_id)  # returns the ticket corresponding to the id or an 404 error page

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket  # we define the ticket obtained as the ticket of the review
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
    return render(request, 'reviews/update_review.html', {'review_form': review_form, 'ticket': ticket, })


@login_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)  # necessary for GET and POST

    if request.method == 'POST':
        review.delete()
        return redirect('feed')

    return render(request, 'reviews/delete_review.html', {'review': review})


def get_users_viewable_reviews(connected_user):  # returns the reviews we want to display in the feed
    following = [elm.followed_user for elm in UserFollows.objects.filter(user=connected_user)]
    following.append(connected_user)
    reviews = Review.objects.filter(user__in=following)  # reviews of followed users

    my_tickets = Ticket.objects.filter(user=connected_user)
    reviews_to_my_tickets = Review.objects.filter(ticket__in=my_tickets)  # user reviews

    all_reviews = list(reviews) + list(reviews_to_my_tickets)
    all_ids = [elm.id for elm in all_reviews]
    return Review.objects.filter(id__in=all_ids)


def get_users_viewable_tickets(connected_user):  # returns the tickets we want to display in the feed
    following = [elm.followed_user for elm in UserFollows.objects.filter(user=connected_user)]
    following.append(connected_user)
    return Ticket.objects.filter(user__in=following)   # tickets of followed users


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # list of ticket ids that have a review in which the author of the ticket and the review is the same
    ids_same_user = [review.ticket.id for review in reviews if review.user == review.ticket.user]

    # if a user publishes a ticket and a review in one process, so we keep the review and the ticket,
    # but we don't display the ticket alone with exclude method
    tickets = get_users_viewable_tickets(request.user).exclude(id__in=ids_same_user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    tickets_and_reviews = sorted(chain(reviews, tickets),
                                 key=lambda tickets_and_reviews: tickets_and_reviews.time_created, reverse=True)

    # Paginator is a class that’s split an iterable or Queryset across several pages, with “Previous/Next” links
    paginator = Paginator(tickets_and_reviews, 5)  # the second argument is the number of posts displayed per page

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

    # we get the followers and the followed users by using a related name defined in the models
    # to access the related model from the reverse side of the relation
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
        searched = request.POST['searched']  # 'searched' is the username the user has written in the searchbar
        # Django QuerySet Field lookup, to get all users whose name are contained in searched
        users_to_follow = User.objects.filter(username__contains=searched)
        # and we pass searched and users_to_follow in the template
        return render(request, 'reviews/search_user.html', {'searched': searched, 'users_to_follow': users_to_follow})
    else:  # in the case of a GET method
        return render(request, 'reviews/search_user.html', {})


@login_required
def follow(request, user_id):
    user = request.user
    user_to_follow = User.objects.get(id=user_id)
    following = user.following.all()
    message = ''

    if request.method == 'POST':
        try:
            if user_to_follow.id != user.id:  # to ensure that the user doesn't follow himself
                UserFollows.objects.create(user=user, followed_user=user_to_follow)
                return redirect('subscriptions')
            else:
                message = 'Vous ne pouvez pas vous suivre vous-même.'
        except IntegrityError:  # because with unique_together in models , we cannot follow twice the same user
            message = 'Vous êtes déjà abonné à cet utilisateur.'
    return render(request, 'reviews/follow.html', {'user_to_follow': user_to_follow, 'message': message})


@login_required
def unfollow(request, followed_id):
    userfollows = UserFollows.objects.get(id=followed_id)  # we get the user we want to unfollow by his id

    if request.method == 'POST':
        # delete the followed from the database
        userfollows.delete()
        # then redirect to the subscriptions page
        return redirect('subscriptions')

    return render(request, 'reviews/unfollow.html', {'userfollows': userfollows})
