# 🌵 Project Aurora: Lone Star Soil Intelligence
### *An Automated GitOps ML Pipeline for Texas-Wide Geospatial Analytics*

Project Aurora is a distributed cloud-native system designed to monitor, predict, and visualize soil temperatures across the state of Texas. It leverages a modern "Triple Threat" data architecture (Redis, PostgreSQL, and Python) orchestrated via Kubernetes.

---

## 🏗️ Architecture Overview
The system is divided into four distinct layers:

1.  **The Ingress (Worker):** A Python microservice that polls the Open-Meteo Satellite API for 15+ major Texas hubs.
2.  **The Fast-Cache (Redis):** Stores real-time geospatial JSON data for instant UI rendering.
3.  **The Archive (PostgreSQL):** A persistent time-series database storing historical soil data for trend analysis.
4.  **The Intelligence UI (Streamlit & PyDeck):** A high-performance dashboard featuring:
    * **Interactive GIS Map:** Selectable sensors with hover-tooltips.
    * **The Oracle:** A Linear Regression engine predicting 1-hour temperature shifts.
    * **AI Briefing:** A generative reporting tool that summarizes state-wide conditions.

---

## 🛠️ Tech Stack
* **Orchestration:** Kubernetes (Kind/K3s)
* **CI/CD & GitOps:** ArgoCD & GitHub Actions
* **Databases:** Redis (Hot Data), PostgreSQL (Cold Data)
* **Languages:** Python (Pandas, NumPy, Psycopg2, Requests)
* **Visualization:** Streamlit, PyDeck (WebGL-powered maps)

---

## 🚀 How to Deploy
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/BryanPruneda/Project-Aurora-Automated-GitOps-ML-Pipeline.git
   ```
2. **Apply K8s Manifests:**
   ```bash
   kubectl apply -f charts/ml-app/templates/ -n production
   ```
3. **Access the Oracle:**
   ```bash
   kubectl port-forward svc/aurora-ui-service -n production 8501:80
   ```

---

## 🔮 Future Roadmap
* **LSTM Neural Networks:** Implementing deep learning for 7-day soil moisture forecasting.
* **Prometheus Monitoring:** Real-time cluster health and API latency tracking.
* **Edge Simulation:** Connecting physical Raspberry Pi sensors to the central K8s cluster.

---
**Author:** Bryan Pruneda  
**Status:** Operational 🚀
