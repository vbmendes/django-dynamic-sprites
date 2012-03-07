# coding: utf8

import os

from django.conf import settings

from dynamic_sprites.sprite import Sprite


class ModelSprite(Sprite):

    def __init__(self, name, queryset, image_field, slug_field, **kwargs):
        images = self._get_images_from_queryset(queryset, image_field, slug_field)
        super(ModelSprite, self).__init__(name, images, **kwargs)

    @staticmethod
    def _get_images_from_queryset(queryset, image_field, slug_field):
        images = []
        for obj in queryset.values(image_field, slug_field):
            image = (obj[slug_field], os.path.join(settings.MEDIA_ROOT, obj[image_field]))
            images.append(image)
        return images
