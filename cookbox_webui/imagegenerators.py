from imagekit import ImageSpec, register
from imagekit.processors import SmartResize


class ThumbnailLarge(ImageSpec):
    processors = [SmartResize(900, 600)]
    format = "JPEG"
    options = {"quality": 85}


class ThumbnailMedium(ImageSpec):
    processors = [SmartResize(600, 400)]
    format = "JPEG"
    options = {"quality": 85}


class ThumbnailSmall(ImageSpec):
    processors = [SmartResize(200, 133)]
    format = "JPEG"
    options = {"quality": 70}


class ThumbnailNoPre(ImageSpec):
    format = "JPEG"
    options = {"quality": 85}


register.generator("cookbox_webui:thumbnail_large", ThumbnailLarge)
register.generator("cookbox_webui:thumbnail_medium", ThumbnailMedium)
register.generator("cookbox_webui:thumbnail_small", ThumbnailSmall)
register.generator("cookbox_webui:thumbnail_no_pre", ThumbnailNoPre)
