from flask import Flask, send_file, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('Object Visibility.html')

@app.route('/submit', methods=['POST'])
def handle_post():
    return render_template('results.html', results=request.form)

if __name__ == '__main__':
    app.run(debug=True)
    
