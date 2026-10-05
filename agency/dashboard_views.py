import json
import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Service, EventPortfolio, UniformStyle, GalleryItem, Testimonial, QuoteInquiry, CrewApplication


def dashboard_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('agency:dashboard_home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('agency:dashboard_home')
        else:
            messages.error(request, 'Invalid administrative credentials.')
            
    return render(request, 'dashboard/login.html')


def dashboard_logout_view(request):
    logout(request)
    return redirect('agency:dashboard_login')


@login_required(login_url='agency:dashboard_login')
def dashboard_home_view(request):
    total_inquiries = QuoteInquiry.objects.count()
    new_inquiries = QuoteInquiry.objects.filter(status='new').count()
    confirmed_events = QuoteInquiry.objects.filter(status='confirmed').count()
    total_applications = CrewApplication.objects.count()
    pending_applications = CrewApplication.objects.filter(status='pending').count()
    total_services = Service.objects.count()
    total_case_studies = EventPortfolio.objects.count()

    recent_inquiries = QuoteInquiry.objects.all()[:6]
    recent_applications = CrewApplication.objects.all()[:5]

    context = {
        'total_inquiries': total_inquiries,
        'new_inquiries': new_inquiries,
        'confirmed_events': confirmed_events,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'total_services': total_services,
        'total_case_studies': total_case_studies,
        'recent_inquiries': recent_inquiries,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/index.html', context)


# ==================== CRM: INQUIRIES & BOOKINGS ====================

@login_required(login_url='agency:dashboard_login')
def inquiries_list_view(request):
    status = request.GET.get('status', 'all')
    search = request.GET.get('q', '').strip()
    
    inquiries = QuoteInquiry.objects.all()
    if status != 'all':
        inquiries = inquiries.filter(status=status)
    if search:
        inquiries = inquiries.filter(full_name__icontains=search) | inquiries.filter(event_name__icontains=search) | inquiries.filter(organization__icontains=search)

    context = {
        'inquiries': inquiries,
        'current_status': status,
        'search_query': search,
    }
    return render(request, 'dashboard/inquiries_list.html', context)


@login_required(login_url='agency:dashboard_login')
def inquiry_detail_view(request, pk):
    inquiry = get_object_or_404(QuoteInquiry, pk=pk)

    # Pre-formatted WhatsApp reply message
    reply_msg = (
        f"👑 *THE POISED CREW - OFFICIAL PROPOSAL & AVAILABILITY*\n\n"
        f"Dear {inquiry.full_name},\n"
        f"Thank you for reaching out regarding *{inquiry.event_name}* on *{inquiry.event_date}*.\n\n"
        f"We have reserved your preliminary date slot for {inquiry.crew_count} Protocol Officers ({inquiry.uniform_preference}).\n"
        f"Our team lead is ready to discuss the final itinerary and dispatch requirements.\n\n"
        f"Best regards,\n"
        f"*Lead Protocol Director, The Poised Crew*"
    )
    encoded_msg = urllib.parse.quote(reply_msg)
    clean_phone = inquiry.phone_whatsapp.replace(' ', '').replace('+', '').replace('-', '')
    if clean_phone.startswith('0'):
        clean_phone = '234' + clean_phone[1:]
    whatsapp_reply_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"

    context = {
        'inquiry': inquiry,
        'whatsapp_reply_url': whatsapp_reply_url,
    }
    return render(request, 'dashboard/inquiry_detail.html', context)


@login_required(login_url='agency:dashboard_login')
def inquiry_update_status_view(request, pk):
    inquiry = get_object_or_404(QuoteInquiry, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(QuoteInquiry.STATUS_CHOICES):
            inquiry.status = new_status
            inquiry.save()
            messages.success(request, f"Inquiry #{inquiry.id} status updated to '{inquiry.get_status_display()}'.")
            
    if request.htmx:
        return render(request, 'dashboard/partials/inquiry_status_badge.html', {'inquiry': inquiry})
    return redirect('agency:inquiry_detail', pk=pk)


@login_required(login_url='agency:dashboard_login')
def inquiry_delete_view(request, pk):
    inquiry = get_object_or_404(QuoteInquiry, pk=pk)
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, 'Inquiry deleted successfully.')
        return redirect('agency:inquiries_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Inquiry', 'item_name': inquiry.event_name, 'cancel_url': 'agency:inquiries_list'})


# ==================== CONTENT CMS: SERVICES ====================

@login_required(login_url='agency:dashboard_login')
def services_admin_list_view(request):
    services = Service.objects.all()
    return render(request, 'dashboard/services_list.html', {'services': services})


@login_required(login_url='agency:dashboard_login')
def service_form_view(request, pk=None):
    service = get_object_or_404(Service, pk=pk) if pk else None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'ushering')
        badge_text = request.POST.get('badge_text', '').strip()
        icon_name = request.POST.get('icon_name', 'crown').strip()
        short_description = request.POST.get('short_description', '').strip()
        full_description = request.POST.get('full_description', '').strip()
        deliverables = request.POST.get('deliverables', '').strip()
        suitable_events = request.POST.get('suitable_events', '').strip()
        uniform_recommendations = request.POST.get('uniform_recommendations', '').strip()
        is_featured = request.POST.get('is_featured') == 'on'
        order = int(request.POST.get('order', 0) or 0)

        if service:
            service.title = title
            service.category = category
            service.badge_text = badge_text
            service.icon_name = icon_name
            service.short_description = short_description
            service.full_description = full_description
            service.deliverables = deliverables
            service.suitable_events = suitable_events
            service.uniform_recommendations = uniform_recommendations
            service.is_featured = is_featured
            service.order = order
            service.save()
            messages.success(request, f"Service '{service.title}' updated successfully.")
        else:
            service = Service.objects.create(
                title=title,
                category=category,
                badge_text=badge_text,
                icon_name=icon_name,
                short_description=short_description,
                full_description=full_description,
                deliverables=deliverables,
                suitable_events=suitable_events,
                uniform_recommendations=uniform_recommendations,
                is_featured=is_featured,
                order=order,
            )
            messages.success(request, f"New service '{service.title}' created.")

        return redirect('agency:services_admin_list')

    context = {
        'service': service,
        'categories': Service.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/service_form.html', context)


@login_required(login_url='agency:dashboard_login')
def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, f"Service '{service.title}' deleted.")
        return redirect('agency:services_admin_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Service', 'item_name': service.title, 'cancel_url': 'agency:services_admin_list'})


