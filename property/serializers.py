from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Property,Image, PropertyType,Room,PropertyImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        

class PropertySerializer(serializers.ModelSerializer):
    #images = ImageSerializer(many=True)
    images = serializers.ListField(
                       child=serializers.ImageField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ),required=False
                                )
    def create(self, validated_data):
        if 'images' in validated_data.keys():
            images=validated_data.pop('images')
            for img in images:
                photo=Image.objects.create(image=img)
            return photo
        return validated_data
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id","owner")

class RoomSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ("id","owner")

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = "__all__"

"""   
from django.core.files import File

f = File(open(os.path.join(IMPORT_DIR, 'fotos', photo), 'rb'))
p = Photo(name=f.name, image=f, parent=supply.supply_ptr)
name = str(uuid1()) + os.path.splitext(f.name)[1]
p.image.save(name, f)
p.save()

"""