$(function () {
    ('use strict');

    //===== Prealoder

    $(window).on('load', function (event) {
        $('.preloader').delay(500).fadeOut(500);
    });

    function transcribe() {
        var randomBoolean = Math.random() < 0.5;
        return randomBoolean;
    }

    //===== YouTube Form
    $("#youtubeurl").bind('paste', function (e) {
        resetYoutubeFormState();
     
        $("#youtube_spinner").fadeIn();
        var successfullTranscribe = transcribe();
        setTimeout(function () {
            if (successfullTranscribe) {
                $("#youtube_spinner").fadeOut();
                $("#youtube_spinner_ok").fadeIn();
                $("#youtube_Submit").addClass("text-left");
                $("#youtube_price").fadeIn();
            }
            else {
                $("#youtube_spinner").fadeOut();
                $("#youtube_spinner_error").fadeIn();
            }
        }, 3000);
    });


    function resetYoutubeFormState(){
        $("#youtube_spinner_ok").hide();
        $("#youtube_spinner_error").hide();
        $("#youtube_Submit").removeClass("text-left");
        $("#youtube_price").hide();
    }


    //===== File Upload Form
    $("#fileurl").change(function (e) {
        resetFileUploadFormState();

        $("#fileupload_spinner").fadeIn();
        var successfullTranscribe = transcribe();
        setTimeout(function () {
            if (successfullTranscribe) {
                $("#fileupload_spinner").fadeOut();
                $("#fileupload_spinner_ok").fadeIn();
                $("#fileupload_Submit").addClass("text-left");
                $("#fileupload_price").fadeIn();
            }
            else {
                $("#fileupload_spinner").fadeOut();
                $("#fileupload_spinner_error").fadeIn();
            }
        }, 3000);
    });


    function resetFileUploadFormState() {
        $("#fileupload_spinner_ok").hide();
        $("#fileupload_spinner_error").hide();
        $("#fileupload_Submit").removeClass("text-left");
        $("#fileupload_price").hide();
    }

    //===== Accordion
    const items = document.querySelectorAll('.accordion button');

    function toggleAccordion() {
        const itemToggle = this.getAttribute('aria-expanded');

        for (i = 0; i < items.length; i++) {
            items[i].setAttribute('aria-expanded', 'false');
        }

        if (itemToggle == 'false') {
            this.setAttribute('aria-expanded', 'true');
        }
    }

    items.forEach(item => item.addEventListener('click', toggleAccordion));

    //===== File
    var inputs = document.querySelectorAll('.file-input');

    for (var i = 0, len = inputs.length; i < len; i++) {
        customInput(inputs[i]);
    }

    function customInput(el) {
        const fileInput = el.querySelector('[type="file"]');
        const label = el.querySelector('[data-js-label]');

        fileInput.onchange = fileInput.onmouseout = function () {
            if (!fileInput.value) return;

            var value = fileInput.value.replace(/^.*[\\\/]/, '');
            el.className += ' -chosen';
            label.innerText = value;
        };
    }

    //===== Match Height
    $('.matchHeight').matchHeight();
    
});
