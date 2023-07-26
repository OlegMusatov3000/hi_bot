from collections import Counter

from django import template

register = template.Library()


@register.simple_tag()
def get_favorite_command(objects):
    objects_list = [obj.get_command_response_display() for obj in objects]
    num_of_uses, fav_com = max(
        (count, value) for value, count in Counter(objects_list).items()
    )
    return num_of_uses, fav_com