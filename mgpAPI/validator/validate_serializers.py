from django.core.exceptions import ValidationError
from transactions.models import InputDetail, WithdrawDetail, AdjustDetail, ScrapDetail, ReturnDetail
from products.models import Product
from conclusion.models import Outage, ManufacturingTransaction, ManufacturingTransactionLine, PowerGeneration
from units.models import Unit
from common.master_models import Sector


def validate_check_input_transaction_pk(value):
    try:
        InputDetail.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_withdraw_transaction_pk(value):
    try:
        WithdrawDetail.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_adjust_transaction_pk(value):
    try:
        AdjustDetail.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_scrap_transaction_pk(value):
    try:
        ScrapDetail.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_return_transaction_pk(value):
    try:
        ReturnDetail.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_sector_pk(value):
    try:
        Sector.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_product_pk(value):
    try:
        Product.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_unit_pk(value):
    try:
        Unit.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )


def validate_check_outage_pk(value):
    try:
        Outage.objects.get(id=value)
    except Exception as e:
        raise ValidationError(
            ('Not found %(value)s is pk'),
            params={'value': value},
        )
