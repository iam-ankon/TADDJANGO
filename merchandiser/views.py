from requests import Response
from rest_framework import viewsets, status
from .models import *
from .serializers import *
import json
import logging
from rest_framework.response import Response
from rest_framework import status

# Initialize logger
logger = logging.getLogger(__name__)

# Customer Views


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Agent Views


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

# Supplier Views


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# Buyer Views


class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

# Color Size Group Views


class ColorSizeGroupViewSet(viewsets.ModelViewSet):
    queryset = ColorSizeGroup.objects.all()
    serializer_class = ColorSizeGroupSerializer

# Size Quantity Views


class SizeQuantityViewSet(viewsets.ModelViewSet):
    queryset = SizeQuantity.objects.all()
    serializer_class = SizeQuantitySerializer

# Inquiry Views


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        try:
            if 'data' in request.data:
                json_data = json.loads(request.data['data'])

                # Handle file fields
                files_mapping = {
                    'image': request.FILES.get('image'),
                    'image1': request.FILES.get('image1'),
                    'attachment': request.FILES.get('attachment')
                }
                json_data.update({k: v for k, v in files_mapping.items() if v})

                serializer = self.get_serializer(data=json_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )

            return super().create(request, *args, **kwargs)

        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return Response(
                {'error': 'Invalid JSON data format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error processing inquiry: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            if 'data' in request.data:
                json_data = json.loads(request.data['data'])

                # ✅ Handle deleted color size groups
                deleted_ids = json_data.get('deleted_color_size_group_ids', [])
                if deleted_ids:
                    from .models import ColorSizeGroup  # adjust this if needed
                    ColorSizeGroup.objects.filter(id__in=deleted_ids).delete()

                # Handle file fields - only update if new files are provided
                files_mapping = {
                    'image': request.FILES.get('image'),
                    'image1': request.FILES.get('image1'),
                    'attachment': request.FILES.get('attachment')
                }

                for key, file in files_mapping.items():
                    if file:
                        json_data[key] = file

                serializer = self.get_serializer(
                    instance, data=json_data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)

            return super().update(request, *args, **kwargs)

        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return Response(
                {'error': 'Invalid JSON data format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating inquiry: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class StyleViewSet(viewsets.ModelViewSet):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer


class RepeatOfViewSet(viewsets.ModelViewSet):
    queryset = RepeatOf.objects.all()
    serializer_class = RepeatOfSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FabricationViewSet(viewsets.ModelViewSet):
    queryset = Fabrication.objects.all()
    serializer_class = FabricationSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorTotalViewSet(viewsets.ModelViewSet):
    queryset = ColorTotal.objects.all()
    serializer_class = ColorTotalSerializer

class InquiryAttachmentViewSet(viewsets.ModelViewSet):
    queryset = InquiryAttachment.objects.all()
    serializer_class = InquiryAttachmentSerializer