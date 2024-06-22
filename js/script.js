
function predict() {
    const subStats = [
        document.getElementById('sub_stat1').value,
        document.getElementById('sub_stat2').value,
        document.getElementById('sub_stat3').value
    ];
    
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sub_stats: subStats })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred.';
    });
}
