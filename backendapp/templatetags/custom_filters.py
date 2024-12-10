from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    key_list = list(obj.keys())
    index_of_id = key_list.index(attr_name)
    print(str(obj[key_list[index_of_id]]) + " is the answer.")
    return (obj[key_list[index_of_id]]) 

@register.filter(name='add_class')
def add_class(field, css_class):
    """Adds a CSS class to a form field widget."""
    return field.as_widget(attrs={"class": css_class})

@register.filter
def add_attr(field, attr):
    attrs = {}
    definition = attr.split(',')
    for d in definition:
        key, val = d.split('=')
        attrs[key] = val
    return field.as_widget(attrs=attrs)