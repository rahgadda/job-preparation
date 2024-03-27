from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chatwithum', methods=['POST'])
def generate_output():

    # Getting the input string from the request
    input_string = request.json.get('query')

    # Your processing logic here
    # For demonstration, let's just reverse the input string
    output_string = input_string[::-1]

    # Returning the output as JSON response
    return jsonify({'response': output_string})

if __name__ == '__main__':
    app.run(debug=True)