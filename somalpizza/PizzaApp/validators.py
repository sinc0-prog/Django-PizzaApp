from django.core.exceptions import ValidationError


def valid_pizza_name(name):
    if name == "":
        raise ValidationError("Name of pizza is required")


