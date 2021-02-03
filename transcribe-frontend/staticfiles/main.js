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
