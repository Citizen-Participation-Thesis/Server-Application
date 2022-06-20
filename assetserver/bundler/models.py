from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File
from colorfield.fields import ColorField

import qrcode
from PIL import Image, ImageDraw
from io import BytesIO


class SwappableGroup(models.Model):
    name = models.CharField(max_length=20)
    connected = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Swappable Groups"

    def __str__(self):
        return self.name


class Material(models.Model):
    hex_color = ColorField(default='#FFFFFF')
    connected = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Colors"

    def __str__(self):
        return str(self.hex_color)


class MaterialPrefix(models.Model):
    prefix = models.CharField(max_length=40)
    materials = models.ManyToManyField(Material, max_length=1)
    connected = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Material Prefixes"

    def __str__(self):
        return self.prefix


class ModelFile(models.Model):
    hidden_name = models.CharField(max_length=40, unique=True)
    presentable_name = models.CharField(max_length=40, unique=True)
    model_base = models.TextField(default="empty")
    placeable = models.BooleanField(default=False)

    prefixes = models.ManyToManyField(MaterialPrefix)
    group = models.ManyToManyField(SwappableGroup, max_length=1)

    class Meta:
        verbose_name_plural = "Raw Model Files"

    def __str__(self):
        return self.presentable_name


class ModelSubConfiguration(models.Model):
    subPosX = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    subPosY = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    subPosZ = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    subRotX = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])
    subRotY = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])
    subRotZ = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])

    class Meta:
        verbose_name_plural = "Model SubConfigurations"

    def __str__(self):
        return "SubConf-" + str(self.subPosX) + "-" + str(self.subPosY) + "-" + str(self.subPosZ)


class ModelConfiguration(models.Model):
    model_file_ref = models.ManyToManyField(ModelFile, max_length=1)
    posX = models.DecimalField('posX', decimal_places=2, max_digits=5, default=0)
    posY = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    posZ = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    rotX = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])
    rotY = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])
    rotZ = models.DecimalField(decimal_places=2, max_digits=5, default=0,
                               validators=[MinValueValidator(-360), MaxValueValidator(360)])
    scaleX = models.DecimalField(decimal_places=2, max_digits=5, default=1)
    scaleY = models.DecimalField(decimal_places=2, max_digits=5, default=1)
    scaleZ = models.DecimalField(decimal_places=2, max_digits=5, default=1)

    sub_configurations = models.ManyToManyField(ModelSubConfiguration, max_length=6, blank=True)

    class Meta:
        verbose_name_plural = "Model Configurations"

    def __str__(self):
        return "Config-" + str(self.posX.__int__()) + "-" + str(self.posY.__int__()) + "-" + str(self.posZ.__int__())


class Project(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=400)

    bundle = models.FileField(upload_to="bundles")
    status = models.CharField(max_length=20, default="Not deployed")
    qr = models.ImageField(upload_to='qrcode', blank=True)

    model_files = models.ManyToManyField(ModelFile)

    model_configurations = models.ManyToManyField(ModelConfiguration)

    class Meta:
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.title)
        canvas = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr.save(f'{self.title}-code.png', File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)



