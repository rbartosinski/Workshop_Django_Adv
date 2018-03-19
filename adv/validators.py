from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_year(value):
    if not 2000 <= value <= 2004:
        raise ValidationError("{} nie mieści się w przedziale 2000-2004!".format(value))


def validate_range(_min, _max):
    def innerValidate(value):
        if not _min <= value <= _max:
            raise ValidationError("{} nie mieści się w przedziale {}-{}!".format(value, _min, _max))
    return innerValidate


def validate_username(value):
    try:
        User.objects.get(username=value)
        raise ValidationError('Użytkownik o nazwie {} już istnieje!'.format(value))
    except User.DoesNotExist:
        pass