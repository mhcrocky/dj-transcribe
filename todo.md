
TODO
====

1. Milestone (100 USD)
* upload file to s3 bucket (separate upload folder instead of direct bucket)
* create new stripe api key and set "pending" status in meta fields (write documentation)
* loader should keep rotating (css change)  

2. Milestone (100 USD)
* test assembly-ai (/transcribe-download) create a free key for a week or use my key for small files
* create transcription job via assembly-ai (/transcribe-download) and set Stripe invoice status to "polling" (crontab)

3. Milestone (100 USD)
* poll results from assembly-ai to send email with attachments (/transcribe-parse)
 if transcription is available and set Stripe invoice status to "finished" (crontab)

 