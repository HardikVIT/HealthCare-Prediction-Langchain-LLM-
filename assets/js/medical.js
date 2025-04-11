document.getElementById("consultationForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    // Ensure you're selecting the correct form
    const form = document.getElementById("consultationForm"); 
    const formData = new FormData(form);

    // Print form data for debugging
    console.log("Form Data:");
    for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
    }

    // Send the form data to the server
    fetch("/general.html", {
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
        document.getElementById("outputText").innerText = "An error occurred while processing your request: " + error.message;
        document.getElementById("outputSection").classList.remove("d-none");
    });
});
