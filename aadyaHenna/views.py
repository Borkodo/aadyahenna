from datetime import datetime

from django.shortcuts import render, redirect
from media_manager.models import Event, ArtProject, Tag, HennaDesign
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from media_manager.forms import ContactForm
from django.db.models import Q


def home(request):
    designs = HennaDesign.objects.filter(is_featured=True)
    current_time = timezone.now()
    upcoming_events = Event.objects.filter(date__gte=current_time).order_by('date')
    return render(request, 'home.html', {'designs': designs, 'events': upcoming_events})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            company = form.cleaned_data['company']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Create email content
            text_content = """
            Name: {name}
            Company: {company}
            Email: {email}

            Message:
            {message}
            """.format(name=name, company=company, email=email, message=message)

            html_content = """
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Company:</strong> {company}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            """.format(name=name, company=company, email=email, message=message.replace('\n', '<br>'))

            # Send email
            email_message = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact_success.html')


def art_portfolio(request):
    query = request.GET.get('q', '')
    tags_filter = [tag for tag in request.GET.getlist('tags') if tag]

    projects = ArtProject.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(role__icontains=query)
        )

    if tags_filter:
        projects = projects.filter(tags__name__in=tags_filter).distinct()

    all_tags = Tag.objects.all()
    return render(request, 'art_portfolio.html', {
        'projects': projects,
        'all_tags': all_tags,
        'query': query,
        'tags_filter': tags_filter,
    })


def henna_gallery(request):
    designs = HennaDesign.objects.all()
    return render(request, 'henna_gallery.html', {'designs': designs})
