# Created by Oleksandr Sorochynskyi
# On 06/12/2019

from cookbox_core.tests import CookboxBaseTest

from cookbox_seasons.models import SeasonsItem

class SeasonsBaseTest(CookboxBaseTest):
    seasons_item_data = {
        'name'  : 'apples',
        'note' : 'Produced all year long, but naturally grows during following seasons',
        'jan'   : SeasonsItem.OUT_OF_SEASON,
        'feb'   : SeasonsItem.OUT_OF_SEASON,
        'mar'   : SeasonsItem.IN_SEASON,
        'apr'   : SeasonsItem.IN_SEASON,
        'may'   : SeasonsItem.IN_SEASON,
        'jun'   : SeasonsItem.IN_SEASON,
        'jul'   : SeasonsItem.PEAK_SEASON,
        'aug'   : SeasonsItem.PEAK_SEASON,
        'sep'   : SeasonsItem.PEAK_SEASON,
        'oct'   : SeasonsItem.IN_SEASON,
        'nov'   : SeasonsItem.IN_SEASON,
        'dec'   : SeasonsItem.OUT_OF_SEASON,
    }
