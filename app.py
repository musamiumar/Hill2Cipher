from flask import Flask, render_template, request, jsonify
import string
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index.html template for the home page.
    """
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """
    Encrypts a sentence using the Hill cipher.

    Expects a POST request with the following form data:
    - 'a11', 'a12', 'a21', 'a22': Elements of the 2x2 matrix A
    - 'input-text': The sentence to encrypt

    Returns:
    - JSON object containing the encrypted ciphertext
    """
    alphabets = list(string.ascii_uppercase)
    numbers = list(range(1, 27))
    char_with_no = dict(zip(alphabets, numbers))

    # Extract matrix elements from form data
    a11 = int(request.form['a11'])
    a12 = int(request.form['a12'])
    a21 = int(request.form['a21'])
    a22 = int(request.form['a22'])
    A = np.array([[a11, a12], [a21, a22]])

    # Process input sentence
    sentence = request.form['input-text']
    uppercase_sentence = sentence.upper().strip()

    # Map characters to numbers
    result = []
    for i in range(len(uppercase_sentence)):
        if uppercase_sentence[i] in char_with_no:
            result.append(char_with_no[uppercase_sentence[i]])

    # Ensure result has an even length
    if len(result) % 2 != 0:
        result.append(result[-1])

    # Create pairs of numbers for encryption
    pairs = [(result[i], result[i + 1]) for i in range(0, len(result), 2)]
    column_matrices = [np.array(pair).reshape(-1, 1) for pair in pairs]

    # Encrypt the pairs using the Hill cipher
    number_for_encryption_list = [np.dot(A, column_matrix) % 26 for column_matrix in column_matrices]

    # Flatten the encrypted matrix
    flat_list = [element for matrix in number_for_encryption_list for row in matrix for element in row]

    # Convert numbers back to characters
    cipherlist = []
    for element in flat_list:
        for key, value in char_with_no.items():
            if value == element:
                cipherlist.append(key)

    # Join characters to form the ciphertext
    ciphertext = "".join(cipherlist)

    return jsonify({'ciphertext': ciphertext})

if __name__ == '__main__':
    app.run(debug=True)
