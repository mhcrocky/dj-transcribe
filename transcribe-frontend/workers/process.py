import os
from django.conf import settings
from datetime import datetime
import stripe
import boto3

STRIPE_SECRET_KEY = 'sk_test_51ILA0WGzr6eXbH6PrW3FsnAFM55MZ4Eqg6FO464xyQu1WW8nlLpUTunnsdC8fWuNqGIuNkDoo57zyVq1EfXDr0iz00f5eztRR3'
AWS_ACCESS_KEY_ID = 'AKIASOJFJ5RPYZJMYOOY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'transcribe-now'

def delete_files_job():
    stripe.api_key = STRIPE_SECRET_KEY
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
            if (td_days == 0):
                filename = line_item['description']
                # delete the file from S3 bucket
                s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                obj = s3.Object(AWS_STORAGE_BUCKET_NAME, 'uploads/'+filename)
                obj.delete()
                print('delete file',filename)
if __name__ == '__main__':
     delete_files_job()