from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Profile, Skill, Project, Experience, ContactMessage
from .forms import ContactForm


def send_contact_notification(contact_message, profile=None):
    """Send the contact submission email to the portfolio owner."""
    recipient_list = []
    if profile and profile.email:
        recipient_list.append(profile.email)
    if settings.DEFAULT_FROM_EMAIL and settings.DEFAULT_FROM_EMAIL not in recipient_list:
        recipient_list.append(settings.DEFAULT_FROM_EMAIL)
    if not recipient_list:
        recipient_list = [settings.DEFAULT_FROM_EMAIL]

    subject = f'Portfolio Contact: {contact_message.subject}'
    message = (
        f'From: {contact_message.name} ({contact_message.email})\n\n'
        f'{contact_message.message}'
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)


def home(request):
    """Home page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    skills = Skill.objects.all()
    featured_projects = Project.objects.filter(featured=True)[:3]
    if not featured_projects:
        featured_projects = Project.objects.all()[:3]
    recent_projects = Project.objects.filter(featured=False)[:3]
    experiences = Experience.objects.all()[:5]
    
    context = {
        'profile': profile,
        'skills': skills,
        'featured_projects': featured_projects,
        'recent_projects': recent_projects,
        'experiences': experiences,
    }
    
    return render(request, 'portfolio/home.html', context)


def about(request):
    """About page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
    }
    
    return render(request, 'portfolio/about.html', context)


def projects(request):
    """Projects page view"""
    profile = Profile.objects.first()
    all_projects = Project.objects.all()
    
    context = {
        'profile': profile,
        'projects': all_projects,
    }
    
    return render(request, 'portfolio/projects.html', context)


def contact(request):
    """Contact page view"""
    profile = Profile.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_contact_notification(contact_message, profile)
            except Exception as e:
                print(f"Email sending failed: {e}")

            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'form': form,
    }
    
    return render(request, 'portfolio/contact.html', context)


def project_detail(request, project_id):
    """Project detail page view"""
    profile = Profile.objects.first()

    try:
        project = Project.objects.get(id=project_id)
        related_projects = Project.objects.exclude(id=project_id)[:3]
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('projects')
    
    context = {
        'profile': profile,
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'portfolio/project_detail.html', context)


def api_contact(request):
    """API endpoint for contact form (AJAX)"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_contact_notification(contact_message, Profile.objects.first())
            except Exception as e:
                print(f"Email sending failed: {e}")
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


