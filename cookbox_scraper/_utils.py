import re
import textwrap

from html import unescape
from functools import wraps
from fractions import Fraction

from cookbox_core.models import Recipe, Instruction

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

def parse_quantity(quantity):
    try:
        return float(quantity)
    except ValueError:
        quantity_list = quantity.split(' ')
        quantity_float = []
        for qty in quantity_list:
            quantity_float.append(float(Fraction(qty)))
        return sum(quantity_float)

def parse_ingredients(ing_list):
    '''
    Returns a list of tuples (quantity, unit, description)
    '''
    mesurements_re = [r"tbsp\.?", r"tsp\.?", r"table ?spoons?", r"tea ?spoons?",
        r"grams?", r"g\.?", r"kilo\.?", r"kilograms?", r"kg\.?", r"liters?",
        r"litres?" r"l\.?", r"ml\.?", r"milliliter\.?", r"cups?", r"pounds?",
        r"ounces?", r"oz\.?", r"lb\.?", r"кг\.?", r"г\.?", r"мг\.?",
        r"л\.?", r"мл\.?", r"ст\.?л\.?", r"ч\.?л\.?",
    ]

    # Only match if the regesp in list is after a space, a numeric,
    # or new line (ie. "g" does not match "egg", but does "250g")
    combined = r"(?:\d|^|\s)(?:(" + ")|(".join(mesurements_re) + r"))(?:$|\s)"
    pat = re.compile(combined, re.IGNORECASE)

    new_ing_list = []
    mesurements = []
    for ing in ing_list:
        m = re.search(pat, ing)
        if m:
            mesurements.append(m.group(m.lastindex))
            new_ing_list.append(re.sub(pat, ' ', ing))
        else:
            mesurements.append("")
            new_ing_list.append(ing)
    ing_list = new_ing_list
    
    quantity_str = [
        ing.split(' ',1)[0] if ' ' in ing else '1'
        for ing in ing_list
    ]
    descriptions = [
        ing.split(' ',1)[1] if ' ' in ing else ing
        for ing in ing_list
    ]

    ingredients = []

    for qty, mes, desc in zip(quantity_str, mesurements, descriptions):
        try:
            q = parse_quantity(qty)
            ingredients.append((q, mes, desc))
        except ValueError:
            ingredients.append((1, mes, ' '.join([qty, desc])))
    return ingredients

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
