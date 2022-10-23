from django.db import models

from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.
# class Upload(models.Model):
#     class FilterChoices(models.TextChoices):
#         NO_FILTER = 'no_filter'
#         COLORIZED = 'colorized'
#         GRAYSCALE = 'grayscale'
#         BLURRED = 'blurred'
#         BINARY = 'binary'
#         INVERT = 'invert'
#
#     image = models.ImageField(upload_to='images')
#     action = models.CharField(max_length=20, choices=FilterChoices.choices, default=FilterChoices.NO_FILTER)
#
#     def __str__(self):
#         return str(self.id)
#
#     def save(self, *args, **kwargs):
#         # open image
#         pil_img = Image.open(self.image)
#
#         # convert the image to array and do some processing
#         cv_img = np.array(pil_img)
#         img = get_filtered_image(cv_img, self.action)
#
#         # convert back to pil image
#         im_pil = Image.fromarray(img)
#
#         # save
#         buffer = BytesIO()
#         im_pil.save(buffer, format='png')
#         image_png = buffer.getvalue()
#         self.image.save(str(self.image), ContentFile(image_png), save=False)
#
#         super().save(*args, **kwargs)


class FilterChoices(models.TextChoices):
    NO_FILTER = 'no filter'
    COLORIZED = 'colorized'
    GRAYSCALE = 'grayscale'
    BLURRED = 'blurred'
    BINARY = 'binary'
    INVERT = 'invert'
    LESS_BRIGHT = "less bright"

    MORE_BRIGHT = "more bright"
    SHARPEN_EFFECT = "sharpen"

    SEPIA_EFFECT = "sepia"
    PENCIL_SKETCH_GRAY = "grey pencil sketch"
    PENCIL_SKETCH_COLOR = "color pencil sketch"
    HDR_EFFECT = "hdr"
    SUMMER_EFFECT = "summer"
    WINTER_EFFECT = "winter"


class Upload(models.Model):
    image = models.ImageField(upload_to='images')
    action = models.CharField(max_length=50, choices=FilterChoices.choices, default=FilterChoices.NO_FILTER)
    filtered_image = models.ImageField(upload_to='filtered', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # open image
        pil_img = Image.open(self.image)

        # convert the image to array and do some processing
        cv_img = np.array(pil_img)
        img = get_filtered_image(cv_img, self.action)

        # convert back to pil image
        im_pil = Image.fromarray(img)

        # save
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), self.image, save=False)
        self.filtered_image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)
