console.log("Sanity check!");
const fadeOutDelay = 400

function fetchVideoInfo(url) {
    // let video_link = document.getElementById("inputUrl").value;
    resetYoutubeFormState();
    checkValidation('youtube')

    fetch('/ytvideo-info/?' + new URLSearchParams({
        url: url,
    }))
    .then((result) => { return result.json(); })
    .then((data) => {
        console.log("response:", data);
        if (data.status === 'error') {
            // Hide video detail card
            $('#videoDetail').addClass("d-none")
            showFailState('youtube')
        } else {
            localStorage.setItem("videoinfo", JSON.stringify(data));
            document.getElementById("videoThumbnail").setAttribute("src", data.thumbnail_url);
            document.getElementById("videoTitle").textContent = data.title;
            document.getElementById("videoDescription").textContent = data.description;
            document.getElementById("videoAuthor").textContent = "Author: " + data.author;
            const pub_date = new Date(data.publish_date);
            document.getElementById("videoPublish").textContent = "Published: " + pub_date.toDateString();
            document.getElementById("videoLength").textContent = "Length: " + data.length.toString().toHHMM();
            const price = parseInt(data.length/60) > 50 ? parseInt(data.length/60)/100 : 50/100;
            document.getElementById("videoPrice").textContent = "Price: " + price + " USD";

            // Show video detail card
            $('#videoDetail').removeClass("d-none")

            const duration = formatTime(data.length)
            showSuccessState(duration, 'youtube')
        }
    })
}

// Get Stripe publishable key
fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);
        // Event handler
        document.querySelector("#buttonSearch").addEventListener("click", (event) => {
            event.preventDefault();
            let videoinfo = JSON.parse(localStorage.getItem("videoinfo"));
            // Get Checkout Session ID
            fetch('/create-checkout-session/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({title: videoinfo.title, length: videoinfo.length, url: videoinfo.url }),
            })
                .then((result) => { return result.json(); })
                .then((data) => {
                    console.log(data);
                    // Hide video detail card
                    let videoDetailElement = document.getElementById("videoDetail");
                    videoDetailElement.classList.add("d-none");
                    // Remove videoinfo from localStorage
                    localStorage.removeItem("videoinfo");
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                });

        });
    });

// convert duration seconds to hh:mm format
String.prototype.toHHMM = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0" + hours;}
    if (minutes < 10) {minutes = "0" + minutes;}
    if (seconds < 10) {seconds = "0" + seconds;}
    return hours + ':' + minutes;
}

//========= YouTube && File Upload Form =========//
const checkIsAudio = (fileType) => {
    switch (fileType) {
        case 'audio/mpeg':
        case 'audio/wav':
        case 'audio/ogg':
            return true;
    }

    return false;
}

const checkIsVideo = (fileType) => {
    switch (fileType) {
        case 'video/mp4':
        case 'video/ogg':
        case 'video/webm':
        case 'video/quicktime': // .mov
            return true;
    }

    return false;
}

const formatTime = (sec) => {
    const sec_num = parseInt(sec, 10); // don't forget the second param
    let hours   = Math.floor(sec_num / 3600);
    let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    let seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0" + hours;}
    if (minutes < 10) {minutes = "0" + minutes;}
    if (seconds < 10) {seconds = "0" + seconds;}

    return hours + ':' + minutes + ':' + seconds;
}


const checkValidation = (media_source) => {
    if (media_source === 'youtube') {
        $("#youtube_spinner").fadeIn();
        $("#youtubeSearch .youtube-search .button .caption").text('')
    } else {
        $("#fileUpload_spinner").fadeIn();
        $("#fileUpload .file-input .button .caption").text('')
    }
}

const showSuccessState = (duration, media_source='youtube') => {
    if (media_source === 'youtube') {
        $("#youtube_spinner").fadeOut(fadeOutDelay, function () {
            $("#youtube_spinner_ok").fadeIn();
            $("#youtube_Submit").addClass("text-left");
            $("#youtube_price").fadeIn();

            // $("#youtubeSearch .media-duration").text(duration)
            $("#youtubeSearch .button .caption").text(duration)
            $('#youtubeSearch .btn.main-btn').prop('disabled', false)
        });
    } else {
        $("#fileUpload_spinner").fadeOut(fadeOutDelay, function () {
            $("#fileUpload_spinner_ok").fadeIn();
            $("#fileUpload_Submit").addClass("text-left");
            $("#fileUpload_price").fadeIn();

            // $("#fileUpload .media-duration").text(duration)
            $("#fileUpload .file-input .button .caption").text(duration)
            $('#fileUpload .btn.main-btn').prop('disabled', false)
        });
    }
}

const showFailState = (media_source='youtube') => {
    if (media_source === 'youtube') {
         $("#youtube_spinner").fadeOut(fadeOutDelay, function () {
            $("#youtube_spinner_error").fadeIn();
            // $("#fileUpload .media-duration").text('')
            $('#youtubeSearch .btn.main-btn').prop('disabled', true)
        });
    } else {
        $("#fileUpload_spinner").fadeOut(fadeOutDelay, function () {
            $("#fileUpload_spinner_error").fadeIn();
            // $("#fileUpload .media-duration").text('')
            $('#fileUpload .btn.main-btn').prop('disabled', true)
        });
    }
}

const resetFileUploadFormState = () => {
    $("#fileUpload_spinner_ok").hide();
    $("#fileUpload_spinner_error").hide();
    $("#fileUpload_Submit").removeClass("text-left");
    $("#fileUpload_price").hide();

    // $("#fileUpload .media-duration").text('')
    $("#fileUpload .file-input .button .caption").text('Choose')
}

const resetYoutubeFormState = () => {
    $("#youtube_spinner_ok").hide();
    $("#youtube_spinner_error").hide();
    $("#youtube_Submit").removeClass("text-left");
    $("#youtube_price").hide();

    // $("#youtubeSearch .media-duration").text('')
    $("#youtubeSearch .youtube-search .button .caption").text('Search')
}
