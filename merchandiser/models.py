from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class Buyer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    wgr = models.IntegerField(verbose_name="W.G.R", blank=True, null=True)
    product_categories = models.CharField(
        max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    buyer = models.ManyToManyField(Buyer, related_name="customers", blank=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Supplier(models.Model):

    AGREEMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    DOC_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Vendor Information
    vendor_id = models.CharField(max_length=100, blank=True, null=True)
    reference_no = models.CharField(max_length=100, blank=True, null=True)

    # Company Names
    name = models.CharField(max_length=100, blank=True, null=True)
    name_1 = models.CharField(max_length=100, blank=True, null=True)
    name_2 = models.CharField(max_length=100, blank=True, null=True)
    name_3 = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    local_name = models.CharField(max_length=100, blank=True, null=True)

    # Vendor Status
    vendor_type = models.CharField(max_length=100, blank=True, null=True)
    holding_group = models.CharField(max_length=100, blank=True, null=True)
    vendor_access_creation = models.BooleanField(
        default=False, blank=True, null=True)
    vendor_rating = models.CharField(max_length=50, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    place_of_incorporation = models.CharField(
        max_length=100, blank=True, null=True)

    # Address
    address = models.TextField(blank=True, null=True)
    additional_address = models.TextField(blank=True, null=True)
    town_city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country_region = models.CharField(max_length=100, blank=True, null=True)
    gps_lng = models.CharField(max_length=50, blank=True, null=True)
    gps_lat = models.CharField(max_length=50, blank=True, null=True)
    eu_country = models.BooleanField(default=False, blank=True, null=True)

    # General Contact
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)

    # general
    preferred_language = models.CharField(
        max_length=50, default="English", blank=True, null=True)
    deactivation_date = models.DateField(blank=True, null=True)
    planned_inactivation_date = models.DateField(blank=True, null=True)
    vendor_rating = models.CharField(max_length=50, blank=True, null=True)

    # group
    purchasing_group = models.CharField(max_length=255, blank=True, null=True)
    contract_sign_date = models.DateField(blank=True, null=True)
    deactivation_reason = models.TextField(blank=True, null=True)
    capability = models.CharField(max_length=255, blank=True, null=True)

    # Default Contact Person
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_mobile = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    # Bank Info
    bank_details = models.TextField(blank=True, null=True)
    swift_code = models.CharField(max_length=20, blank=True, null=True)

    # Company Background
    place_of_incorporation = models.CharField(
        max_length=100, blank=True, null=True)
    year_established = models.CharField(max_length=4, blank=True, null=True)
    number_of_running_factories = models.CharField(
        max_length=10, blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(
        max_length=50, default="English", blank=True, null=True)
    capability = models.CharField(max_length=255, blank=True, null=True)
    reason_for_enlistment = models.TextField(blank=True, null=True)

    # Dates & Status
    contract_sign_date = models.DateField(blank=True, null=True)
    deactivation_date = models.DateField(blank=True, null=True)
    planned_inactivation_date = models.DateField(blank=True, null=True)
    deactivation_reason = models.TextField(blank=True, null=True)

    # Misc
    purchasing_group = models.CharField(max_length=255, blank=True, null=True)
    migrated = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)

    # Shipment Terms
    incoterm = models.CharField(max_length=100, blank=True, null=True)
    avg_lead_time_days = models.IntegerField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    payment_term = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    cash_discount = models.CharField(max_length=50, blank=True, null=True)
    liability_insurance = models.CharField(
        max_length=100, blank=True, null=True)
    export_license_no = models.CharField(max_length=100, blank=True, null=True)

    # classification
    classification_code = models.CharField(
        max_length=100, blank=True, null=True)
    classification_name = models.TextField(blank=True, null=True)

    # financial_details
    account_name = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    account_no_2 = models.CharField(max_length=100, blank=True, null=True)
    bank_key = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    country_of_bank = models.CharField(max_length=100, blank=True, null=True)
    bank_code_swift_code = models.CharField(
        max_length=100, blank=True, null=True)
    discount_rate = models.CharField(max_length=100, blank=True, null=True)
    total_annual_turnover = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    export_annual_turnover = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    credit_limit = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    credit_report = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    agent_payment = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    super_bonus = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)

    # Certification
    certification_type = models.CharField(
        max_length=100, blank=True, null=True)
    certification_name = models.CharField(
        max_length=100, blank=True, null=True)
    certification_number = models.CharField(
        max_length=100, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    institute_country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    attachment = models.FileField(
        upload_to='certifications/', blank=True, null=True)

    # Agreements
    agreement_code = models.CharField(max_length=100, blank=True, null=True)
    agreement_name = models.CharField(max_length=255, blank=True, null=True)
    agreement_description = models.TextField(blank=True, null=True)
    agreement_type = models.CharField(max_length=100, blank=True, null=True)
    agreement_contract_file = models.FileField(
        upload_to='agreements/', blank=True, null=True)
    agreement_status = models.CharField(
        max_length=20, choices=AGREEMENT_STATUS_CHOICES, default='pending', blank=True, null=True
    )
    agreement_vendor_signing_copy = models.FileField(
        upload_to='agreements/vendor_copies/', blank=True, null=True)
    agreement_doc_status = models.CharField(
        max_length=20, choices=DOC_STATUS_CHOICES, default='draft', blank=True, null=True
    )
    agreement_vendor_action_required = models.BooleanField(
        default=False, blank=True, null=True)
    agreement_signature_due_date = models.DateField(blank=True, null=True)
    agreement_expiry_date = models.DateField(blank=True, null=True)
    agreement_accepted_on = models.DateField(blank=True, null=True)
    agreement_instruction_to_vendor = models.TextField(blank=True, null=True)

    # Address (Default)
    address_type = models.CharField(max_length=100, blank=True, null=True)
    address_country_region = models.CharField(
        max_length=100, blank=True, null=True)
    address_street = models.TextField(blank=True, null=True)
    address_town_city = models.CharField(max_length=100, blank=True, null=True)
    address_gps_lng = models.CharField(max_length=50, blank=True, null=True)
    address_gps_lat = models.CharField(max_length=50, blank=True, null=True)
    address_postal_code = models.CharField(
        max_length=20, blank=True, null=True)
    address_port_of_loading_discharge = models.CharField(
        max_length=100, blank=True, null=True)
    address_language = models.CharField(max_length=50, blank=True, null=True)
    address_inactive = models.BooleanField(default=False)
    address_gps_text = models.TextField(blank=True, null=True)
    address_eu_country = models.BooleanField(default=False)

    # Contact 1 (Default)
    contact1_type = models.CharField(max_length=100, blank=True, null=True)
    contact1_texweave_access = models.BooleanField(default=False)
    contact1_title = models.CharField(max_length=50, blank=True, null=True)
    contact1_first_name = models.CharField(
        max_length=100, blank=True, null=True)
    contact1_last_name = models.CharField(
        max_length=100, blank=True, null=True)
    contact1_position = models.CharField(max_length=100, blank=True, null=True)
    contact1_tel = models.CharField(max_length=20, blank=True, null=True)
    contact1_mobile = models.CharField(max_length=20, blank=True, null=True)
    contact1_email = models.EmailField(blank=True, null=True)
    contact1_department = models.CharField(
        max_length=100, blank=True, null=True)

    # Related Vendor (1 record)
    related_vendor_name = models.CharField(
        max_length=255, blank=True, null=True)
    related_vendor_id = models.CharField(max_length=100, blank=True, null=True)
    related_vendor_type = models.CharField(
        max_length=100, blank=True, null=True)
    related_vendor_status = models.CharField(
        max_length=100, blank=True, null=True)
    related_vendor_doc_status = models.CharField(
        max_length=100, blank=True, null=True)
    related_vendor_relationship = models.TextField(blank=True, null=True)

    # Related Factory (0 or 1 record)
    factory_default = models.BooleanField(default=False)
    factory_name = models.CharField(max_length=255, blank=True, null=True)
    factory_id = models.CharField(max_length=100, blank=True, null=True)
    factory_type = models.CharField(max_length=100, blank=True, null=True)
    factory_sync = models.BooleanField(default=False)
    factory_status = models.CharField(max_length=100, blank=True, null=True)
    factory_doc_status = models.CharField(
        max_length=100, blank=True, null=True)
    factory_vendor_ref = models.CharField(
        max_length=100, blank=True, null=True)
    factory_vendor_reverse_ref = models.CharField(
        max_length=100, blank=True, null=True)
    factory_capacity = models.CharField(max_length=100, blank=True, null=True)
    factory_related = models.CharField(max_length=100, blank=True, null=True)
    factory_related_since = models.DateField(blank=True, null=True)
    factory_note = models.TextField(blank=True, null=True)
    audit_social = models.BooleanField(default=False)
    audit_1st_enlistment = models.BooleanField(default=False)
    audit_2nd_enlistment = models.BooleanField(default=False)
    audit_qualification_visit = models.BooleanField(default=False)
    audit_kik_csr = models.BooleanField(default=False)
    audit_environmental = models.BooleanField(default=False)
    audit_qc_visit = models.BooleanField(default=False)

    # QA Assessment
    qa_rank = models.CharField(max_length=100, blank=True, null=True)
    qa_assessment_level = models.CharField(
        max_length=100, blank=True, null=True)
    qa_risk_level = models.CharField(max_length=100, blank=True, null=True)
    qa_performance_level = models.CharField(
        max_length=100, blank=True, null=True)
    qa_score = models.CharField(max_length=50, blank=True, null=True)
    qa_accredited = models.BooleanField(default=False)
    qa_summary = models.TextField(blank=True, null=True)
    qa_disposal_licensing = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="E.g., 'not by EU supplier'"
    )

    # Latest Audit Report (1 record)
    latest_audit_report_no = models.CharField(
        max_length=100, blank=True, null=True)
    latest_audit_version = models.CharField(
        max_length=50, blank=True, null=True)
    latest_audit_report_type = models.CharField(
        max_length=100, blank=True, null=True)
    latest_audit_customer = models.CharField(
        max_length=255, blank=True, null=True)
    latest_audit_date = models.DateField(blank=True, null=True)
    latest_auditor = models.CharField(max_length=100, blank=True, null=True)
    latest_audit_party = models.CharField(
        max_length=100, blank=True, null=True)
    latest_audit_result = models.CharField(
        max_length=100, blank=True, null=True)
    latest_audit_expiry_date = models.DateField(blank=True, null=True)
    latest_audit_report_date = models.DateField(blank=True, null=True)
    latest_audit_status = models.CharField(
        max_length=100, blank=True, null=True)
    latest_audit_editing_status = models.CharField(
        max_length=100, blank=True, null=True)

    # Images (0 or 1 record)
    image_type = models.CharField(max_length=100, blank=True, null=True)
    image_description = models.TextField(blank=True, null=True)
    image_file = models.ImageField(
        upload_to='supplier_images/', blank=True, null=True)
    image_last_modified_by = models.CharField(
        max_length=100, blank=True, null=True)
    image_last_modified_on = models.DateTimeField(blank=True, null=True)

    # Attachments (0 or 1 record)
    attachment_type = models.CharField(max_length=100, blank=True, null=True)
    attachment_description = models.TextField(blank=True, null=True)
    attachment_file = models.FileField(
        upload_to='supplier_attachments/', blank=True, null=True)
    attachment_last_modified_by = models.CharField(
        max_length=100, blank=True, null=True)
    attachment_last_modified_on = models.DateTimeField(blank=True, null=True)

    # Shared Files (0 or 1 record)
    shared_file_name = models.CharField(max_length=255, blank=True, null=True)
    shared_file_type = models.CharField(max_length=100, blank=True, null=True)
    shared_file_description = models.TextField(blank=True, null=True)
    shared_file = models.FileField(
        upload_to='supplier_shared_files/', blank=True, null=True)
    shared_file_details = models.TextField(blank=True, null=True)
    shared_file_status = models.CharField(
        max_length=100, blank=True, null=True)
    shared_file_effective_from = models.DateField(blank=True, null=True)
    shared_file_effective_to = models.DateField(blank=True, null=True)
    shared_file_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Style(models.Model):
    styles = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.styles


class RepeatOf(models.Model):
    repeat_of = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.repeat_of


class Item(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.item


class Fabrication(models.Model):
    fabrication = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.fabrication


class ColorTotal(models.Model):
    total_color = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.total_color


class Color(models.Model):
    color = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.color


class SizeQuantity(models.Model):
    size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f"{self.size}: {self.quantity}"


class ColorSizeGroup(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size_quantities = models.ManyToManyField(SizeQuantity, blank=True)
    total = models.PositiveIntegerField(default=0, blank=True, null=True)
        
    def __str__(self):
        return f"{self.color} - Total: {self.total}"

@receiver(m2m_changed, sender=ColorSizeGroup.size_quantities.through)
def update_color_size_group_total(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.total = sum(sq.quantity for sq in instance.size_quantities.all()) if instance.size_quantities.exists() else 0
        instance.save(update_fields=['total'])
    

class Inquiry(models.Model):
    ORDER_TYPE_CHOICES = [
        ('advertisement', 'Advertisement'),
        ('programmer', 'Programmer'),
    ]

    WITH_HANGER = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    GENDER_CHOICES = [
        ('all', 'All'),
        ('blanks', 'Blanks'),
        ('ladies', 'Ladies'),
        ('bag', 'Bag'),
        ('boy', 'Boy'),
        ('girls', 'Girls'),
        ('mama', 'Mama'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('quoted', 'Quoted'),
        ('running', 'Running'),
        ('Suppliersinformed', 'Suppliers Informed'),
        ('all', 'All'),
    ]

    GARMENT_CHOICES = [
        ('all', 'All'),
        ('knit', 'Knit'),
        ('woven', 'Woven'),
        ('sweater', 'Sweater'),

    ]
    
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]
    # Inquiry Information

    inquiry_no = models.IntegerField(blank=True, null=True)
    season = models.CharField(
        max_length=20, choices=SEASON_CHOICES, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    repeat_of = models.ForeignKey(
        RepeatOf, on_delete=models.SET_NULL, null=True, blank=True)
    same_style = models.ForeignKey(
        Style, on_delete=models.SET_NULL, null=True, blank=True)
    buyer = models.ForeignKey(
        Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    shipment_date = models.DateField(blank=True,null=True)
    wgr = models.IntegerField(verbose_name="W.G.R", blank=True, null=True)
    with_hanger = models.CharField(max_length=3, choices=WITH_HANGER, blank=True, null=True)
    program = models.CharField(max_length=100,blank=True,null=True)
    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE_CHOICES, blank=True, null=True)
    garment = models.CharField(
        max_length=100, choices=GARMENT_CHOICES, blank=True, null=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True, blank=True)
    fabric1 = models.TextField(blank=True, null=True)
    fabric2 = models.TextField(blank=True, null=True)
    fabric3 = models.TextField(blank=True, null=True)
    fabric4 = models.TextField(blank=True, null=True)
    fabrication = models.ForeignKey(
        Fabrication, on_delete=models.SET_NULL, null=True, blank=True)
    received_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='inquiries/', blank=True, null=True)
    image1 = models.ImageField(upload_to='inquiries/', blank=True, null=True)
    proposed_shipment_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer,  on_delete=models.SET_NULL, null=True, blank=True)
    local_remarks = models.TextField(blank=True, null=True)
    buyer_remarks = models.TextField(blank=True, null=True)
    wash_description = models.TextField(blank=True, null=True)
    techrefdate = models.DateField(blank=True, null=True)
    target_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    confirmed_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    confirmed_price_date = models.DateField(blank=True, null=True)
    attachment = models.FileField(
        upload_to='inquiries/attachments/', blank=True, null=True)
    current_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', blank=True, null=True)
    order_remarks = models.TextField(blank=True, null=True)
    color_size_groups = models.ManyToManyField(ColorSizeGroup, blank=True)
    grand_total = models.PositiveIntegerField(default=0,blank=True, null=True)
    order_no = models.CharField(max_length=100, blank=True, null=True)
    order_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.item} - {self.order_type}"
    
    def save(self, *args, **kwargs):
        # First save the Inquiry instance to get an ID
        super().save(*args, **kwargs)
        
        # Now we can safely work with the many-to-many relationships
        # Calculate grand_total only if color_size_groups exists
        if hasattr(self, 'color_size_groups'):
            self.grand_total = sum(group.total for group in self.color_size_groups.all()) if self.color_size_groups.exists() else 0
            # Save again to update the grand_total, but avoid infinite recursion
            super().save(update_fields=['grand_total'])

    def save(self, *args, **kwargs):
        # First save the Inquiry instance to get an ID
        super().save(*args, **kwargs)
        
        # Handle color_size_groups grand total calculation
        if hasattr(self, 'color_size_groups'):
            self.grand_total = sum(group.total for group in self.color_size_groups.all()) if self.color_size_groups.exists() else 0
        
        # Handle attachment creation
        if self.attachment and not InquiryAttachment.objects.filter(file=self.attachment.name).exists():
            InquiryAttachment.objects.create(
                inquiry=self,
                file=self.attachment,
                description=f"Auto-created attachment for inquiry {self.inquiry_no}"
            )
        
        # Save again to update fields, but avoid infinite recursion
        super().save(update_fields=['grand_total'])
          


class InquiryAttachment(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='attachments', blank=True, null=True)
    file = models.FileField(upload_to='inquiries/attachments/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.inquiry.inquiry_no} - {self.file.name}"

