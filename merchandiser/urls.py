from django.urls import path, include
from .views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('buyer', BuyerViewSet)
router.register('agent', AgentViewSet)
router.register('supplier', SupplierViewSet)
router.register('customer', CustomerViewSet)
router.register('style', StyleViewSet)
router.register('repeat_of', RepeatOfViewSet)
router.register('item', ItemViewSet)
router.register('fabrication', FabricationViewSet)
router.register('inquiry', InquiryViewSet)
router.register('color', ColorViewSet)
router.register('color_total', ColorTotalViewSet)
router.register('color_size_group', ColorSizeGroupViewSet)
router.register('size_quantity', SizeQuantityViewSet)
router.register('inquiry_attachment', InquiryAttachmentViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

]



