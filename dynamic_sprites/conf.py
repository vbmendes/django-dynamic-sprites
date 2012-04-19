from django.conf import settings

USE_PNGQUANT = getattr(settings, 'DYNAMIC_SPRITES_USE_PNGQUANT', False)
