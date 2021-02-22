import os
from django.conf import settings
from datetime import datetime
import stripe
import boto3
from modules.download import voice
from modules.parse import parse
STRIPE_SECRET_KEY = 'sk_test_51ILA0WGzr6eXbH6PrW3FsnAFM55MZ4Eqg6FO464xyQu1WW8nlLpUTunnsdC8fWuNqGIuNkDoo57zyVq1EfXDr0iz00f5eztRR3'
AWS_ACCESS_KEY_ID = 'AKIASOJFJ5RPYZJMYOOY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'transcribe-now'

ASSEMBLY_AI_KEY = '1fc3ded0edaa4851b288051bff6e56d5'
stripe.api_key = STRIPE_SECRET_KEY
checkout_list = stripe.checkout.Session.list()['data']

def delete_files_job():

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
                s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                obj = s3.Object(AWS_STORAGE_BUCKET_NAME, 'uploads/'+filename)
                obj.delete()
                print('delete file',filename)


def transcription_job():
    ai = voice.AssemblyAi(ASSEMBLY_AI_KEY)
    audio_url = "https://s3-us-west-2.amazonaws.com/blog.assemblyai.com/audio/8-7-2018-post/7510.mp3"
    tag = ai.transcribe(audio_url)
    res = ai.poll('l4getqqv4-4120-457b-9e72-e020f05d2a12')

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

if __name__ == '__main__':
     delete_files_job()