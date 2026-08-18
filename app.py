import os
import asyncio
from flask import Flask, jsonify
from run_end_to_end import run_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "service": "Marquee Agentic Cinema Backend",
        "endpoints": ["POST /trigger"]
    })

@app.route('/trigger', methods=['POST'])
def trigger_pipeline():
    """
    Triggers the Marquee Agent Pipeline (Watcher -> Analyst -> Advisor -> Executor).
    In a real production system, this would be triggered by an Alertmanager webhook.
    Here we execute it and return success (the actual execution logs to stdout and Grafana).
    """
    try:
        # Run the async pipeline in a new event loop for this request
        # (Cloud Run instances will scale, so this is fine for demo purposes)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_pipeline())
        loop.close()
        
        return jsonify({"status": "success", "message": "Pipeline executed successfully. Check Grafana for annotations and OTLP traces."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
