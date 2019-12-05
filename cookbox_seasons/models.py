# Created by Oleksandr Sorochynskyi
# On 04/12/2019

from django.db import models

from cookbox_core.models import (
    CHAR_FIELD_MAX_LEN_SHORT,
    CHAR_FIELD_MAX_LEN_MEDIUM,
    CHAR_FIELD_MAX_LEN_LONG,
)

class CookboxSeasonEntry(models.Model):
    PEAK_SEASON = 'peak'
    IN_SEASON = 'ok'
    OUT_OF_SEASON = 'ko'

    SEASON_STATE = (
        (PEAK_SEASON, 'Peak season'),
        (IN_SEASON, 'In season'),
        (OUT_OF_SEASON, 'Out of season'),
    )

    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "")
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN_LONG, default= "")
    jan = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    feb = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    mar = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    apr = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    may = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    jun = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    jul = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    aug = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    sep = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    oct = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    nov = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    dec = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, choices=SEASON_STATE, default=OUT_OF_SEASON)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name