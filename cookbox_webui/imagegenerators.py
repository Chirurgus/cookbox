from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill

class ThumbnailLarge(ImageSpec):
    processors = [ResizeToFill(900, 600)]
    format = 'JPEG'
    options = {'quality': 85}

class ThumbnailMedium(ImageSpec):
    processors = [ResizeToFill(600, 400)]
    format = 'JPEG'
    options = {'quality': 85}

class ThumbnailSmall(ImageSpec):
    processors = [ResizeToFill(200, 133)]
    format = 'JPEG'
    options = {'quality': 70}

register.generator('cookbox_webui:thumbnail_large', ThumbnailLarge)
register.generator('cookbox_webui:thumbnail_medium', ThumbnailMedium)
register.generator('cookbox_webui:thumbnail_small', ThumbnailSmall)
