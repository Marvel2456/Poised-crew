from django.urls import path
from . import views
from . import dashboard_views

app_name = 'agency'

urlpatterns = [
    # Public Website Routes
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_list_view, name='services'),
    path('services/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('portfolio/', views.portfolio_list_view, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail_view, name='portfolio_detail'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('book/', views.quote_request_view, name='book'),
    path('api/estimate/', views.calculate_estimate_api, name='estimate_api'),
    path('join-crew/', views.join_crew_view, name='join_crew'),

    # Executive Dashboard & CRM Routes
    path('dashboard/', dashboard_views.dashboard_home_view, name='dashboard_home'),
    path('dashboard/login/', dashboard_views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/logout/', dashboard_views.dashboard_logout_view, name='dashboard_logout'),

    # CRM Inquiries
    path('dashboard/inquiries/', dashboard_views.inquiries_list_view, name='inquiries_list'),
    path('dashboard/inquiries/<int:pk>/', dashboard_views.inquiry_detail_view, name='inquiry_detail'),
    path('dashboard/inquiries/<int:pk>/status/', dashboard_views.inquiry_update_status_view, name='inquiry_update_status'),
    path('dashboard/inquiries/<int:pk>/delete/', dashboard_views.inquiry_delete_view, name='inquiry_delete'),

    # CMS Services
    path('dashboard/services/', dashboard_views.services_admin_list_view, name='services_admin_list'),
    path('dashboard/services/create/', dashboard_views.service_form_view, name='service_create'),
    path('dashboard/services/<int:pk>/edit/', dashboard_views.service_form_view, name='service_edit'),
    path('dashboard/services/<int:pk>/delete/', dashboard_views.service_delete_view, name='service_delete'),

    # CMS Event Portfolio
    path('dashboard/portfolio/', dashboard_views.portfolio_admin_list_view, name='portfolio_admin_list'),
    path('dashboard/portfolio/create/', dashboard_views.portfolio_form_view, name='portfolio_create'),
    path('dashboard/portfolio/<int:pk>/edit/', dashboard_views.portfolio_form_view, name='portfolio_edit'),
    path('dashboard/portfolio/<int:pk>/delete/', dashboard_views.portfolio_delete_view, name='portfolio_delete'),

    # CMS Gallery & Uniforms
    path('dashboard/gallery/', dashboard_views.gallery_admin_list_view, name='gallery_admin_list'),
    path('dashboard/gallery/create/', dashboard_views.gallery_create_view, name='gallery_create'),
    path('dashboard/gallery/<int:pk>/delete/', dashboard_views.gallery_delete_view, name='gallery_delete'),
    path('dashboard/uniforms/create/', dashboard_views.uniform_form_view, name='uniform_create'),
    path('dashboard/uniforms/<int:pk>/edit/', dashboard_views.uniform_form_view, name='uniform_edit'),
    path('dashboard/uniforms/<int:pk>/delete/', dashboard_views.uniform_delete_view, name='uniform_delete'),

    # Crew Recruitment
    path('dashboard/crew-applications/', dashboard_views.crew_applications_list_view, name='crew_applications_list'),
    path('dashboard/crew-applications/<int:pk>/', dashboard_views.crew_application_detail_view, name='crew_application_detail'),
    path('dashboard/crew-applications/<int:pk>/status/', dashboard_views.crew_application_update_status_view, name='crew_application_update_status'),

    # Testimonials CMS
    path('dashboard/testimonials/', dashboard_views.testimonials_admin_list_view, name='testimonials_admin_list'),
    path('dashboard/testimonials/create/', dashboard_views.testimonial_form_view, name='testimonial_create'),
    path('dashboard/testimonials/<int:pk>/edit/', dashboard_views.testimonial_form_view, name='testimonial_edit'),
    path('dashboard/testimonials/<int:pk>/delete/', dashboard_views.testimonial_delete_view, name='testimonial_delete'),
]
