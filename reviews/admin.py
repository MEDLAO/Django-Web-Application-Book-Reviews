from django.contrib import admin
from .models import Ticket, Review, UserFollows

# we choose here how we want to display our models and data in the admin interface


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'headline', 'user')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows)
