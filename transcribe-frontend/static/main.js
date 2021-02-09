console.log("Sanity check!");

function fetchVideoInfo(url) {
  document.getElementById("buttonSearch").textContent = "Loading...";
  document.getElementById('buttonSearch').disabled = true;

  // let video_link = document.getElementById("inputUrl").value;
  fetch('/ytvideo-info/?' + new URLSearchParams({
    url: url,
  }))
  .then((result) => { return result.json(); })
  .then((data) => {
    console.log("response:", data);
    if (data.status === 'false') {
      document.getElementById("buttonSearch").textContent = "Error";
      document.getElementById('buttonSearch').disabled = true;
      // Hide video detail card
      let videoDetailElement = document.getElementById("videoDetail");
      videoDetailElement.classList.add("d-none");
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
      let videoDetailElement = document.getElementById("videoDetail");
      videoDetailElement.classList.remove("d-none");

      document.getElementById("buttonSearch").textContent = 'Transcribe Now';
      document.getElementById('buttonSearch').disabled = false;

    }
  })
  .then((res) => {
    if (res) {
      console.log(res);
      document.getElementById("buttonSearch").textContent = "Error";
      document.getElementById('buttonSearch').disabled = true;
      // Hide video detail card
      let videoDetailElement = document.getElementById("videoDetail");
      videoDetailElement.classList.add("d-none");
    }
  });
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


//========= YouTube Form =========//
    $("#youtubeLink").bind('paste', function (e) {
        resetYoutubeFormState();

        $("#youtube_spinner").fadeIn();

        // var successfullTranscribe = transcribe();
        // setTimeout(function () {
        //     if (successfullTranscribe) {
        //         $("#youtube_spinner").fadeOut();
        //         $("#youtube_spinner_ok").fadeIn();
        //         $("#youtube_Submit").addClass("text-left");
        //         $("#youtube_price").fadeIn();
        //     }
        //     else {
        //         $("#youtube_spinner").fadeOut();
        //         $("#youtube_spinner_error").fadeIn();
        //     }
        // }, 3000);

    });


    function resetYoutubeFormState(){
        $("#youtube_spinner_ok").hide();
        $("#youtube_spinner_error").hide();
        $("#youtube_Submit").removeClass("text-left");
        $("#youtube_price").hide();
    }
//========= File Upload Form =========//

//========= File Upload Form =========//
    $("#fileURL").change(function (e) {
        resetFileUploadFormState();

        $("#fileUpload_spinner").fadeIn();

        const target = e.currentTarget;
        const file = target.files[0];
        if (target.files && file) {
            const fileType = file.type
            console.log("Type: " + fileType);
            const isAudio = checkIsAudio(fileType)
            if (isAudio) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    audioContext.decodeAudioData(event.target.result, function(buffer) {
                        const duration = buffer.duration;
                        const formattedDuration = formatTime(duration)
                        console.log("The duration of the song is of: " + formattedDuration + " seconds");

                        showSuccessState(formattedDuration)
                    });
                };

                reader.onerror = function (event) {
                    console.error("An error occurred reading the file: ", event);
                    showFailState()
                };

                reader.readAsArrayBuffer(file);
            } else {
                showFailState()
            }
        } else {
            $("#fileUpload_spinner").fadeOut();
        }
    });

    const checkIsAudio = (fileType) => {
        switch (fileType) {
            case 'audio/mpeg':
            case 'audio/wav':
            case 'audio/ogg':
                return true;
        }

        return false;
    }

    const showSuccessState = (duration) => {
        $("#fileUpload_spinner").fadeOut();
        $("#fileUpload_spinner_ok").fadeIn();
        $("#fileUpload_Submit").addClass("text-left");
        $("#fileUpload_price").fadeIn();

        $("#fileUpload .media-duration").text(duration)
    }

    const showFailState = () => {
        $("#fileUpload_spinner").fadeOut();
        $("#fileUpload_spinner_error").fadeIn();
        $("#fileUpload .media-duration").text('')
    }

    function resetFileUploadFormState() {
        $("#fileUpload_spinner_ok").hide();
        $("#fileUpload_spinner_error").hide();
        $("#fileUpload_Submit").removeClass("text-left");
        $("#fileUpload_price").hide();

        $("#fileUpload .media-duration").text('')
    }

    const formatTime = (duration) => {
        const sec_num = parseInt(duration, 10); // don't forget the second param
        let hours   = Math.floor(sec_num / 3600);
        let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
        let seconds = sec_num - (hours * 3600) - (minutes * 60);

        if (hours   < 10) {hours   = "0" + hours;}
        if (minutes < 10) {minutes = "0" + minutes;}
        if (seconds < 10) {seconds = "0" + seconds;}

        return hours + ':' + minutes + ':' + seconds;
    }
//========= File Upload Form =========//