# ==================== CONTENT CMS: EVENT PORTFOLIO ====================

@login_required(login_url='agency:dashboard_login')
def portfolio_admin_list_view(request):
    portfolio_items = EventPortfolio.objects.all()
    return render(request, 'dashboard/portfolio_list.html', {'portfolio_items': portfolio_items})


@login_required(login_url='agency:dashboard_login')
def portfolio_form_view(request, pk=None):
    item = get_object_or_404(EventPortfolio, pk=pk) if pk else None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'corporate')
        date_held = request.POST.get('date_held')
        location = request.POST.get('location', '').strip()
        city = request.POST.get('city', '').strip()
        client_name = request.POST.get('client_name', '').strip()
        planner_name = request.POST.get('planner_name', '').strip()
        crew_deployed = int(request.POST.get('crew_deployed', 20) or 20)
        services_provided = request.POST.get('services_provided', '').strip()
        summary = request.POST.get('summary', '').strip()
        highlight_result = request.POST.get('highlight_result', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        is_featured = request.POST.get('is_featured') == 'on'
        order = int(request.POST.get('order', 0) or 0)

        if item:
            item.title = title
            item.category = category
            if date_held:
                item.date_held = date_held
            item.location = location
            item.city = city
            item.client_name = client_name
            item.planner_name = planner_name
            item.crew_deployed = crew_deployed
            item.services_provided = services_provided
            item.summary = summary
            item.highlight_result = highlight_result
            item.image_url = image_url
            item.is_featured = is_featured
            item.order = order
            item.save()
            messages.success(request, f"Case study '{item.title}' updated.")
        else:
            item = EventPortfolio.objects.create(
                title=title,
                category=category,
                date_held=date_held if date_held else '2026-01-01',
                location=location,
                city=city,
                client_name=client_name,
                planner_name=planner_name,
                crew_deployed=crew_deployed,
                services_provided=services_provided,
                summary=summary,
                highlight_result=highlight_result,
                image_url=image_url,
                is_featured=is_featured,
                order=order,
            )
            messages.success(request, f"New case study '{item.title}' added.")

        return redirect('agency:portfolio_admin_list')

    context = {
        'item': item,
        'categories': EventPortfolio.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/portfolio_form.html', context)


@login_required(login_url='agency:dashboard_login')
def portfolio_delete_view(request, pk):
    item = get_object_or_404(EventPortfolio, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f"Case study '{item.title}' deleted.")
        return redirect('agency:portfolio_admin_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Case Study', 'item_name': item.title, 'cancel_url': 'agency:portfolio_admin_list'})


# ==================== CONTENT CMS: GALLERY & UNIFORMS ====================

@login_required(login_url='agency:dashboard_login')
def gallery_admin_list_view(request):
    gallery_items = GalleryItem.objects.all()
    uniforms = UniformStyle.objects.all()
    return render(request, 'dashboard/gallery_list.html', {'gallery_items': gallery_items, 'uniforms': uniforms})


@login_required(login_url='agency:dashboard_login')
def gallery_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'events')
        image_url = request.POST.get('image_url', '').strip()
        caption = request.POST.get('caption', '').strip()
        order = int(request.POST.get('order', 0) or 0)

        GalleryItem.objects.create(
            title=title,
            category=category,
            image_url=image_url,
            caption=caption,
            order=order
        )
        messages.success(request, 'Gallery item added.')
        return redirect('agency:gallery_admin_list')
    
    return render(request, 'dashboard/gallery_form.html', {'categories': GalleryItem.CATEGORY_CHOICES})


