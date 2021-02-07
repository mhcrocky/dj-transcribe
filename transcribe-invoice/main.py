import datetime
import time
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def cratepdf(companynamepdf, companyaddresspdf, amountpdf, staxpdf, emailpdf, timestamppdf, canvas2, datepdf, finalstaxpdf, productpdf):

    invoice_id = 1337

    canvas = canvas2.Canvas(f"/Users/philippbraun/Desktop/transcribe/transcribe-invoice/{invoice_id}.pdf", pagesize=letter)

    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)

    canvas.line(50, 747, 580, 747) #FROM TOP 1ST LINE
    canvas.drawString(280, 750, "INVOICE")
    canvas.drawString(60, 720, companynamepdf)
    canvas.drawString(60, 690, emailpdf)
    canvas.drawString(60, 660, companyaddresspdf)

    canvas.drawString(450, 720, str(datepdf))
    canvas.line(450, 710, 560, 710)
    canvas.line(50, 640, 580, 640)#FROM TOP 2ST LINE
    canvas.line(50, 748, 50, 50)#LEFT LINE
    canvas.line(400, 640, 400, 50)# MIDDLE LINE
    canvas.line(580, 748, 580, 50)# RIGHT LINE
    canvas.drawString(475, 615, 'TOTAL AMOUNT')
    canvas.drawString(100, 615, 'PRODUCT')
    canvas.line(50, 600, 580, 600)#FROM TOP 3rd LINE
    canvas.drawString(60, 550, productpdf)
    canvas.drawString(500, 550, amountpdf)
    TOTAL = int(amountpdf) * ((int(staxpdf)) / 100)
    canvas.drawString(60, 500, "SERVICE TAX (" +staxpdf+"%)")
    canvas.drawString(500, 500, str(TOTAL))
    canvas.line(50, 100, 580, 100)#FROM TOP 4th LINE
    canvas.drawString(60, 80, " TOTAL AMOUNT")
    canvas.drawString(500, 80, str(finalstaxpdf))
    canvas.line(50, 50, 580, 50)#FROM TOP LAST LINE


    canvas.setFont('Helvetica', 7)
    canvas.drawString(80, 200, "Es wird gemäß §19 Abs. 1 Umsatzsteuergesetz keine Umsatzsteuer erhoben.")
    canvas.drawString(80, 190, "Die aufgeführten Dienstleistungen haben Sie gemäß unserer AGB erhalten.")
    canvas.drawString(80, 180, "Wenn nicht anders angegeben entspricht das Leistungsdatum dem Rechnungsdatum.")


    canvas.save()

if __name__ == "__main__":
    companyname = "transcribe.lol"
    companyaddress = "COMPANY ADDRESS"
    amount = "10000"
    stax = "18"
    email = "hi@transcribe.lol"
    product = "Office Table"


    timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    date = time.strftime("%d/%m/%Y")
    finalstax = int(amount) + (int(amount) * ((int(stax))/100))
    cratepdf(companyname, companyaddress, amount, stax, email, timestamp, canvas, date, finalstax, product)