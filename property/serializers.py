from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Property,Image, PropertyType,Room,PropertyImage
from authapp.serializers import UserCreateSerializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        

class PropertySerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    images = ImageSerializer(many=True,required=False)
    imag = serializers.ListField(
                       child=serializers.ImageField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ),required=False
                               )

 

    def create(self, validated_data):
        print(validated_data.keys())
        if 'imag' in validated_data.keys():
            images=validated_data.pop('imag')
        
        obj = Property.objects.create(**validated_data)
        if images:
            for i,img in enumerate(images):
                    temp=Image.objects.create(image=img)
                    obj.images.add(temp)
                    #PropertyImage.objects.create(order=i,img=temp,property=obj)
                    obj.save()
        
        
        
        return obj
        
    
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id","user")

class RoomSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    images = ImageSerializer(many=True,required=False)
    imag = serializers.ListField(
                       child=serializers.ImageField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ),required=False
                               )
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ("id","user")
    
    def create(self, validated_data):
        print(validated_data.keys())
        if 'imag' in validated_data.keys():
            images=validated_data.pop('imag')
        
        obj = Room.objects.create(**validated_data)
        if images:
            for i,img in enumerate(images):
                    temp=Image.objects.create(image=img)
                    obj.images.add(temp)
                    #PropertyImage.objects.create(order=i,img=temp,property=obj)
                    obj.save()
        
        
        
        return obj

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