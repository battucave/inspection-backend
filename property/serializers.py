from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from authapp.serializers import UserCreateSerializer

from PIL import Image as PILImage
from pixelmatch.contrib.PIL import pixelmatch
from io import BytesIO,StringIO
from django.core.files import File
from django.core.files.base import ContentFile

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

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = "__all__"

class CompareSectionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'expected_image' in validated_data.keys():
            expected_image_pk = validated_data.pop('expected_image')
        else:
            expected_image_pk = None

        if 'room_occupancy' in validated_data.keys():
            room_occupancy = validated_data.pop('room_occupancy')
        else:
            room_occupancy = None

        if 'property' in validated_data.keys():
            property = validated_data.pop('property')
        else:
            property = None

        if 'room' in validated_data.keys():
            room = validated_data.pop('room')
        else:
            room = None

        if 'event' in validated_data.keys():
            event = validated_data.pop('event')
        else:
            event = None

        obj = Section.objects.create(**validated_data)
        obj.save()

        try:
            expected_image = Image.objects.get(pk=expected_image_pk)
            img1 = PILImage.open(expected_image.image)
            img2 = PILImage.open(validated_data.get('image'))
            img1.thumbnail((1000, 1000))
            img2.thumbnail((1000, 1000))
            img_diff = PILImage.new("RGB", img1.size)
            mismatch = pixelmatch(img1, img2, img_diff, threshold=0.5, fail_fast=True,includeAA=True)

            img_io = BytesIO()
            img_diff.save(img_io, format='png', quality=100)
            img_content = ContentFile(img_io.getvalue(), 'img5.png')
            
            img_diff_obj = Image.objects.create(image=img_content)
            img_diff_obj.save()

            if mismatch > 0:
                discrepancy = Discrepancy.objects.create(
                    property = property,
                    room_occupancy = room_occupancy,
                    expected_image = expected_image,
                    uploaded_image = obj,
                    discrepancy_at = event,
                    diff = mismatch,
                    diff_image = img_diff_obj
                )
                discrepancy.save()
        except:
            print("ERROR cannot calculate")

        return obj


    class Meta:
        model = Section
        fields = "__all__"

class RoomOccupancySerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False)
    room = RoomSerializer(required=False)
    check_in_images = SectionSerializer(many=True, required=False)
    check_out_images = SectionSerializer(many=True, required=False)

    class Meta:
        model = RoomOccupancy
        fields = "__all__"

class ListRoomOccupancySerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False)
    room = RoomSerializer(required=False)
    check_in_images = SectionSerializer(many=True, required=False)
    check_out_images = SectionSerializer(many=True, required=False)

    class Meta:
        model = RoomOccupancy
        fields = "__all__"


class DiscrepencySerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False)
    room_occupancy = RoomOccupancySerializer(required=False)
    expected_image = ImageSerializer(required=False)
    uploaded_image = SectionSerializer(required=False)
    diff_image = ImageSerializer(required=False)
    
    class Meta:
        model = Discrepancy
        fields = "__all__"


class TenantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tenant
        fields = ("id", "email", "property","user")
        extra_kwargs = {
            "property": {"read_only": True},
            "user": {"read_only": True},
        }

    def validate(self, data):
        if Tenant.objects.filter(
            email=data['email'],
            property = self.context["property"]         
            ).exists():

            raise serializers.ValidationError(
                "This user (email) already in your tenant added list"
            )
        return data
        

    