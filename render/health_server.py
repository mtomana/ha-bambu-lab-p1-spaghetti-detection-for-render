import os
import subprocess
import threading
from flask import Flask, jsonify

app = Flask(__name__)

worker_process = None

@app.get("/")
def index():
    return "ok", 200

@app.get("/health")
def health():
    running = worker_process is not None and worker_process.poll() is None
    return jsonify({
        "status": "ok" if running else "starting_or_stopped",
        "worker_running": running
    }), 200

def run_worker():
    global worker_process

    image = os.environ.get("UPSTREAM_IMAGE", "nberk/ha_bambu_lab_p1_spaghetti_detection_standalone:latest")
    ml_api_token = os.environ.get("ML_API_TOKEN", "obico_api_secret")
    inner_port = os.environ.get("INNER_PORT", "3333")

    # Ta wersja zakłada, że właściwy proces masz odpalany z obrazu bazowego
    # Jeśli finalnie będziesz wszystko budował lokalnie z kodu, ten fragment zmienimy.
    worker_process = subprocess.Popen(
        [
            "sh",
            "-c",
            f"echo 'Health server is running. Configure actual worker start here.' && sleep infinity"
        ]
    )
    worker_process.wait()

if __name__ == "__main__":
    threading.Thread(target=run_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
