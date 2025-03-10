from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from profiles.models import UserProfile
from reviews.models import Review

from .models import Message
from .forms import MessageForm


@login_required
def management(request):
    """
    A view to return the Site Management Page
    """

    # Checks user is superuser
    # redirects to home if not
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only Admin or Emporium Staff  can do that.')
        return redirect(reverse('home'))

    # Gets unapproved Reviews from DB
    unapproved_reviews = Review.objects.filter(
        is_approved=False).order_by('-created_on')

    # Gets messages from DB
    customer_messages = Message.objects.all().order_by('-created_on')

    # Reset filter variables
    open = None
    current_filter = None

    # Handles product filtering by is_open
    if 'open' in request.GET:
        open = request.GET['open']
        customer_messages = customer_messages.filter(
            is_open=open).order_by('-created_on').values()

        # Sets current filter value
        if open == "False":
            current_filter = "Closed"
        else:
            current_filter = "Open"

    context = {
        'customer_messages': customer_messages,
        'current_filter': current_filter,
        'reviews': unapproved_reviews
    }

    return render(request, 'management/management.html', context)


@login_required
def toggle_message(request, message_id):
    """
    A View to toggle the message open / closed
    """

    # Checks user is superuser
    # redirects to home if not
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only admin/staff can access that page.')
        return redirect(reverse('home'))

    try:
        # Gets the message from DB
        message = get_object_or_404(Message, id=message_id)

        # Gets value of hidden input
        message_open = request.POST.get('is_open')

        # Sets value of is_open field on DB
        if message_open == "True":
            message.is_open = True
        else:
            message.is_open = False
        message.save()
        messages.success(request, "Message status updated successfully")

        # Gets current filter value
        current_filter = request.POST.get('current_filter')

        # Redirects to 'management' view with query if current_filter set
        # Maintains current filtering
        if current_filter == "None":
            return redirect(reverse('management'))
        else:
            if current_filter == "Closed":
                query = "?open=False"
            elif current_filter == "Open":
                query = "?open=True"

            return redirect(reverse('management') + query)

    # Handles errors
    except Exception as e:
        messages.error(
            request,
            'Sorry, the message status could not be updated. ' +
            'Please try again later.'
        )
        return HttpResponse(content=e, status=400)


def contact_us(request):
    """
    Renders form to add message / contact us.
    Adds new message to database.
    """

    if request.user.is_authenticated:
        # Sets author based on current user
        user = User.objects.get(username=request.user)
    else:
        user = None

    # Handles Form Submission
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save()
            message.user = user
            message.save()

            request.session['show_bag_summary'] = False
            messages.success(request, "Your message has been sent.")
            # go to products page on succesful send
            return redirect(reverse('products'))
        else:
            messages.error(request, "Form invalid, please try again.")

    # Handles View Rendering
    else:

        # Attempt to prefill form with user info
        # If not render empty form
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                form = MessageForm(initial={
                    'name': profile.user.get_full_name(),
                    'email': profile.user.email,
                })
            except UserProfile.DoesNotExist:
                form = MessageForm()
        else:
            form = MessageForm()

    # Sets page template
    template = 'management/contact_us.html'

    # Sets current product & form content
    context = {
        'form': form,
    }

    return render(request, template, context)
