import json
import urllib.parse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import (
    Service, EventPortfolio, UniformStyle, GalleryItem, Testimonial, 
    QuoteInquiry, CrewApplication, SiteContent, CoreValue
)


def home_view(request):
    featured_services = Service.objects.filter(is_featured=True)[:6]
    all_services = Service.objects.all()[:9]
    featured_portfolio = EventPortfolio.objects.filter(is_featured=True)[:4]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    uniform_styles = UniformStyle.objects.all()[:4]
    gallery_preview = GalleryItem.objects.all()[:6]
    content = SiteContent.get_solo()

    context = {
        'featured_services': featured_services,
        'all_services': all_services,
        'featured_portfolio': featured_portfolio,
        'testimonials': testimonials,
        'uniform_styles': uniform_styles,
        'gallery_preview': gallery_preview,
        'stats': {
            'events_count': content.stat_events_count,
            'events_label': content.stat_events_label,
            'officers_count': content.stat_officers_count,
            'officers_label': content.stat_officers_label,
            'punctuality_rate': content.stat_punctuality_rate,
            'punctuality_label': content.stat_punctuality_label,
            'diplomatic_summits': content.stat_summits_count,
            'diplomatic_label': content.stat_summits_label,
        }
    }
    return render(request, 'agency/home.html', context)


def about_view(request):
    testimonials = Testimonial.objects.all()[:3]
    core_values = CoreValue.objects.all()
    if not core_values.exists():
        values = [
            {'title': 'Uncompromising Poise', 'desc': 'Elegance, impeccable posture, and serene command of every room, regardless of event scale.', 'icon': 'crown'},
            {'title': 'Diplomatic Precision', 'desc': 'Flawless adherence to state protocol, seating order of precedence, and VIP dignitary etiquette.', 'icon': 'shield-check'},
            {'title': 'Absolute Discretion', 'desc': 'Strict confidentiality agreements for private wealth, royal families, and political assemblies.', 'icon': 'lock'},
            {'title': 'Relentless Punctuality', 'desc': '60-minute mandatory pre-call arrival, briefing, and floor rehearsal for zero deployment delays.', 'icon': 'clock'},
            {'title': 'Immaculate Grooming', 'desc': 'Standardized uniform fitting, hygiene, styling, and presence that enhances your event prestige.', 'icon': 'sparkles'},
            {'title': 'Multilingual Hospitality', 'desc': 'Hostesses and officers fluent in English, French, and major indigenous languages.', 'icon': 'languages'},
        ]
    else:
        values = [{'title': v.title, 'desc': v.description, 'icon': v.icon_name} for v in core_values]

    context = {
        'testimonials': testimonials,
        'values': values,
    }
    return render(request, 'agency/about.html', context)


