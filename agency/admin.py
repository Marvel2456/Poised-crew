from django.contrib import admin
from .models import Service, EventPortfolio, UniformStyle, GalleryItem, Testimonial, QuoteInquiry, CrewApplication


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'badge_text', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'short_description', 'deliverables')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured')


@admin.register(EventPortfolio)
class EventPortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_held', 'location', 'crew_deployed', 'client_name', 'is_featured')
    list_filter = ('category', 'date_held', 'is_featured')
    search_fields = ('title', 'client_name', 'location', 'services_provided')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)


@admin.register(UniformStyle)
class UniformStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'gender', 'color_palette')
    search_fields = ('name', 'tag', 'description')


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'caption')
    list_editable = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role_company', 'event_name', 'rating', 'is_featured')
    list_filter = ('rating', 'is_featured')
    search_fields = ('client_name', 'client_role_company', 'event_name')


@admin.register(QuoteInquiry)
class QuoteInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'full_name', 'organization', 'event_type', 'event_date', 'crew_count', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'event_date', 'created_at')
    search_fields = ('full_name', 'organization', 'email', 'phone_whatsapp', 'event_name', 'venue_name')
    list_editable = ('status',)
    readonly_fields = ('created_at',)


@admin.register(CrewApplication)
class CrewApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'age', 'height_cm', 'city', 'experience_years', 'status', 'created_at')
    list_filter = ('status', 'gender', 'city', 'experience_years')
    search_fields = ('full_name', 'email', 'phone_whatsapp', 'city', 'languages')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
