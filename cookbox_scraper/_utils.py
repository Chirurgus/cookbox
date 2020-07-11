import re
import textwrap
import unicodedata

from html import unescape
from functools import wraps
from fractions import Fraction

from cookbox_core.models import Recipe, Instruction

VULGAR_FRACTIONS = "¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞"
MESUREMENT_UNITS = {
    r"tbsp?\.?"       : ("ml", 15),
    r"tsp\.?"         : ("ml", 5),
    r"table ?spoons?" : ("ml", 15),
    r"tea ?spoons?"   : ("ml", 5),
    r"grams?"         : ("g", 1),
    r"g\.?"           : ("g", 1),
    r"kilo\.?"        : ("kg", 1),
    r"kilograms?"     : ("kg", 1),
    r"kg\.?"          : ("kg", 1),
    r"liters?"        : ("l", 1),
    r"litres?"        : ("l", 1),
    r"l\.?"           : ("l", 1),
    r"ml\.?"          : ("ml", 1),
    r"milliliter\.?"  : ("ml", 1),
    r"cups?"          : ("ml", 236.588),
    r"pounds?"        : ("g", 453.6),
    r"ounces?"        : ("g", 28.36),
    r"oz\.?"          : ("g", 28.36),
    r"lb\.?"          : ("g", 453.6),
    r"кг\.?"          : ("kg", 1),
    r"г\.?"           : ("g", 1),
    r"мг\.?"          : ("mg", 1),
    r"л\.?"           : ("l", 1),
    r"мл\.?"          : ("ml", 1),
    r"ст\.?л\.?"      : ("ml", 15),
    r"ч\.?л\.?"       : ("g", 5),
}

def normalize_string(string):
    return unescape(
        re.sub(
        r'\s+', ' ',
        string.replace(
            '\xa0', ' ').replace(  # &nbsp;
            '\n', ' ').replace(
            '\t', ' ').strip()
        )
    )

def parse_quantity(quantity, default=None):
    '''
    Parse a quantity string to a float

    Always returns a valid float. If the parsing fails returns None.
    This function also handles Vulgar fractions (e.g. ¼),
    and composite fractions, i.e., '1 1/2'.
    '''
   # Handle the common case like "123" or "123.2", or "123,2"
    try:
        return float(quantity.replace(",", "."))
    except ValueError:
        pass  

    # In case of Unicode fractions
    try:
        return unicodedata.numeric(quantity)
    except (TypeError, ValueError):
        pass

    # In case of fractions like "1/2"
    try:
        return float(Fraction(quantity))
    except ValueError:
        pass

    # Handle cases like "1 1/2", assumes additivity, i.e., that "2 1/2" is 2.5
    if ' ' in quantity:
        return sum([
            parse_quantity(qty, 0)
            for qty in quantity.strip().split(' ')
        ])

    # Handle cases like "1¼", case assumes additivity
    vfrac_rexp = "[" + VULGAR_FRACTIONS + "]"
    vfracs = re.findall(vfrac_rexp, quantity)
    if vfracs:
        quantity = quantity.replace(vfrac_rexp , ' ').strip()
        ret = sum([ parse_quantity(f, 0) for f in vfracs ])
        ret += parse_quantity(quantity, 0)
        return ret
    
    # If all else fails
    return default

def parse_ingredients(ing_list):
    '''
    Returns a list of tuples (quantity, unit, description)
    '''
    mesurements_re = MESUREMENT_UNITS.keys()
    qty_re = r"(?:\d+[,./]?\d*)|(?:[" + VULGAR_FRACTIONS + "]+)"

    # Only match if the regexp in list is after a space, a numeric,
    # or new line (ie. "g" does not match "egg", but does "250g")
    combined = r"(?:(?P<qty>" + qty_re + r")\s?|^|\s)(?P<unit>(?:" + r")|(?:".join(mesurements_re) + r"))(?:$|\s)"
    pat = re.compile(combined, re.IGNORECASE)

    ret = []
    for ing in ing_list:
        # Try to extract unit form ingredients
        m = re.search(pat, ing)
        if m:
            qty = m.group("qty") if m.group("qty") else ""
            unit = m.group("unit") if m.group("unit") else ""
            # Remove the qty/unit form the description
            repl = m.group()
            for f in [ "qty", "unit" ]:
                if m.group(f):
                    repl = repl.replace(m.group(f), "")
            desc = ing.replace(m.group(), repl.strip())
        else:
            qty = ""
            unit = ""
            desc = ing
        
        # Extract qty
        if qty == "":
            m = re.search("(" + qty_re + ")", desc)
            if m:
                qty = m.group()
                desc = desc.replace(m.group(), "")
        ret.append( (parse_quantity(qty, 1), unit, desc) )

    return ret

def normalize_instructions(instructions):
    '''
    Returns list of strings.
    '''
    MAX_LEN = Instruction._meta.get_field("instruction").max_length

    if isinstance(instructions, str):
        instructions = [ instructions ]

    ret = []

    for string in instructions:
        ins_list = string.split('.')
        for ins in ins_list:
            ret += textwrap.wrap(ins, MAX_LEN, break_long_words=False)

    return [
        normalize_string(instruction)
        for instruction in ret if instruction != ''
    ]

def parse_iso8601(string):
    '''
    Parse duration in ISO 8601 format

    Returns (unit, numeric) tuple. Unit is one of Recipe
    duration units.
    '''
    iso8601re = r"(P(?:(?P<years>\d*)Y)?(?:(?P<month>\d*)M)?(?:(?P<week>\d*)W)?(?:(?P<day>\d*)D)?)?(T(?:(?P<hour>\d*)H)?(?:(?P<minute>\d*)M)?(?:(?P<second>\d*)S)?)?"
    m = re.search(iso8601re, string)
    weeks = 0.0
    if m.group("years"):
        weeks = weeks + float(m.group("years")) * 52.18
    if m.group("month"):
        weeks = weeks + float(m.group("month")) * 4.39
    if m.group("week"):
        weeks = weeks + float(m.group("week"))
    if m.group("day"):
        weeks = weeks + float(m.group("day")) / 7

    hours = weeks * 24 * 7
    if m.group("hour"):
        hours = hours + float(m.group("hour"))
    if m.group("minute"):
        hours = hours + float(m.group("minute")) / 60
    if m.group("second"):
        hours = hours + float(m.group("second")) / 365

    return (Recipe.HRS, round(hours, 2))
