# Marquee - Agentic Cinema: The Blockbuster Hackathon

When a blockbuster title premieres globally across 190 countries, no one knows how to instantly translate "the bitrate dropped in São Paulo" to "you are losing 40,000 viewers in your second-largest market and you have eight minutes before it becomes a trending topic." 

Marquee does.

## Features
- **The Living Map:** The main screen is not just a metrics table. It's a world map where each region pulses with the real health of the premiere, powered by live data from the Grafana MCP.
- **Visible Deliberation:** Our sub-agents don't work in silence. Their reasoning appears on screen as it happens: one detects, another quantifies the damage, another proposes the plays.
- **Self-Observability:** We instrumented the agent itself using Grafana Cloud AI Observability, tracking its Gemini calls, token costs, latency, and MCP tool activity.

## Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install "google-cloud-aiplatform[agent_engines,adk]>=1.101.0" python-dotenv mcp-grafana
   ```
3. Set up your `.env` file with Grafana and Google Cloud credentials.

## Architecture
- **Data Source:** Custom OpenTelemetry generator simulating a global premiere.
- **Agents:** Google ADK + Gemini (via Agent Engine), orchestrated to deliberate and recommend business decisions based on Grafana MCP data.
- **Observability:** Grafana Cloud AI Observability SDK.
- **Backend:** Python + FastAPI.
- **Frontend:** Next.js + TypeScript + Tailwind.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
