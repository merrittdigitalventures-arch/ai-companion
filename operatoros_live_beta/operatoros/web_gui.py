from flask import Flask, render_template, Response
import os, time

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_task')
def start_task():
    def generate():
        steps = [
            "Step 1: Validating user credentials...\n",
            "Step 2: Fetching APIs...\n",
            "Step 3: Running content generation...\n",
            "Step 4: Performing recursive QC...\n",
            "Step 5: Preparing results for sales automation...\n",
        ]
        for step in steps:
            yield step
            time.sleep(1)  # simulate processing time
        yield "All tasks completed successfully!\n"
    return Response(generate(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
