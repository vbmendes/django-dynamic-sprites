Django Dynamic Sprites
======================

Create sprites dynamicaly for Python and Django.

Version 0.1.3

Instalation
-----------

Install the package via ``pip``::

    pip install django-dynamic-sprites

Generating sprite for images in a folder
----------------------------------------

One way to generate sprites is from all pictures within a folder. To do so, type this command::

    generate_sprites.py path/to/folder path/to/output

One thing to notice is that you don't pass the output extension. The script already generates the image with ``.png`` and the CSS with ``.css``.

Generating sprite from Python code
----------------------------------

Within your python code you can generate sprites for a given set of images. All you have to do is provide the images paths, a nome to each image, generate the sprite and save it::

    from dynamic_sprites.sprite import Sprite

    images = (
        ('brazil', '/path/to/brazil/image.png'),
        ('usa', '/path/to/usa/image.png'),
    )

    sprite = Sprite('sprite_name', images)

    output_image = sprite.generate()
    output_image.save('/path/to/output/image.png')

    output_css = sprite.generate_css('http://images.com/output/image.png')
    output_css.save('/path/to/output/style.css')

That's the basics for generating a sprite from Python code. But there is some abstractions integrating it with Django. Even the name of the project having Django on it, the sprites can be generated without using Django.

Generating sprites for Django queryset objects
----------------------------------------------

Let's pretend you have a Django model like this::

    from django.db import models

    class Country(models.Model):
        name = models.CharField(max_length=255)
        slug = models.SlugField()
        flag = models.ImageField(upload_to='countries')

And you want to have a sprite with all the country flags. You can generate it using a ``Sprite`` specialization::

    from dynamic_sprites.model_sprite import ModelSprite

    sprite = ModelSprite('country-flags', queryset=Country.objects.all(), image_field='flag', slug_field='slug')

    output_image = sprite.generate()
    output_image.save('/path/to/output/image.png')

    output_css = sprite.generate_css('http://images.com/output/image.png')
    output_css.save('/path/to/output/style.css')

You can also connect the sprite generation to the post_save listener and have your sprite generated again each time an object in your queryset is saved::

    from django.db.models.signals import post_save
    from dynamic_sprites.listeners import ModelSpriteListener

    listener = ModelSpriteListener('country-flags', image_field='flag', slug_field='slug', queryset=Country.objects.all())

    post_save.connect(listener, sender=Country)

Contributing to the project
---------------------------

This project is open source, contributions are welcome.
