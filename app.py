from flask import Flask, render_template, request
from routing_utils import init_client, get_route, create_map

app = Flask(__name__)
# Replace with your actual OpenRouteService API key
client = init_client('5b3ce3597851110001cf6248749418dba9354818bb14723910d29e6f')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        start_lat = float(request.form.get("start_lat"))
        start_lon = float(request.form.get("start_lon"))
        end_lat = float(request.form.get("end_lat"))
        end_lon = float(request.form.get("end_lon"))

        coords = [(start_lon, start_lat), (end_lon, end_lat)]
        route = get_route(client, coords)
        if route:
            # Calculate distance in km
            distance = route['features'][0]['properties']['summary']['distance'] / 1000
            map_file = create_map(route, coords)
            return render_template("index.html", map_display=True, map_file=map_file, distance=distance)
        else:
            return render_template("index.html", map_display=False, error="Failed to get route. Please try again.")
    return render_template("index.html", map_display=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
