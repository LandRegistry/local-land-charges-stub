class ChargeId(object):

    # The lowest valid charge id.
    FLOOR = 1

    # The highest valid charge id.
    CEILING = 887503680

    # The separator used between the prefix and the charge id.
    SEPARATOR = '-'

    # Value prefixed to each encoded charge id.
    PREFIX_NO_SEPARATOR = 'LLC'
    PREFIX = '{}{}'.format(PREFIX_NO_SEPARATOR, SEPARATOR)

    # Characters allowed for encoding.
    CHARACTERS = '0123456789BCDFGHJKLMNPQRSTVWXYZ'

    # The minimum length of an encoded charge id (excluding the prefix).
    LENGTH_FLOOR = 1

    # The maximum length of an encoded charge id (excluding the prefix).
    LENGTH_CEILING = 6

    # Regex to match a charge id's prefix. The prefix is mandatory the separator optional.
    PREFIX_REGEX = '^(' + PREFIX_NO_SEPARATOR + ')' + '(' + SEPARATOR + ')?'

    # Regex to match a valid encoded charge id, with it's prefix.
    IS_VALID_REGEX = PREFIX_REGEX + '([' + CHARACTERS + ']){' + str(LENGTH_FLOOR) + ',' + str(LENGTH_CEILING) + '}$'
