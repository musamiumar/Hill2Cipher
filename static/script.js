function encryptText() {
    // Retrieve matrix elements and input text from HTML elements
    let a11 = document.getElementById('a11').value;
    let a12 = document.getElementById('a12').value;
    let a21 = document.getElementById('a21').value;
    let a22 = document.getElementById('a22').value;
    let inputText = document.getElementById('input-text').value;

    // Send a POST request to the server for encryption
    fetch('/encrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `a11=${a11}&a12=${a12}&a21=${a21}&a22=${a22}&input-text=${inputText}`
    })
    .then(response => response.json())
    .then(data => {
        // Update the output-text HTML element with the encrypted text
        document.getElementById('output-text').value = data.ciphertext;
    })
    .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error('Error:', error);
    });
}
