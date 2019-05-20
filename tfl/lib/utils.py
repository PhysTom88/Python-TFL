
from tfl.api.exceptions import InvalidInputError
from tfl.lib.validation import validate_input

def stringify_boolean(to_string)
    clean_string = validate_input(to_string, str, "clean_string")
    if clean_string.lower() == "true":
        return "True"
    elif clean_string.lower() == "false":
        return "False"
    else:
        raise InvalidInputError("Unable to booleanise the string: {0}".format(clean_string))
