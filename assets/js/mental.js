document.getElementById("mentalForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const form = document.getElementById("mentalForm");
    const formData = new FormData(form);

    // Debugging: Log form data
    console.log("Mental Form Data:");
    for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
    }

    // Send data to server
    fetch("/mental.html", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("outputText").innerText = data.response;
        document.getElementById("outputSection").classList.remove("d-none");
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("outputText").innerText = "An error occurred: " + error.message;
        document.getElementById("outputSection").classList.remove("d-none");
    });
});