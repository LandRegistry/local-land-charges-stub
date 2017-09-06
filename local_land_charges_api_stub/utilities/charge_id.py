from local_land_charges_api_stub.constants.charge_id import ChargeId
from local_land_charges_api_stub.exceptions import ApplicationError
import re


# TODO(unknown): This service is duplicated in the search-api any changes here should be mirrored there.
# TODO(unknown): Once the infrastructure is in place this service should be moved into a module and
# TODO(unknown): imported into this project.

def is_valid_charge_id(charge_id):
    """Returns true if the given charge_id has a valid format, false otherwise."""
    return re.match(ChargeId.IS_VALID_REGEX, charge_id)


def encode_charge_id(charge_id):
    """Encodes and returns the given charge id prefixed with ChargeId.PREFIX.

    Throws ApplicationError if charge_id is less than ChargeId.FLOOR or greater than ChargeId.CEILING.
    """
    encoded_charge_id = encode_base_31(charge_id)
    return add_prefix(encoded_charge_id)


def decode_charge_id(encoded_charge_id):
    """Removes the ChargeId.PREFIX and decodes the given charge id."""
    encoded_charge_id = remove_prefix(encoded_charge_id)
    return decode_base_31(encoded_charge_id)


def add_prefix(encoded_charge_id):
    """Takes an encoded charge id and adds the ChargeId.PREFIX."""
    return "{}{}".format(ChargeId.PREFIX, encoded_charge_id)


def remove_prefix(encoded_charge_id):
    """Takes an encoded charge id and removes the ChargeId.PREFIX."""
    return re.sub(ChargeId.PREFIX_REGEX, '', encoded_charge_id)


def encode_base_31(charge_id):
    """Encodes the given base 10 charge_id into a base 31 string.

    Throws ApplicationError if charge_id is less than ChargeId.FLOOR or greater than ChargeId.CEILING.
    """
    if charge_id < ChargeId.FLOOR or charge_id > ChargeId.CEILING:
        raise ApplicationError('The given charge id ({}) is less than the allowed floor ({}), or greater than the '
                               'allowed ceiling ({})'.format(charge_id, ChargeId.FLOOR, ChargeId.CEILING), 500)

    encoded = ''
    while charge_id > 0:
        charge_id, remainder = divmod(charge_id, 31)
        encoded = ChargeId.CHARACTERS[remainder] + encoded

    return encoded


def decode_base_31(encoded_charge_id):
    """Decodes the given a base 31 encoded_charge_id returning it's base 10 equivalent."""
    result = 0

    for index in range(len(encoded_charge_id)):
        place_value = ChargeId.CHARACTERS.index(encoded_charge_id[index])
        result += place_value * (len(ChargeId.CHARACTERS) ** (len(encoded_charge_id) - index - 1))

    return result
