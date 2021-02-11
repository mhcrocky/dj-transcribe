import os
from datetime import datetime
import stripe


def delete_files_job():
    checkout_list = stripe.checkout.Session.list()['data']
    for checkout in checkout_list:
        if checkout['payment_status'] == 'unpaid':
            checkout_id = checkout['id']
            line_items = stripe.checkout.Session.list_line_items(checkout_id)
            [line_item] = line_items
            created_at = line_item['created']
            now = datetime.now().timestamp()
            td = now - created_at

            td_days = int((round(td.total_seconds() / 60))/60/24)

            # deletefile
            if (td_days > 7):
                filename = line_item['filename']
                # delete the file from S3 bucket
                s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
                bucket.delete_object(Bucket=s3, Key=filename)
                print('delete file')