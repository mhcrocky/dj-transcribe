Structure
=========

/transcribe-download

download and unpload script for assembly-ai (use your own free key)

/transcribe-template 

contains the template that should be used in the django application

/transcribe-parse

parse assembly-ai json to pdf and other files

/transcribe-invoice

pdf invoice generator that complies with german law


Pages
============

(1) Landing page
* URL field for youtube url
* Check video and get duration etc via pytube (get results via javascript/typescript and change stripe buy price based on duration)


(2) Checkout page
* Checkout via stripe (set custom field - youtube video url) on website
* Make sure customer provides an email address

(3) Success
* Send confirmation email
* Display success page + return to landing page link

(4) Script
* Python script that sets custom values in stripe api.


Inspiration
===========

* https://goya-template.webflow.io/
* https://comma.ai/
* https://soft-html-template.webflow.io/


Docker
======

```
docker build -t transcribe .
docker run -it --rm -v D:/Dmitry_Job/transcribe:/root -p 8000:8000 transcribe

python3 manage.py runserver 0.0.0.0:8000
python3 main.py
```