import re
from django.utils.safestring import mark_safe
from django import template
register = template.Library()


class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')


# from djangosnippets.org/snippets/2253/
@register.filter
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class), match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class,
                                          string))
    else:
        return mark_safe(string.replace('>', ' class="%s">' % css_class))
    return value


@register.filter
def set_placeholder(value, placeholder):
    string = unicode(value)
    if 'placeholder' in string:
        return value
    return mark_safe(string.replace('>', ' placeholder="%s">' % placeholder))