@login_required(login_url='agency:dashboard_login')
def gallery_delete_view(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Gallery item removed.')
        return redirect('agency:gallery_admin_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Gallery Item', 'item_name': item.title, 'cancel_url': 'agency:gallery_admin_list'})


@login_required(login_url='agency:dashboard_login')
def uniform_form_view(request, pk=None):
    uniform = get_object_or_404(UniformStyle, pk=pk) if pk else None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        tag = request.POST.get('tag', '').strip()
        description = request.POST.get('description', '').strip()
        gender = request.POST.get('gender', 'Unisex').strip()
        color_palette = request.POST.get('color_palette', '').strip()
        image_url = request.POST.get('image_url', '').strip()

        if uniform:
            uniform.name = name
            uniform.tag = tag
            uniform.description = description
            uniform.gender = gender
            uniform.color_palette = color_palette
            uniform.image_url = image_url
            uniform.save()
            messages.success(request, f"Uniform style '{uniform.name}' updated.")
        else:
            UniformStyle.objects.create(
                name=name,
                tag=tag,
                description=description,
                gender=gender,
                color_palette=color_palette,
                image_url=image_url
            )
            messages.success(request, f"New uniform style '{name}' created.")

        return redirect('agency:gallery_admin_list')

    return render(request, 'dashboard/uniform_form.html', {'uniform': uniform})


@login_required(login_url='agency:dashboard_login')
def uniform_delete_view(request, pk):
    uniform = get_object_or_404(UniformStyle, pk=pk)
    if request.method == 'POST':
        uniform.delete()
        messages.success(request, 'Uniform style removed.')
        return redirect('agency:gallery_admin_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Uniform Style', 'item_name': uniform.name, 'cancel_url': 'agency:gallery_admin_list'})


# ==================== TALENT / CREW RECRUITMENT ====================

@login_required(login_url='agency:dashboard_login')
def crew_applications_list_view(request):
    status = request.GET.get('status', 'all')
    apps = CrewApplication.objects.all()
    if status != 'all':
        apps = apps.filter(status=status)
    return render(request, 'dashboard/crew_list.html', {'applications': apps, 'current_status': status})


@login_required(login_url='agency:dashboard_login')
def crew_application_detail_view(request, pk):
    app = get_object_or_404(CrewApplication, pk=pk)
    return render(request, 'dashboard/crew_detail.html', {'application': app})


@login_required(login_url='agency:dashboard_login')
def crew_application_update_status_view(request, pk):
    app = get_object_or_404(CrewApplication, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(CrewApplication.STATUS_CHOICES):
            app.status = new_status
            app.save()
            messages.success(request, f"Application for '{app.full_name}' updated to {app.get_status_display()}.")
    return redirect('agency:crew_application_detail', pk=pk)


# ==================== TESTIMONIALS CMS ====================

@login_required(login_url='agency:dashboard_login')
def testimonials_admin_list_view(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})


@login_required(login_url='agency:dashboard_login')
def testimonial_form_view(request, pk=None):
    testimonial = get_object_or_404(Testimonial, pk=pk) if pk else None

    if request.method == 'POST':
        client_name = request.POST.get('client_name', '').strip()
        client_role_company = request.POST.get('client_role_company', '').strip()
        event_name = request.POST.get('event_name', '').strip()
        quote = request.POST.get('quote', '').strip()
        rating = int(request.POST.get('rating', 5) or 5)
        is_featured = request.POST.get('is_featured') == 'on'

        if testimonial:
            testimonial.client_name = client_name
            testimonial.client_role_company = client_role_company
            testimonial.event_name = event_name
            testimonial.quote = quote
            testimonial.rating = rating
            testimonial.is_featured = is_featured
            testimonial.save()
            messages.success(request, 'Testimonial updated.')
        else:
            Testimonial.objects.create(
                client_name=client_name,
                client_role_company=client_role_company,
                event_name=event_name,
                quote=quote,
                rating=rating,
                is_featured=is_featured
            )
            messages.success(request, 'New testimonial added.')

        return redirect('agency:testimonials_admin_list')

    return render(request, 'dashboard/testimonial_form.html', {'testimonial': testimonial})


@login_required(login_url='agency:dashboard_login')
def testimonial_delete_view(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted.')
        return redirect('agency:testimonials_admin_list')
    return render(request, 'dashboard/confirm_delete.html', {'item_type': 'Testimonial', 'item_name': testimonial.client_name, 'cancel_url': 'agency:testimonials_admin_list'})
