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

            if (td_days > 7):
                filename = line_item['filename']
                # deletefile
                # we should mention the path also in a constant
                os.remove(filename)
                print('delete file')