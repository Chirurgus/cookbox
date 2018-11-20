import re

from functools import wraps

from fractions import Fraction


TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?'
)


def get_minutes(element):
    try:
        tstring = element.get_text()
        if '-' in tstring:
            tstring = tstring.split('-')[1]  # sometimes formats are like this: '12-15 minutes'
        matched = TIME_REGEX.search(tstring)

        minutes = int(matched.groupdict().get('minutes') or 0)
        minutes += 60 * int(matched.groupdict().get('hours') or 0)

        return minutes
    except AttributeError:  # if dom_element not found or no matched
        return 0


def normalize_string(string):
    return re.sub(
        r'\s+', ' ',
        string.replace(
            '\xa0', ' ').replace(  # &nbsp;
            '\n', ' ').replace(
            '\t', ' ').strip()
    )

def parse_ingredients(ing_str):
    ''' Returns list of tuples (quntity, description) '''
    quantity_str = [ ing.split(' ',1)[0] for ing in ing_str ]
    descriptions = [ ing.split(' ',1)[1] for ing in ing_str ]

    ingredients = []

    for qty, desc in zip(quantity_str, descriptions):
        try:
            q = float(Fraction(qty))
            ingredients.append((q, desc))
        except ValueError:
            q = float(0)
            ingredients.append( (q, ' '.join([qty, desc])) )
    return ingredients

def normalize_instructions(instructions):
    ret = []

    for string in instructions:
        ret += string.split('.')

    return [instruction for instruction in ret if instruction != '']
    


def on_exception_return(to_return):
    """
    On unpredicted exception return `to_return` provided in the decorator.
    Still raise some specific errors (as NotImplementedError listed here)

    This is needed due to not being able to predict what elements can be missing
    from the DOM and not being able to foresee all the possible erorrs from bs4
    """
    def decorate(decorated_function):
        @wraps(decorated_function)
        def wrap(*args, **kwargs):
            try:
                result = decorated_function(*args, **kwargs)
                return result
            except NotImplementedError as e:
                raise e
            except Exception:
                return to_return
        return wrap
    return decorate
