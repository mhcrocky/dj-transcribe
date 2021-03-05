import os
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from datetime import datetime
import stripe
import json
import boto3
from modules.download import voice
from modules.parse import parse


def delete_files_job():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_list = stripe.checkout.Session.list()['data']
    for checkout in checkout_list:
        if checkout['payment_status'] == 'unpaid':
            checkout_id = checkout['id']
            line_items = stripe.checkout.Session.list_line_items(checkout_id)
            [line_item] = line_items
            created_at = line_item['price']['created']
            now = datetime.now()
            td = now - datetime.fromtimestamp(created_at)

            td_days = int((round(td.total_seconds() / 60))/60/24)
            # deletefile
            if (td_days > 7):
                filename = line_item['description']
                # delete the file from S3 bucket
                #TODO: delete json file
                s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'uploads/'+filename)
                obj.delete()
                print('delete file',filename)

#
def transcription_job():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_list = stripe.checkout.Session.list()['data']
    ai = voice.AssemblyAi(settings.ASSEMBLY_AI_KEY)
    print('transcribe_job')
    for checkout in checkout_list:
        if(checkout['payment_status'] == 'paid'):
            payment_intent_id = checkout['payment_intent']
            
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            payment_intent_status = payment_intent['metadata']['status']

            if(payment_intent_status == 'pending'):
                if(ai.poll(payment_intent['metadata']['tag'])=='okay'):
                    stripe.PaymentIntent.modify(
                        payment_intent_id,
                        metadata={"status": "polling"},
                    )
                else:
                    stripe.PaymentIntent.modify(
                        payment_intent_id,
                        metadata={"status": "cancelled"},
                    )

#send email with result pdf file
def send_result_job():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_list = stripe.checkout.Session.list()['data']

    for checkout in checkout_list:
        if(checkout['payment_status'] == 'paid'):
            payment_intent_id = checkout['payment_intent']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            payment_intent_status = payment_intent['metadata']['status']
            tag = payment_intent['metadata']['tag']

            if(payment_intent_status == 'polling'):
                #get json file from s3 and generate pdf file
                subject = 'This is subject'
                message = 'This is message'
                customer_email = checkout['customer_details']['email']
                print(f'will send email to :{customer_email}')

                s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'uploads/json/{tag}.json')
                words = json.loads(obj.get()['Body'].read().decode('utf-8'))['words']

                txtfile = parse.generateTxt(words,isTimeStamp=True)
                pdffile = parse.generatePDF(words)
                srtfile = parse.generateSrt(words)

                # send email to customer
                mail = EmailMessage( subject , message , 'andreii@picknmelt.com', [customer_email,])
                mail.attach('trascribe.pdf', pdffile, 'pdf/pdf')
                mail.attach('trascribe.txt', txtfile, 'txt/txt')
                mail.attach('trascribe.srt', srtfile, 'srt/srt')
                mail.send()

                #set state to finished
                stripe.PaymentIntent.modify(
                    payment_intent_id,
                    metadata={"status": "finished"},
                )
