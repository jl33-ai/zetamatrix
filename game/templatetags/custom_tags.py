from django import template

register = template.Library()

@register.inclusion_tag('components/titleinfo.html')
def titleinfo(title, num_contributions, home_url="/game/"):
    info_list = [
        f"Made of {num_contributions} answered questions",
        "Please note that the values are the log_e(·) of the real values"
    ]
    return {
        'title': title,
        'info_list': info_list,
        'home_url': home_url
    }