def services_list_view(request):
    category = request.GET.get('category', 'all')
    if category != 'all':
        services = Service.objects.filter(category=category)
    else:
        services = Service.objects.all()
    
    context = {
        'services': services,
        'current_category': category,
    }
    if request.htmx:
        return render(request, 'agency/partials/services_grid.html', context)
    return render(request, 'agency/services.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.exclude(id=service.id)[:3]
    related_portfolio = EventPortfolio.objects.filter(category__in=['corporate', 'conference', 'wedding'])[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
        'related_portfolio': related_portfolio,
    }
    return render(request, 'agency/service_detail.html', context)


def portfolio_list_view(request):
    category = request.GET.get('category', 'all')
    if category and category != 'all':
        portfolio_items = EventPortfolio.objects.filter(category=category)
    else:
        portfolio_items = EventPortfolio.objects.all()

    context = {
        'portfolio_items': portfolio_items,
        'current_category': category,
    }
    if request.htmx:
        return render(request, 'agency/partials/portfolio_grid.html', context)
    return render(request, 'agency/portfolio.html', context)


def portfolio_detail_view(request, slug):
    item = get_object_or_404(EventPortfolio, slug=slug)
    related_events = EventPortfolio.objects.exclude(id=item.id)[:3]
    context = {
        'item': item,
        'related_events': related_events,
    }
    return render(request, 'agency/portfolio_detail.html', context)


def gallery_view(request):
    category = request.GET.get('category', 'all')
    if category and category != 'all':
        gallery_items = GalleryItem.objects.filter(category=category)
    else:
        gallery_items = GalleryItem.objects.all()
        
    uniform_styles = UniformStyle.objects.all()
    
    context = {
        'gallery_items': gallery_items,
        'uniform_styles': uniform_styles,
        'current_category': category,
    }
    if request.htmx:
        return render(request, 'agency/partials/gallery_grid.html', context)
    return render(request, 'agency/gallery.html', context)


def quote_request_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        organization = request.POST.get('organization', '').strip()
        email = request.POST.get('email', '').strip()
        phone_whatsapp = request.POST.get('phone_whatsapp', '').strip()
        event_name = request.POST.get('event_name', '').strip()
        event_type = request.POST.get('event_type', 'Corporate Event')
        event_date = request.POST.get('event_date', '')
        event_location = request.POST.get('event_location', 'Lagos')
        venue_name = request.POST.get('venue_name', '').strip()
        expected_guests = request.POST.get('expected_guests', '100-300')
        duration_hours = int(request.POST.get('duration_hours', 8) or 8)
        crew_count = int(request.POST.get('crew_count', 10) or 10)
        gender_preference = request.POST.get('gender_preference', 'Balanced Mix')
        uniform_preference = request.POST.get('uniform_preference', 'Imperial Black-Tie Tuxedo & Gown')
        special_requirements = request.POST.get('special_requirements', '').strip()
        
        # Collect services checkbox
        services_list = request.POST.getlist('services')
        services_required = ", ".join(services_list) if services_list else "General Event Ushering"

        services_required = ", ".join(services_list) if services_list else "General Event Ushering"

        inquiry = QuoteInquiry.objects.create(
            full_name=full_name,
            organization=organization,
            email=email,
            phone_whatsapp=phone_whatsapp,
            event_name=event_name,
            event_type=event_type,
            event_date=event_date if event_date else '2026-11-01',
            event_duration_hours=duration_hours,
            event_location=event_location,
            venue_name=venue_name or "Venue TBD",
            expected_guests=expected_guests,
            services_required=services_required,
            crew_count=crew_count,
            gender_preference=gender_preference,
            uniform_preference=uniform_preference,
            special_requirements=special_requirements,
        )

        # Generate WhatsApp pre-filled link
        wa_text = (
            f"👑 *THE POISED CREW - BOOKING INQUIRY #{inquiry.id}*\n\n"
            f"👤 *Client:* {full_name} ({organization or 'Private'})\n"
            f"🎉 *Event:* {event_name} ({event_type})\n"
            f"📅 *Date:* {event_date} ({duration_hours} hrs)\n"
            f"📍 *Location:* {venue_name}, {event_location}\n"
            f"👥 *Guests:* {expected_guests} | *Crew Requested:* {crew_count} Officers\n"
            f"👔 *Uniform:* {uniform_preference}\n"
            f"📋 *Services:* {services_required}\n\n"
            f"Hello Lead Protocol Director, I've just submitted an event booking inquiry. Please confirm date availability and provide an official invoice."
        )
        encoded_wa = urllib.parse.quote(wa_text)
        whatsapp_url = f"https://wa.me/2347051851600?text={encoded_wa}"

        context = {
            'inquiry': inquiry,
            'whatsapp_url': whatsapp_url,
        }
        if request.htmx:
            return render(request, 'agency/partials/quote_success.html', context)
        return render(request, 'agency/quote_success_page.html', context)

    # GET request
    prefill_service = request.GET.get('service', '')
    context = {
        'prefill_service': prefill_service,
        'services': Service.objects.all(),
        'uniforms': UniformStyle.objects.all(),
    }
    return render(request, 'agency/quote_request.html', context)


@require_GET
def calculate_estimate_api(request):
    try:
        crew_count = int(request.GET.get('crew_count', 10) or 10)
        duration_hours = int(request.GET.get('duration_hours', 8) or 8)
        services_count = int(request.GET.get('services_count', 2) or 2)
        event_type = request.GET.get('event_type', 'corporate')
    except (ValueError, TypeError):
        crew_count = 10
        duration_hours = 8
        services_count = 2
        event_type = 'corporate'

    base_rate_per_officer = 40000
    if event_type in ['government', 'protocol']:
        base_rate_per_officer = 50000
    elif event_type in ['wedding', 'gala']:
        base_rate_per_officer = 42000

    service_mult = 1.0 + (max(0, services_count - 1) * 0.08)
    hour_mult = max(4, duration_hours) / 8.0
    
    est_base = crew_count * base_rate_per_officer * hour_mult * service_mult
    est_min = int(est_base * 0.9)
    est_max = int(est_base * 1.2)

    context = {
        'crew_count': crew_count,
        'duration_hours': duration_hours,
        'est_min': f"{est_min:,.0f}",
        'est_max': f"{est_max:,.0f}",
    }
    return render(request, 'agency/partials/estimate_badge.html', context)


def join_crew_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_whatsapp = request.POST.get('phone_whatsapp', '').strip()
        gender = request.POST.get('gender', 'Female')
        age = int(request.POST.get('age', 22) or 22)
        height_cm = int(request.POST.get('height_cm', 170) or 170)
        city = request.POST.get('city', 'Lagos')
        education = request.POST.get('education', 'Undergraduate / Graduate')
        languages = request.POST.get('languages', 'English')
        experience_years = request.POST.get('experience_years', '1-2 years')
        experience_summary = request.POST.get('experience_summary', '').strip()
        instagram_handle = request.POST.get('instagram_handle', '').strip()

        app = CrewApplication.objects.create(
            full_name=full_name,
            email=email,
            phone_whatsapp=phone_whatsapp,
            gender=gender,
            age=age,
            height_cm=height_cm,
            city=city,
            education=education,
            languages=languages,
            experience_years=experience_years,
            experience_summary=experience_summary,
            instagram_handle=instagram_handle,
        )

        context = {
            'application': app,
        }
        if request.htmx:
            return render(request, 'agency/partials/recruitment_success.html', context)
        return render(request, 'agency/recruitment_success_page.html', context)

    return render(request, 'agency/join_crew.html')
