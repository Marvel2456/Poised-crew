from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('protocol', 'VIP & Diplomatic Protocol'),
        ('ushering', 'Event Ushering & Guest Experience'),
        ('corporate', 'Corporate & Conference Management'),
        ('specialist', 'Specialist & Logistics Coordination'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ushering')
    short_description = models.TextField(help_text="Short teaser for cards and hero previews")
    full_description = models.TextField(help_text="In-depth breakdown of the service")
    icon_name = models.CharField(max_length=50, default='crown', help_text="Lucide icon name e.g. crown, shield-check, users, award, mic")
    deliverables = models.TextField(help_text="Newline-separated list of what is included")
    suitable_events = models.TextField(help_text="Newline-separated list of suitable event types")
    uniform_recommendations = models.CharField(max_length=255, default="Corporate Black-Tie or Luxury Velvet")
    badge_text = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 'Most Requested' or 'VIP Exclusive'")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def deliverables_list(self):
        return [item.strip() for item in self.deliverables.split('\n') if item.strip()]

    @property
    def suitable_events_list(self):
        return [item.strip() for item in self.suitable_events.split('\n') if item.strip()]


class EventPortfolio(models.Model):
    CATEGORY_CHOICES = [
        ('corporate', 'Corporate'),
        ('wedding', 'Wedding'),
        ('conference', 'Conference'),
        ('government', 'Government & Diplomatic'),
        ('entertainment', 'Entertainment & Gala'),
        ('exhibition', 'Exhibition & Expo'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_held = models.DateField()
    location = models.CharField(max_length=255, help_text="e.g. Eko Convention Centre, Victoria Island")
    city = models.CharField(max_length=100, default="Lagos, Nigeria")
    client_name = models.CharField(max_length=200)
    planner_name = models.CharField(max_length=200, blank=True, null=True)
    crew_deployed = models.IntegerField(default=20, help_text="Number of ushers / protocol officers")
    services_provided = models.CharField(max_length=300, help_text="e.g. VIP Protocol • Digital Registration • Red Carpet • Hall Ushering")
    summary = models.TextField()
    highlight_result = models.CharField(max_length=255, help_text="Key accomplishment or metric")
    image_url = models.CharField(max_length=500)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_held']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class UniformStyle(models.Model):
    name = models.CharField(max_length=150)
    tag = models.CharField(max_length=100, help_text="e.g. VIP Galas & Red Carpets")
    description = models.TextField()
    gender = models.CharField(max_length=50, default="Unisex / Male & Female")
    image_url = models.CharField(max_length=500)
    color_palette = models.CharField(max_length=150, default="Imperial Gold & Obsidian Black")

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('events', 'Event Highlights'),
        ('team', 'Our Team & Officers'),
        ('uniforms', 'Uniform Lookbook'),
        ('protocol', 'VIP Protocol'),
        ('conferences', 'Conferences & Summits'),
        ('weddings', 'Luxury Weddings'),
        ('bts', 'Behind The Scenes'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='events')
    image_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    client_role_company = models.CharField(max_length=200, help_text="e.g. Lead Planner, Aurora Luxury Weddings")
    event_name = models.CharField(max_length=200)
    quote = models.TextField()
    rating = models.IntegerField(default=5)
    avatar_url = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client_name} - {self.event_name}"


class QuoteInquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New Inquiry'),
        ('contacted', 'Contacted / Proposal Sent'),
        ('confirmed', 'Confirmed & Booked'),
        ('completed', 'Event Completed'),
        ('archived', 'Archived'),
    ]

    # Contact Info
    full_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone_whatsapp = models.CharField(max_length=50)

    # Event Details
    event_name = models.CharField(max_length=250)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    event_duration_hours = models.IntegerField(default=8)
    event_location = models.CharField(max_length=150, default="Lagos, Nigeria")
    venue_name = models.CharField(max_length=250)
    expected_guests = models.CharField(max_length=100)

    # Staffing Details
    services_required = models.TextField(help_text="Comma-separated selected services")
    crew_count = models.IntegerField(default=10)
    gender_preference = models.CharField(max_length=100, default="Balanced Mix")
    uniform_preference = models.CharField(max_length=150, default="Classic Black-Tie Tuxedo & Gown")
    special_requirements = models.TextField(blank=True)

    # Financial Estimator
    estimated_cost_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estimated_cost_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Quote #{self.id} - {self.event_name} ({self.full_name})"


class CrewApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('shortlisted', 'Shortlisted for Audition'),
        ('accepted', 'Accepted into Academy'),
        ('active', 'Active Protocol Officer'),
        ('rejected', 'Not Selected'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_whatsapp = models.CharField(max_length=50)
    gender = models.CharField(max_length=30)
    age = models.IntegerField()
    height_cm = models.IntegerField(help_text="Height in cm")
    city = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    languages = models.CharField(max_length=200, help_text="e.g. English, French, Yoruba")
    experience_years = models.CharField(max_length=50)
    experience_summary = models.TextField()
    instagram_handle = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Audition: {self.full_name} ({self.city})"
