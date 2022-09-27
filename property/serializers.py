from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Property,Image, PropertyType,Room,PropertyImage,PropertyApplication,Documents
from authapp.serializers import UserCreateSerializer

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        
class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = "__all__"
        
class PropertySerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    images = ImageSerializer(many=True,required=False)
    imag = serializers.ListField(
                       child=serializers.ImageField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ),required=False
                               )
    property_type_name = serializers.ReadOnlyField(source='property_type.name')

 

    def create(self, validated_data):
        if 'imag' in validated_data.keys():
            images=validated_data.pop('imag')
        else:
            images =None
        
        obj = Property.objects.create(**validated_data)
        if images:
            for i,img in enumerate(images):
                    temp=Image.objects.create(image=img)
                    obj.images.add(temp)
                    obj.save()
        
        
        
        return obj
        
    
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id","user")
    
    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

class RoomSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True,required=False)
    property = PropertySerializer(required = False)
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
        if 'imag' in validated_data.keys():
            images=validated_data.pop('imag')
        else:
            images=None
        
        obj = Room.objects.create(**validated_data)
        if images:
            for i,img in enumerate(images):
                    temp=Image.objects.create(image=img)
                    obj.images.add(temp)
                    obj.save()
        
        
        
        return obj

class PropertyApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True,required=False)
    docs = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False ),required=False
                               )
    class Meta:
        model = PropertyApplication
        fields = "__all__"
    
    def create(self, validated_data):
        if 'docs' in validated_data.keys():
            docs=validated_data.pop('docs')
        else:
            docs =None
        
        
        obj = PropertyApplication.objects.create(**validated_data)
        if docs and obj:
            for i,doc in enumerate(docs):
                    temp=Documents.objects.create(document=doc)
                    obj.documents.add(temp)
                    obj.save()
        
        
        
        return obj

class ListPropertyApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True,required=False)
    property = PropertySerializer(required=False)

    class Meta:
        model = PropertyApplication
        fields = "__all__"

"""   
from django.core.files import File

f = File(open(os.path.join(IMPORT_DIR, 'fotos', photo), 'rb'))
p = Photo(name=f.name, image=f, parent=supply.supply_ptr)
name = str(uuid1()) + os.path.splitext(f.name)[1]
p.image.save(name, f)
p.save()

"""