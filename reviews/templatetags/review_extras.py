from django import template

register = template.Library()


@register.filter  # custom filter to check the instance type, either ticket or review
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)  # custom template tags to display the author of the ticket/review
def get_poster_display(context, user):    # to improve the user experience
    if user == context['user']:
        return 'Vous avez'
    return f'{user.username} a'
