from django import template
register = template.Library()

@register.simple_tag()
def username_modify(user):
    # print(user+"<<<Here we are geting the username")
    if user != None:
        user.username = str(user.username) + "12345"
    return user
