from django.core.exceptions import ValidationError

def validate_nonzero(value):
    if value == 0:
        raise ValidationError(
            ('Quantity %(value)s is not allowed'),
            params={'value': value},
        )