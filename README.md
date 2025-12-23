# 🛡️ Sentinellus v2.0 - Autonomous Self-Healing Infrastructure

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tech Stack](https://img.shields.io/badge/stack-MERN%20%2B%20Docker-blue)


> **"Infrastructure that refuses to die."**

**Sentinellus** is a distributed system visualizer designed to demonstrate core DevOps principles: **Fault Tolerance**, **Load Balancing**, **Elastic Scaling**, and **Chaos Engineering**.

Built as a Final Year Project, it simulates a high-traffic cluster where nodes are randomly terminated by a "Chaos Monkey," only to be automatically detected and recovered by the orchestrator in real-time.
<img width="1470" height="837" alt="image" src="https://github.com/user-attachments/assets/54acb051-237b-49bf-a2d9-fafdfaa9dc75" />

---

## 🚀 Features (The "Wow" Factor)

### 🧠 Intelligent Orchestration
* **Auto-Healing Watchdog:** Detects `SIGKILL` signals (crashes) and restores nodes within 1.5 seconds.
* **Chaos Engine:** A background process that randomly kills nodes to test system resilience (inspired by Netflix Chaos Monkey).

### ⚡ Real-Time Visualization
* **Live Dashboard:** Visualizes Docker containers as interactive cards.
* **WebSocket Telemetry:** Streams CPU load, Memory usage, and Latency metrics in milliseconds—no page refreshes required.
* **Event Audit Log:** A scrolling terminal recording every crash, recovery, and scaling event.

### 📈 Elastic Infrastructure
* **Dynamic Scaling:** Provision new worker nodes on the fly with a single click.
* **Traffic Simulation:** Algorithmic load balancing that shifts traffic away from dead or overloaded nodes.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | **Python (FastAPI)** | The "Brain." Manages Docker Daemon & state. |
| **Frontend** | **React + Vite** | The "Face." Fast, interactive UI. |
| **Styling** | **Tailwind CSS** | Glassmorphism & Responsive Design. |
| **Infrastructure** | **Docker & Docker Compose** | Containerization & Networking. |
| **Database** | **Redis** | In-memory state & caching. |
| **Protocol** | **WebSockets** | Real-time full-duplex communication. |

---

## 📸 Screenshots
<img width="1467" height="836" alt="image" src="https://github.com/user-attachments/assets/5e140c81-d3b6-4771-bd63-219ec54cd56a" />
<img width="1469" height="836" alt="image" src="https://github.com/user-attachments/assets/6007fedc-949b-499b-b316-f00547c30556" />
<img width="1469" height="834" alt="image" src="https://github.com/user-attachments/assets/f9526e10-befd-4a84-bbcc-8ffe8f25249d" />



| **Dashboard** | **Analytics** |
|:---:|:---:|
| *Real-time Cluster Map* | *Latency & Health Graphs* |

---

## ⚡ Quick Start

You can run the entire system with **one command**. No manual setup required.

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Must be running)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/sentinellus.git](https://github.com/yourusername/sentinellus.git)
    cd sentinellus
    ```

2.  **Ignition:**
    ```bash
    docker compose up --build
    ```

3.  **Launch:**
    Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🕹️ How to Use (Demo Script)

1.  **The Chaos Test:**
    * Go to the **Dashboard**. Wait 10-20 seconds.
    * Watch the "Chaos Engine" randomly kill a node.
    * Observe the status turn **RED (CRITICAL)** and then automatically recover to **GREEN**.

2.  **The Stress Test:**
    * Go to **Analytics**.
    * Click **"START STRESS SIMULATION"**.
    * Watch the Latency graph spike and the Health Score drop as the system struggles.

3.  **The Scaling Test:**
    * Go to **Dashboard**.
    * Click **"Add Node +"**.
    * Watch a new container spin up instantly and take a portion of the traffic load.

---

## Contact Me 🙂

---

### 👤 Author

**Sumit Kumar**
* Full Stack Developer & System Architect
* [Connect on LinkedIn](https://www.linkedin.com/in/sumit-kumar2004/)
* [View Portfolio](https://sumitkr-2.github.io/Portfolio_website/)
