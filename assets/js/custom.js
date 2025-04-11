document.getElementById('consultationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let age = document.getElementById('age').value;
    let gender = document.getElementById('gender').value;
    let query = document.getElementById('query').value;

    let response = `Thank you for your query. Based on the details provided: Age: ${age}, Gender: ${gender}, and Query: "${query}", our AI will generate a suitable response shortly.`;

    document.getElementById('outputText').innerText = response;
    document.getElementById('outputSection').classList.remove('d-none');
});