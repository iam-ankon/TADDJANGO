from rest_framework import viewsets
from .models import * 
from .serializers import * 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from PyPDF2 import PdfReader, PdfWriter
from django.http import JsonResponse
from PIL import Image, ImageDraw
from django.http import HttpResponse
import base64
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO


from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image




# Modify EmployeeDetailsViewSet in views.py
class EmployeeDetailsViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDetails.objects.all()
    serializer_class = EmployeeDetailsSerializer

    @action(detail=True, methods=['patch'])
    def update_customers(self, request, pk=None):
        employee = self.get_object()
        customer_ids = request.data.get('customers', [])
        employee.customer.set(customer_ids)
        return Response({'status': 'customers updated'})

class EmployeeTerminationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTermination.objects.all()
    serializer_class = EmployeeTerminationSerializer
    
    def update(self, request, *args, **kwargs):
        # Handle the update logic here if necessary
        return super().update(request, *args, **kwargs)

class PerformanseAppraisalViewSet(viewsets.ModelViewSet):
    queryset = PerformanseAppraisal.objects.all()
    serializer_class = PerformanseAppraisalSerializer

class TADGroupsViewSet(viewsets.ModelViewSet):
    queryset = TADGroups.objects.all()
    serializer_class = TADGroupsSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer    

# Notifications ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class EmailLogViewSet(viewsets.ModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer

    # Custom action for deleting all email logs
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        try:
            # Delete all email logs
            EmailLog.objects.all().delete()
            return Response({'message': 'All email logs have been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeeLeaveViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLeave.objects.all()
    serializer_class = EmployeeLeaveSerializer

class EmployeeLeaveBalanceViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLeaveBalance.objects.all()
    serializer_class = EmployeeLeaveBalanceSerializer

class EmployeeLeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLeaveType.objects.all()
    serializer_class = EmployeeLeaveTypeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer


class LetterSendViewSet(viewsets.ModelViewSet):
    queryset = LetterSend.objects.all()
    serializer_class = LetterSendSerializer
    parser_classes = (MultiPartParser, FormParser)


class ITProvisionViewSet(viewsets.ModelViewSet):
    queryset = ITProvision.objects.all()
    serializer_class = ITProvisionSerializer

class AdminProvisionViewSet(viewsets.ModelViewSet):
    queryset = AdminProvision.objects.all()
    serializer_class = AdminProvisionSerializer

class FinanceProvisionViewSet(viewsets.ModelViewSet):
    queryset = FinanceProvision.objects.all()
    serializer_class = FinanceProvisionSerializer

class EmployeeAttachmentListCreateView(viewsets.ModelViewSet):
    queryset = EmployeeAttachment.objects.all()
    serializer_class = EmployeeAttachmentSerializer

    def get_queryset(self):
        employee_id = self.request.query_params.get("employee_id")
        if employee_id:
            return self.queryset.filter(employee__id=employee_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')  # Get multiple files
        employee_id = request.data.get('employee')  # Get employee ID
        descriptions = request.data.getlist('description')  # Get descriptions for each file

        if not employee_id:
            return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if len(descriptions) != len(files):
            return Response({"error": "Number of descriptions must match number of files"}, status=status.HTTP_400_BAD_REQUEST)

        employee = EmployeeDetails.objects.get(id=employee_id)

        attachments = []
        for i, file in enumerate(files):
            attachment = EmployeeAttachment(employee=employee, file=file, description=descriptions[i])
            attachments.append(attachment)

        EmployeeAttachment.objects.bulk_create(attachments)  # Bulk insert

        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)


class EmployeeAttachmentDeleteView(generics.DestroyAPIView):
    queryset = EmployeeAttachment.objects.all()
    serializer_class = EmployeeAttachmentSerializer


class TerminationAttachmentListCreateView(viewsets.ModelViewSet):
    queryset = TerminationAttachment.objects.all()
    serializer_class = TerminationAttachmentSerializer

    def get_queryset(self):
        employee_id = self.request.query_params.get("employee_id")
        if employee_id:
            return self.queryset.filter(employee__id=employee_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')  # Get multiple files
        employee_id = request.data.get('employee')  # Get employee ID
        descriptions = request.data.getlist('description')  # Get descriptions for each file

        if not employee_id:
            return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if len(descriptions) != len(files):
            return Response({"error": "Number of descriptions must match number of files"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = EmployeeDetails.objects.get(id=employee_id)  # ✅ Use EmployeeTermination
        except EmployeeDetails.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        attachments = [
            TerminationAttachment(employee=employee, file=file, description=descriptions[i])
            for i, file in enumerate(files)
        ]

        TerminationAttachment.objects.bulk_create(attachments)  # Bulk insert

        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)



class TerminationAttachmentDeleteView(generics.DestroyAPIView):
    queryset = TerminationAttachment.objects.all()
    serializer_class = TerminationAttachmentSerializer



class CVAddViewSet(viewsets.ModelViewSet):
    queryset = CVAdd.objects.all()
    serializer_class = CVAddSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if not request.FILES.get("cv_file"):
            request.data._mutable = True
            request.data["cv_file"] = instance.cv_file
            request.data._mutable = False

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="update-cv-with-qr")
    def update_cv_with_qr(self, request, pk=None):
        try:
            cv = get_object_or_404(CVAdd, id=pk)
            if not cv.cv_file:
                return JsonResponse({"error": "No CV file uploaded"}, status=400)

            qr_code_data = request.data.get("qr_code")
            if not qr_code_data:
                return JsonResponse({"error": "No QR code data provided"}, status=400)

            # Decode base64 QR code image
            qr_img_data = base64.b64decode(qr_code_data.split(",")[1])
            qr_img = Image.open(BytesIO(qr_img_data))

            # Save QR to BytesIO as PNG
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format="PNG")
            qr_buffer.seek(0)

            # Load existing PDF
            pdf_path = cv.cv_file.path
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Create overlay PDF with QR code
            overlay = BytesIO()
            c = canvas.Canvas(overlay, pagesize=letter)
            c.drawImage(ImageReader(qr_buffer), 450, 650, width=100, height=100)  # Adjust position
            c.save()
            overlay.seek(0)

            overlay_pdf = PdfReader(overlay)

            # Merge overlay with first page
            first_page = reader.pages[0]
            first_page.merge_page(overlay_pdf.pages[0])
            writer.add_page(first_page)

            for i in range(1, len(reader.pages)):
                writer.add_page(reader.pages[i])

            # Return updated PDF
            output_pdf = BytesIO()
            writer.write(output_pdf)
            output_pdf.seek(0)

            return HttpResponse(
                output_pdf,
                content_type="application/pdf",
                headers={'Content-Disposition': 'inline; filename="cv_with_qr.pdf"'}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class MdsirViewSet(viewsets.ModelViewSet):
    queryset = Mdsir.objects.all()
    serializer_class = MdsirSerializer

class InviteMailViewSet(viewsets.ModelViewSet):
    queryset = InviteMail.objects.all()
    serializer_class = InviteMailSerializer    