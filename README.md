# 🚀 Cloud-Native Asynchronous Lead Feedback Architecture

An event-driven microservices ecosystem engineered to handle high-throughput lead feedback ingestion and asynchronous background processing. The architecture is fully decoupled using **Python (Flask)**, **Redis** as a message broker, and orchestrated via **Kubernetes (K8s)** to ensure elasticity, resilience, and horizontal scaling.

---

## 🎯 Architecture Overview & Design Decisions

Traditional monolithic applications process incoming requests synchronously (`Client -> API -> Database`), which creates tight coupling and exposes the system to cascading failures or bottlenecks under heavy load. 

This project implements an **Event-Driven Architecture (EDA)** to isolate ingestion from processing, guaranteeing low latency and high availability.

### 🧠 Core Engineering Principles Applied

* **Asynchronous De-coupling:** The API layer validates the payload and instantly queues the message into Redis, returning an HTTP `202 Accepted` status back to the client in milliseconds. Heavy data mutations or third-party integrations are offloaded to background workers.
* **Fault Tolerance & Resiliency:** If the worker or a downstream dependency (such as a primary database) suffers an outage, data is not lost. Messages remain persisted inside the Redis queue until a healthy worker safely processes them.
* **Horizontal Scalability (Scale-Out):** Computational demands are isolated. If the ingestion rate spikes, the API deployment can be scaled independently. If processing backlogs grow, worker replicas can be expanded without disrupting the ingestion API.
* **The 12-Factor App Principles:** System configurations and service discovery routes are injected entirely via environment variables, abstracting infrastructure properties from the core codebase.

---

## 🛠️ Repository Structure

```directory
├── k8s/
│   ├── api-leads.yaml        # Deployment (2 replicas) & ClusterIP Service for Ingestion
│   ├── redis.yaml            # Ingestion broker instance & internal DNS routing Service
│   └── worker.yaml           # Consumer loop background daemon Deployment
├── app.py                    # Flask API exposing ingestion and health-check endpoints
├── worker.py                 # Active polling subscriber daemon using Redis BLPOP
└── Dockerfile                # Multi-stage optimized OCI container definition



    
