$(function () {
    ('use strict');

    //===== Prealoder

    $(window).on('load', function (event) {
        $('.preloader').delay(500).fadeOut(500);
    });

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
