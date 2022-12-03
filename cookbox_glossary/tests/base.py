# Created by Oleksandr Sorochynskyi
# On 03/12/2019

from cookbox_core.tests import CookboxBaseTest


class GlossaryBaseTest(CookboxBaseTest):
    article_data = {
        "body": "Test lalala",
    }

    entry_data = {
        "term": "cookbox glossary",
        "article": None,
    }
