from django import template
register = template.Library()


def filter_key(value):
    if "shit" in value:
        return "error"
    else:
        return value.upper()
register.filter(filter_key)


def  test(value):
    if "test" in value:
        value = "not_null"
        return value
    else:
        return value.lower()
register.filter(test)