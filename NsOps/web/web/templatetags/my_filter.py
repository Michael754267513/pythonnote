from django import template
register = template.Library()


def test(value): # Only one argument.
    "Converts a string into all lowercase"
    return value.upper()
register.filter(test)

def upa(values):
    return values*100
register.filter(upa)