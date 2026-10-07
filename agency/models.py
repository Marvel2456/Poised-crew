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
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True, help_text="Upload portfolio photo (auto-compressed to WebP)")
    image_url = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_held']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/placeholder.jpg'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class UniformStyle(models.Model):
    name = models.CharField(max_length=150)
    tag = models.CharField(max_length=100, help_text="e.g. VIP Galas & Red Carpets")
    description = models.TextField()
    gender = models.CharField(max_length=50, default="Unisex / Male & Female")
    image = models.ImageField(upload_to='uniforms/', blank=True, null=True, help_text="Upload uniform photo (auto-compressed to WebP)")
    image_url = models.CharField(max_length=500, blank=True)
    color_palette = models.CharField(max_length=150, default="Imperial Gold & Obsidian Black")

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/placeholder.jpg'


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
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, help_text="Upload gallery image (auto-compressed to WebP)")
    image_url = models.CharField(max_length=500, blank=True)
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/placeholder.jpg'


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    client_role_company = models.CharField(max_length=200, help_text="e.g. Lead Planner, Aurora Luxury Weddings")
    event_name = models.CharField(max_length=200)
    quote = models.TextField()
    rating = models.IntegerField(default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Upload client/planner photo (auto-compressed to WebP)")
    avatar_url = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client_name} - {self.event_name}"

    @property
    def display_avatar(self):
        if self.avatar:
            return self.avatar.url
        return self.avatar_url


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


class CoreValue(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default='crown', help_text="Lucide icon name e.g. crown, shield-check, lock, clock, sparkles, languages")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class SiteContent(models.Model):
    # --- ABOUT US & BRAND ETHOS ---
    about_hero_badge = models.CharField(max_length=150, default="Our Story & Ethos")
    about_hero_title = models.CharField(max_length=255, default="Redefining African Event Hospitality With Unmatched Poise.")
    about_hero_subtitle = models.TextField(default="Founded on the conviction that event staffing should be a disciplined craft of diplomatic excellence, executive etiquette, and genuine African warmth.")
    about_story_title = models.CharField(max_length=255, default="The Poised Story: From Event Staffing to Protocol Authority")
    about_story_paragraph_1 = models.TextField(default="The Poised Crew was established to bridge a critical gap in the luxury and corporate event industry: the need for impeccably trained, highly punctual, and intellectually sharp protocol officers who can effortlessly navigate both cultural traditions and strict diplomatic decorum.")
    about_story_paragraph_2 = models.TextField(default="Whether handling the accreditation of 3,000 international delegates at an African energy summit or orchestrating royal family protocol at a multi-day wedding, our crew brings calmness, precision, and commanding elegance to every engagement.")
    
    # Mission & Vision
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_statement = models.TextField(default="To provide flawless hospitality and protocol choreography that protects our clients' prestige and creates an unforgettable guest experience.")
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_statement = models.TextField(default="To be Africa's benchmark institution for diplomatic protocol, luxury event ushering, and executive hospitality leadership.")
    
    # Academy / Showcase Highlight
    academy_title = models.CharField(max_length=150, default="The Poised Academy")
    academy_description = models.TextField(default="Over 400 hours of annual protocol & etiquette drill sessions")
    academy_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Upload academy/showcase photo (auto-compressed to WebP)")
    academy_image_url = models.CharField(max_length=500, default="https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1000&q=80", blank=True)

    @property
    def display_academy_image(self):
        if self.academy_image:
            return self.academy_image.url
        return self.academy_image_url or '/static/images/placeholder.jpg'

    # --- HOMEPAGE HERO ---
    hero_badge = models.CharField(max_length=150, default="Excellence in Event Protocol & Luxury Hospitality")
    hero_title = models.CharField(max_length=255, default="Where Regal Poise Meets Diplomatic Precision.")
    hero_subtitle = models.TextField(default="Transforming conferences, high-society weddings, state banquets, and red-carpet galas into seamless, unforgettable experiences across Africa.")
    hero_guarantee_1 = models.CharField(max_length=100, default="100% Punctuality Guarantee")
    hero_guarantee_2 = models.CharField(max_length=100, default="Certified Etiquette & Protocol")
    hero_guarantee_3 = models.CharField(max_length=100, default="Bespoke Attire Customization")

    # --- LIVE MILESTONE STATS ---
    stat_events_count = models.CharField(max_length=50, default="500+")
    stat_events_label = models.CharField(max_length=100, default="Events Executed")
    stat_officers_count = models.CharField(max_length=50, default="120+")
    stat_officers_label = models.CharField(max_length=100, default="Vetted Protocol Officers")
    stat_punctuality_rate = models.CharField(max_length=50, default="99.9%")
    stat_punctuality_label = models.CharField(max_length=100, default="On-Time Deployment")
    stat_summits_count = models.CharField(max_length=50, default="15+")
    stat_summits_label = models.CharField(max_length=100, default="Diplomatic Summits")

    # --- COMPANY & CONTACT INFO ---
    company_name = models.CharField(max_length=150, default="The Poised Crew")
    tagline = models.CharField(max_length=255, default="Luxury Event Ushering & VIP Protocol Agency")
    phone_display = models.CharField(max_length=50, default="0705 185 1600")
    whatsapp_number = models.CharField(max_length=50, default="2347051851600")
    email_address = models.EmailField(default="thepoisedcrew@gmail.com")
    office_address = models.CharField(max_length=255, default="Benin City, Edo State")
    instagram_handle = models.CharField(max_length=100, default="@thepoisedcrew", blank=True)

    # --- CALL TO ACTION (CTA) BANNER ---
    cta_banner_title = models.CharField(max_length=255, default="Elevate Your Next High-Profile Event With The Poised Crew")
    cta_banner_subtitle = models.TextField(default="From royal ceremonies and political summits to luxury society weddings, reserve Africa's most distinguished protocol and ushering professionals.")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Website Content & Settings"
        verbose_name_plural = "Website Content & Settings"

    def __str__(self):
        return "Website Content & Settings"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

