from rest_framework import serializers
from .models import *
import logging


logger = logging.getLogger(__name__)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    agreement_contract_file = serializers.FileField(
        required=False, allow_null=True)
    agreement_vendor_signing_copy = serializers.FileField(
        required=False, allow_null=True)

    class Meta:
        model = Supplier
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"


class SizeQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeQuantity
        fields = "__all__"


class ColorSizeGroupSerializer(serializers.ModelSerializer):
    color = serializers.CharField()  # Accept color name as string
    size_quantities = SizeQuantitySerializer(many=True)

    class Meta:
        model = ColorSizeGroup
        fields = "__all__"

    def create(self, validated_data):
        color_name = validated_data.pop('color')
        size_quantities_data = validated_data.pop('size_quantities')

        color = None
        if color_name:
            color, _ = Color.objects.get_or_create(color=color_name)

        group = ColorSizeGroup.objects.create(color=color)

        for sq_data in size_quantities_data:
            sq = SizeQuantity.objects.create(**sq_data)
            group.size_quantities.add(sq)

        group.total = sum(sq.quantity for sq in group.size_quantities.all())
        group.save()

        return group


# serializers.py

class RepeatOfSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatOf
        fields = ['id', 'repeat_of']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['id', 'styles']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item']


class FabricationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabrication
        fields = ['id', 'fabrication']


class InquirySerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    buyer = serializers.PrimaryKeyRelatedField(
        queryset=Buyer.objects.all(), required=False, allow_null=True
    )
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=False, allow_null=True
    )

    # 🔁 Read-only nested serializers
    repeat_of = RepeatOfSerializer(read_only=True)
    same_style = StyleSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    fabrication = FabricationSerializer(read_only=True)

    # 🔁 Write-only IDs
    repeat_of_id = serializers.PrimaryKeyRelatedField(
        source='repeat_of', queryset=RepeatOf.objects.all(), write_only=True
    )
    same_style_id = serializers.PrimaryKeyRelatedField(
        source='same_style', queryset=Style.objects.all(), write_only=True, required=False, allow_null=True
    )
    item_id = serializers.PrimaryKeyRelatedField(
        source='item', queryset=Item.objects.all(), write_only=True, required=False, allow_null=True
    )
    fabrication_id = serializers.PrimaryKeyRelatedField(
        source='fabrication', queryset=Fabrication.objects.all(), write_only=True, required=False, allow_null=True
    )

    color_size_groups = ColorSizeGroupSerializer(many=True, required=False)

    class Meta:
        model = Inquiry
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'image1': {'required': False, 'allow_null': True},
            'attachment': {'required': False, 'allow_null': True},
            'inquiry_no': {'required': False, 'allow_null': True},
            'order_date': {'required': False, 'allow_null': True},
            'shipment_date': {'required': False, 'allow_null': True},
            'proposed_shipment_date': {'required': False, 'allow_null': True},
            'received_date': {'required': False, 'allow_null': True},
            'techrefdate': {'required': False, 'allow_null': True},
            'confirmed_price_date': {'required': False, 'allow_null': True},
            'remarks': {'required': False, 'allow_null': True},
            'local_remarks': {'required': False, 'allow_null': True},
            'buyer_remarks': {'required': False, 'allow_null': True},
            'wash_description': {'required': False, 'allow_null': True},
            'order_remarks': {'required': False, 'allow_null': True},
            'grand_total': {'required': False, 'allow_null': True},
            'color_size_groups': {'required': False, 'allow_null': True},
            'year': {'required': False, 'allow_null': True},
            'repeat_of': {'required': False, 'allow_null': True},
            'same_style': {'required': False, 'allow_null': True},
            'item': {'required': False, 'allow_null': True},
            'fabrication': {'required': False, 'allow_null': True},
            # REMOVE 'buyer' and 'customer' from extra_kwargs here as they are defined above
            # 'buyer': {'required': False, 'allow_null': True},
            # 'customer': {'required': False, 'allow_null': True},
            'fabric1': {'required': False, 'allow_null': True},
            'fabric2': {'required': False, 'allow_null': True},
            'fabric3': {'required': False, 'allow_null': True},
            'fabric4': {'required': False, 'allow_null': True},
        }

    def _handle_foreign_key_fields(self, validated_data):
        """
        Handle foreign key fields that accept string names for creation/getting.
        Buyer and Customer are now PrimaryKeyRelatedField, so they handle IDs directly
        and are removed from this method's scope.
        """
        fk_fields = {

            'repeat_of': (RepeatOf, 'repeat_of'),
            'same_style': (Style, 'styles'),
            'item': (Item, 'item'),
            'fabrication': (Fabrication, 'fabrication'),
            # Removed 'buyer' and 'customer' from here.
        }
        for field_name, (model_class, field_attr) in fk_fields.items():
            if field_name in validated_data:
                value = validated_data[field_name]
                if value:
                    if isinstance(value, str):
                        obj, _ = model_class.objects.get_or_create(
                            **{field_attr: value})
                        validated_data[field_name] = obj
                    elif isinstance(value, dict) and 'id' in value:
                        try:
                            validated_data[field_name] = model_class.objects.get(
                                id=value['id'])
                        except model_class.DoesNotExist:
                            raise serializers.ValidationError(
                                f"{field_name} with ID {value['id']} does not exist.")
                else:
                    # Set to None if value is falsy
                    validated_data[field_name] = None
        return validated_data

    def create(self, validated_data):
        color_size_groups_data = validated_data.pop('color_size_groups', [])
        # Call _handle_foreign_key_fields only for the fields it manages
        validated_data = self._handle_foreign_key_fields(validated_data)

        image_file = validated_data.pop('image', None)
        image1_file = validated_data.pop('image1', None)
        attachment_file = validated_data.pop('attachment', None)

        inquiry = Inquiry.objects.create(**validated_data)

        if image_file:
            inquiry.image = image_file
        if image1_file:
            inquiry.image1 = image1_file
        if attachment_file:
            inquiry.attachment = attachment_file
        inquiry.save()

        for group_data in color_size_groups_data:
            color_serializer = ColorSizeGroupSerializer(data=group_data)
            color_serializer.is_valid(raise_exception=True)
            color_size_group_instance = color_serializer.save()
            inquiry.color_size_groups.add(color_size_group_instance)

        inquiry.grand_total = sum(
            group.total for group in inquiry.color_size_groups.all())
        inquiry.save()

        return inquiry

    def update(self, instance, validated_data):
        logger.debug(f"Inquiry update - validated_data: {validated_data}")

        color_size_groups_data = validated_data.pop('color_size_groups', None)

        # Call _handle_foreign_key_fields only for the fields it manages
        validated_data = self._handle_foreign_key_fields(validated_data)

        image_file = validated_data.pop('image', None)
        image1_file = validated_data.pop('image1', None)
        attachment_file = validated_data.pop('attachment', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image_file is not None:
            instance.image = image_file
        if image1_file is not None:
            instance.image1 = image1_file
        if attachment_file is not None:
            instance.attachment = attachment_file

        if color_size_groups_data is not None:
            instance.color_size_groups.all().delete()
            for group_data in color_size_groups_data:
                group_id = group_data.get('id')
                if group_id:
                    try:
                        color_group_instance = ColorSizeGroup.objects.get(
                            id=group_id)
                        color_serializer = ColorSizeGroupSerializer(
                            color_group_instance, data=group_data, partial=True)
                    except ColorSizeGroup.DoesNotExist:
                        color_serializer = ColorSizeGroupSerializer(
                            data=group_data)
                else:
                    color_serializer = ColorSizeGroupSerializer(
                        data=group_data)

                color_serializer.is_valid(raise_exception=True)
                created_or_updated_group = color_serializer.save()
                instance.color_size_groups.add(created_or_updated_group)

        if color_size_groups_data is not None:
            instance.grand_total = sum(
                group.total for group in instance.color_size_groups.all())

        instance.save()
        return instance


class InquiryAttachmentSerializer(serializers.ModelSerializer):
    inquiry_no = serializers.IntegerField(source='inquiry.inquiry_no', read_only=True)
    class Meta:
        model = InquiryAttachment
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ColorTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorTotal
        fields = "__all__"



