#!/usr/bin/python

# SaaS Utils script
# Update metadata for PaymentIntent and fetch by metadata

import sys, getopt
import stripe
import json
import requests
from pytube import YouTube
import re


STRIPE_SECRET_KEY = 'sk_test_51I7A7ACXNKb5cnwi9ddh35YkIJUo4DzPinbimiHhqqNe2ZBvmE3gwJ9YRBwziFaJiQOqX0BwlmFRQzr9kZwyIhQd00vKy8owwf'

# update PaymentIntent metadata
# @pi_id: PaymentIntent id
# @meta_key: PaymentIntent metadata key
# @meta_value: PaymentIntent metadata value
def update_custom_value_for_payment(pi_id, meta_key, meta_value):
    stripe.api_key = STRIPE_SECRET_KEY
    result = stripe.PaymentIntent.modify( 
        pi_id, 
        metadata={meta_key: meta_value}, 
        )
    msg = 'Custom value update failed'
    if result.get['id'] == pi_id:
        msg = 'Successfully updated custom value'
    
    print(msg)


# list payment intent by metadata
# @limit: count of objects to be fetched
# @meta_value: metadata value to be used to search
def list_paymentintent_by_meta(meta_value, limit=10):
    # stripe_endpoint = 'https://dashboard.stripe.com/v1/search'
    stripe_endpoint = 'https://api.stripe.com/v1/search'
    # payload = {'prefix': 'false', 'query': 'metadata:{}'.format(meta_value), 'facets': 'true', 'count': limit}
    payload = {'prefix': 'false', 'query': 'video_url:{}'.format(meta_value), 'facets': 'true', 'count': limit}
    print(payload)
    resp = requests.get(stripe_endpoint, 
        headers={ 'Authorization': 'Bearer {}'.format(STRIPE_SECRET_KEY) }, 
        params=payload)
    results = resp.json()
    items = results.get('data')
    # payment_intent
    payment_intents = list(filter(lambda x: x.get('object') == 'payment_intent', items))
    # print first item to the console
    if len(payment_intents) == 0:
        print("Can not find object for specified meta value.")
        sys.exit()
    print(payment_intents)

usage_text = 'Usage\n python saas_utils.py list <video_link> <limit>\n \
            or \n python saas_utils.py update <pi_id> <meta_key> <meta_value>'

# "https://www.youtube.com/watch?v=7fUaUw7PU7M&feature=youtu.be"
def main(argv):
    command = argv[0]
    if command == 'list':
        if len(argv) < 3:
            print('Usage python saas_utils.py list <video_link> <limit>')
            sys.exit()
        meta_value = argv[1]
        limit = int(argv[2]) if (int(argv[2]) > 0) else 10
        list_paymentintent_by_meta(meta_value, limit)
    elif command == 'update':
        if len(argv) < 4:
            print('Usage python saas_utils.py update <pi_id> <meta_key> <meta_value>')
            sys.exit()
        pi_id = argv[1]
        meta_key = argv[2]
        meta_value = argv[3]
        print(pi_id, meta_value, meta_key)
        # update_custom_value_for_payment(pi_id, meta_key, meta_value)
    else:
        print(usage_text)
        sys.exit()


if __name__ == "__main__":
   if len(sys.argv) == 1:
       print(usage_text)
       sys.exit()
   main(sys.argv[1:])

