from flask import Flask, render_template_string, request, redirect
from operatoros.api_fetcher import APIFetcher
from operatoros.logger import log_run

app = Flask(__name__)
fetcher = APIFetcher()

HTML = """
<!doctype html>
<title>OperatorOS Beta</title>
<h2>OperatorOS – Niche Selection</h2>

<form method="post">
  <label>Select a scored niche:</label><br>
  <select name="niche">
    {% for n in niches %}
      <option value="{{n['name']}}">
        {{n['name']}} (score: {{n['score']}})
      </option>
    {% endfor %}
  </select>
  <br><br>

  <label>Or enter a custom niche:</label><br>
  <input name="manual_niche" placeholder="Your own idea"><br><br>

  <button type="submit">Continue</button>
</form>

{% if selected %}
<hr>
<b>Selected Niche:</b> {{selected}}
{% endif %}
"""

selected_niche = None

@app.route("/", methods=["GET", "POST"])
def index():
    global selected_niche
    niches = fetcher.score_niches(fetcher.fetch_trends(), mock=False)

    if request.method == "POST":
        selected_niche = request.form.get("manual_niche") or request.form.get("niche")
        log_run(f"Niche chosen via GUI: {selected_niche}")
        return redirect("/")

    return render_template_string(HTML, niches=niches, selected=selected_niche)

if __name__ == "__main__":
    print("Launching OperatorOS GUI at http://127.0.0.1:5000")
    app.run(debug=False)
