# Created by Oleksandr Sorochynskyi
# On 06/12/2019

import re

from django.urls import reverse,reverse_lazy

from .models import ( GlossaryArticle, GlossaryEntry, )

def _multireplace(string, replacements, ignore_case=False):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str
    """
    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
    # "HEY", "hEy", etc.
    if ignore_case:
        def normalize_old(s):
            return s.lower()
        re_mode = re.IGNORECASE
    else:
        def normalize_old(s):
            return s
        re_mode = 0
    replacements = {normalize_old(key): val for key, val in replacements.items()}
    
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    
    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join(rep_escaped), re_mode)
    
    # For each match, look up the new string in the replacements, being the key the normalized old string
    return pattern.sub(lambda match: replacements[normalize_old(match.group(0))], string)

def insert_links(html, ignore=set()):
    '''
    Replace all occurrences of words found in the Cookbox Glossary
    by a link to the page of that term Wikipedia style.

    :param str html: String in which to find and replace the glossary terms.
    :param set of str: set of terms not to replace
    :return: String with all glossary terms replaced.
    '''
    ancor_link = '<a href="{link}">{term}</a>'
    # Populate the dictionary for replacement
    rep = {}
    for article in GlossaryArticle.objects.all():
        for entry in article.entries.all():
            term = entry.term
            if term in ignore:
                continue
            if entry.article is None:
                continue
            link = reverse('glossary-entry-detail', kwargs={ 'pk': entry.id })
            rep[term] = ancor_link.format(link=link, term=term)
    return _multireplace(html, rep, ignore_case=True)

