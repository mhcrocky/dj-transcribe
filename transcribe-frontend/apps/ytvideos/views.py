# backend/server/apps/ytvideos/views.py
import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import json
from django.core.mail import send_mail
from rest_framework import viewsets 
from pytube import YouTube

from apps.ytvideos.models import Ytvideo 
from apps.ytvideos.serializers import YtvideoSerializer


class YtvideoViewSet(viewsets.ModelViewSet):

    serializer_class = YtvideoSerializer
    queryset = Ytvideo.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter()


class HomePageView(TemplateView):
    template_name = 'home.html'


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


# For processing stripe payments
@csrf_exempt
def retrieve_ytvideo_info(request):
    if request.method == 'GET':
        video_url = request.GET.get('url', '')
        print("Youtube Link:", video_url)
        try:  
            # object creation using YouTube 
            yt = YouTube(video_url)
            video_info = {
              'title': yt.title,
              'length': yt.length,
              'description': yt.description,
              'keywords': yt.keywords,
              'author': yt.author,
              'thumbnail_url': yt.thumbnail_url,
              'publish_date': yt.publish_date,
              'rating': yt.rating,
              'url': video_url,
            }

            # Test data for the frontend
            # video_info = {
            #   'title': 'Learn React JS - Full Course for Beginners - Tutorial 2019',
            #   'length': 18334,
            #   'description': "React.js is a JavaScript library for building dynamic web applications. Upon completion of this course, you'll know everything you need in order to build web applications in React.",
            #   'keywords': '["react", "react full course", "react tutorial", "react.js", "tutorial"]',
            #   'author': 'freeCodeCamp.org',
            #   'thumbnail_url': 'https://i.ytimg.com/vi/DLX62G4lc44/maxresdefault.jpg',
            #   'publish_date': '2018-12-18T00:00:00',
            #   'rating': 4.9596257,
            #   'url': video_url,
            # }
            response = JsonResponse(video_info, safe=False)
            return response
        except:  
            print("Connection Error") #to handle exception
            message = 'Bad request' 
            response = JsonResponse({'status':'false','message':message}, status=400)
            return response
        

# Send email on success payment
def email(customer_email, customer_name):
    subject = 'Thank you for using our service.'
    message = 'Success, you will receive your transcription shortly.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [customer_email,]
    send_mail( subject, message, 'andreii@picknmelt.com', recipient_list, fail_silently=False)


# For processing stripe payments
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        success_url = request.build_absolute_uri('/success/')
        cancel_url = request.build_absolute_uri('/cancelled/')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        post_data = json.loads(request.body.decode("utf-8"))
        print("Request payload: ", post_data)
        video_length = post_data.get('length', 0)
        video_link = post_data.get('url', 'www.youtube.com')
        video_title = post_data.get('title', 'Youtube Video')
        price = int(video_length/60) if (int(video_length/60) > 50) else 50
        try:
            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=success_url,
                cancel_url=cancel_url,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': video_title,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': str(price),
                        'description': video_title,
                    }
                ],
                payment_intent_data={'metadata': {'video_url': video_link, 'status': 'pending', 'processId': 'processId'}}
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        # print("session:", session)
        # This method will be called when user successfully purchases something.
        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    # client_reference_id = user's id
    customer_email = session['charges']['data'][0]['billing_details']['email']
    customer_name = session['charges']['data'][0]['billing_details']['name']
    print("session:", customer_email)
    email(customer_email, customer_name)
    client_reference_id = session.get("client_reference_id")
    payment_intent = session.get("payment_intent")

    if client_reference_id is None:
        # Customer wasn't logged in when purchasing
        return

    # Customer was logged in we can now fetch the Django user and make changes to our models
    try:
        user = User.objects.get(id=client_reference_id)
        print(user.username, "just purchased something.")
    except User.DoesNotExist:
        pass

