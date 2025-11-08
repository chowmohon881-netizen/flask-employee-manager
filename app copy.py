from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/info')
def info():
    return {
        "name": "Mohon Chowdhury",
        "project": "Flask Beginner API",
        "status": "Running perfectly"
    }

@app.route('/api/hello', methods=['POST'])
def hello():
    data = request.get_json()
    name = data.get("name", "Anonymous")
    return {"message": f"Hello {name}, welcome to Flask!"}

if __name__ == "__main__":
    app.run(debug=True)
