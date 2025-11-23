
// Toggle Theme

function toggleTheme() {
    let body = document.body;

    if (body.style.backgroundColor === "white" || body.style.backgroundColor === "") {
        body.style.backgroundColor = "black";
        body.style.color = "white";
    } else {
        body.style.backgroundColor = "white";
        body.style.color = "black";
    }
}


// Click Counter
let clicks = 0;

function countClicks() {
    clicks++;
    document.getElementById("clickCount").innerText = "Clicks: " + clicks;
}


// Form Validation
let form = document.querySelector("form");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    let name = document.querySelector('input[type="text"]').value;
    let email = document.querySelector('input[type="email"]').value;

    if (name === "" || email === "") {
        alert("Please fill in all fields");
    } else {
        alert("Message sent successfully");
        form.reset();
    }
});


//Show today’s date automatically

let today = new Date().toDateString();
let dateBanner = document.createElement("p");
dateBanner.textContent = "Today is: " + today;
dateBanner.style.fontWeight = "bold";
dateBanner.style.marginBottom = "10px";
document.body.prepend(dateBanner);


// EXTRA EFFECT 2: Animate title on page load

window.onload = function() {
    let title = document.querySelector("h1");
    title.style.transition = "0.8s";
    title.style.transform = "scale(1.2)";
    setTimeout(() => {
        title.style.transform = "scale(1)";
    }, 800);
};



// Highlight cards on mouse hover

let cards = document.querySelectorAll(".card");

cards.forEach(card => {
    card.addEventListener("mouseenter", function() {
        card.style.transform = "scale(1.02)";
        card.style.transition = "0.2s";
        card.style.boxShadow = "0 0 12px rgba(0,0,0,0.2)";
    });

    card.addEventListener("mouseleave", function() {
        card.style.transform = "scale(1)";
        card.style.boxShadow = "0 6px 18px rgba(0,0,0,0.06)";
    });
});



// Count remaining characters in message

let textarea = document.querySelector("textarea");

if (textarea) {
    let counter = document.createElement("small");
    counter.textContent = "Characters left: 500";
    textarea.parentNode.appendChild(counter);

    textarea.addEventListener("input", function() {
        let remaining = 500 - textarea.value.length;
        counter.textContent = "Characters left: " + remaining;
    });
}



// Change nav link color when clicked

let navLinks = document.querySelectorAll("nav ul li a");

navLinks.forEach(link => {
    link.addEventListener("click", function() {
        navLinks.forEach(l => l.style.color = "white");
        link.style.color = "yellow";
    });
});
