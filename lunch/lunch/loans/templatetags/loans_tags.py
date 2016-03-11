from django.template import Library

register = Library()


@register.filter
def deletable(loan, user):
    return loan.can_user_delete(user)