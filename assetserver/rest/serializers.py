from rest_framework import serializers
from bundler.models import Project, Material, SwappableGroup, \
    ModelFile, MaterialPrefix, ModelConfiguration, ModelSubConfiguration


class ColorSerializer(serializers.ModelSerializer): # noqa
    class Meta:
        model = Material
        fields = ['hex_color']


class GroupSerializer(serializers.ModelSerializer): # noqa
    class Meta:
        model = SwappableGroup
        fields = ('name', )


class PrefixSerializer(serializers.ModelSerializer): # noqa
    materials = ColorSerializer(many=True)

    class Meta:
        model = MaterialPrefix
        fields = ['prefix', 'materials']


class SimpleModSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelFile
        fields = ('hidden_name',)


class SubConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSubConfiguration
        fields = ['subPosX', 'subPosY', 'subPosZ', 'subRotX', 'subRotY', 'subRotZ']


class ConfigSerializer(serializers.ModelSerializer):
    model_file_ref = SimpleModSerializer(many=True, required=True)
    sub_configurations = SubConfigSerializer(many=True, required=False)

    class Meta:
        model = ModelConfiguration
        fields = ['posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ',
                  'scaleX', 'scaleY', 'scaleZ', 'model_file_ref', 'sub_configurations']

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        # Validate project and model existence

    def save(self):
        super().save()
        # Save to project's model_configurations field




class RawModelSerializer(serializers.ModelSerializer): # noqa
    prefixes = PrefixSerializer(many=True)
    group = GroupSerializer()

    class Meta:
        model = ModelFile
        fields = ['hidden_name', 'presentable_name', 'placeable', 'prefixes', 'group']


class ProjectSerializer(serializers.ModelSerializer): # noqa
    model_files = RawModelSerializer(many=True, required=True)
    model_configurations = ConfigSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('title', 'description', 'bundle', 'status', 'qr', 'model_files', 'model_configurations')


