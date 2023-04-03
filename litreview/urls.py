"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
from django.conf import settings
from django.conf.urls.static import static
import reviews.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='home'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket/', reviews.views.ticket_create, name='ticket_create'),
    path('tickets/<int:ticket_id>/change/', reviews.views.ticket_update, name='ticket_update'),
    path('tickets/<int:ticket_id>/delete/', reviews.views.ticket_delete, name='ticket_delete'),
    path('review/', reviews.views.review_create, name='review_create'),
    path('reviews/<int:ticket_id>/create', reviews.views.review_create_from_ticket, name='review_from_ticket'),
    path('reviews/<int:review_id>/change/', reviews.views.review_update, name='review_update'),
    path('reviews/<int:review_id>/delete/', reviews.views.review_delete, name='review_delete'),
    path('feed/', reviews.views.feed, name='feed'),
    path('subscriptions/', reviews.views.user_follows, name='subscriptions'),
    path('subscriptions/<int:followed_id>/unfollow', reviews.views.unfollow, name='unfollow'),
    path('search-user/', reviews.views.search_user, name='search-user'),
    path('search-user/<int:user_id>/follow', reviews.views.follow, name='follow'),
    path('posts/', reviews.views.posts, name='my_posts'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
