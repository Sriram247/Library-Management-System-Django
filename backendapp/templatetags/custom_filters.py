from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    key_list = list(obj.keys())
    index_of_id = key_list.index(attr_name)
    print(str(obj[key_list[index_of_id]]) + " is the answer.")
    return (obj[key_list[index_of_id]]) 
