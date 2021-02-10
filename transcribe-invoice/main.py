#!/usr/bin/env python3

import sys
import codecs
import yaml
import json
import locale

from pybars import Compiler
from weasyprint import HTML


# generate invoice
# @document_data: invoice dict
# @output_pdf: output pdf str
# @locale_lang: locale str
def generate_invoice(document_data, output_pdf, locale_lang):

    locale.setlocale(locale.LC_ALL, locale_lang)

    base_url = 'template'
    index_html = base_url+'/index.html'

    pos_number = 1
    document_data['totals'] = {
        'netto' : 0,
        'brutto': 0,
        'tax': 0        
    }
    for pos in document_data['positions']:
        if not 'tax_rate' in pos:
            pos['tax_rate'] = document_data['tax_rate']

        pos['pos_number'] = pos_number
        pos['total_netto_price'] = pos['netto_price'] * pos['amount']
        pos['total_tax'] = pos['total_netto_price'] * (pos['tax_rate'] / float(100))
        pos['total_brutto_price'] = pos['total_netto_price'] + pos['total_tax']

        document_data['totals']['netto'] += pos['total_netto_price']
        document_data['totals']['brutto'] += pos['total_brutto_price']
        document_data['totals']['tax'] += pos['total_tax']

        pos['amount'] = locale.format("%.2f", pos['amount'])
        pos['tax_rate'] = locale.format("%.2f", pos['tax_rate'])
        pos['netto_price'] = locale.format("%.2f", pos['netto_price'])
        pos['total_netto_price'] = locale.format("%.2f", pos['total_netto_price'])
        pos['text'] = pos['text'].replace('\n', '<br>')

        pos_number += 1

    document_data['totals']['netto'] = locale.format("%.2f", document_data['totals']['netto'])
    document_data['totals']['brutto'] = locale.format("%.2f", document_data['totals']['brutto'])
    document_data['totals']['tax'] = locale.format("%.2f", document_data['totals']['tax'])

    with codecs.open(index_html, encoding="utf-8") as index_file:
        html_text = index_file.read()
        
        compiler = Compiler()
        template = compiler.compile(html_text)

        html_text = template(document_data)

        weasytemplate = HTML(string=html_text, base_url=base_url)
        weasytemplate.write_pdf(output_pdf)


if __name__ == "__main__":

    template = "invoice"
    output_pdf = "invoice.pdf"
    locale_lang = "de_DE.UTF-8"

    # yaml_file = "data.yml"
    # with open(yaml_file) as file:
    #     document_data = yaml.load(file, Loader=yaml.FullLoader)

    document_data = {
        "to": {
            "name": "Musterkunde",
            "street": "An der Ecke 1",
            "postcode": 12345,
            "city": "Berlin",
            "customer_number": 10004
        },
        "currency": "USD",
        "tax_rate": 0,
        "invoice": {
            "number": 1337,
            "date": "15.01.2021"
        },
        "positions": [
            {
            "netto_price": 1.29,
            "amount": 1.37,
            "text": "Speech Transcription\n<small>https://youtube.com/234fasd</small>\n"
            }
        ]
    }

    generate_invoice(document_data, output_pdf, locale_lang)