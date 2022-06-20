from django.contrib import admin

from .models import Project, MaterialPrefix, ModelConfiguration, ModelFile, Material, SwappableGroup, ModelSubConfiguration

admin.site.register(Project)
admin.site.register(ModelFile)
admin.site.register(ModelConfiguration)
admin.site.register(ModelSubConfiguration)
admin.site.register(MaterialPrefix)
admin.site.register(Material)
admin.site.register(SwappableGroup)
