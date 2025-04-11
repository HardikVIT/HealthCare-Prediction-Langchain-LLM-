document.getElementById('mentalForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let age = document.getElementById('age').value;
    let gender = document.getElementById('gender').value;
    let stressLevel = document.getElementById('stressLevel').value;
    let sleepQuality = document.getElementById('sleepQuality').value;
    let mood = document.getElementById('mood').value;
    let concern = document.getElementById('concern').value;

    let response = `Thank you for sharing. Based on your details:
    - Age: ${age}
    - Gender: ${gender}
    - Stress Level: ${stressLevel}/10
    - Sleep Quality: ${sleepQuality}
    - Mood: ${mood}
    - Concern: "${concern}"

    Our AI will provide recommendations for your mental well-being soon.`;

    document.getElementById('outputText').innerText = response;
    document.getElementById('outputSection').classList.remove('d-none');
});