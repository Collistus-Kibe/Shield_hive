![Uploading ChatGPT Image Feb 10, 2026, 11_34_58 AM.png…]()

# 🛡️ Shield AI: Titan Hive (C2)

> **⚠️ JUDGE EVALUATION NOTICE**
> This repository serves as the **architectural reference** for the Shield AI backend.
> To test the system, please download the **compiled "Judge Edition" application** from the [Releases] section or the provided demo package.

---

## 🦅 The Central "Brain"
**Titan Hive** is the sovereign Command & Control (C2) server for the Shield Defense Ecosystem. Unlike traditional centralized servers that simply log data, the Hive acts as a living, cognitive entity powered by **Google Gemini 3**.

It orchestrates a decentralized swarm of **Shield Sentinel** nodes, ingesting raw telemetry from thousands of endpoints and converting it into actionable, military-grade threat intelligence in real-time.

---

## 🚀 Core Capabilities

### 🧠 1. Cognitive Threat Analysis (Gemini 3)
The Hive integrates directly with Google's Gemini 3 Pro model to replace the human security analyst.
* **Zero-Shot Analysis:** Instantly evaluates unknown processes based on behavior, not just file signatures.
* **Intent Decoupling:** Distinguishes between benign tools (e.g., a game installer) and malicious actors (e.g., ransomware), even if they use similar system calls.
* **Natural Language Reporting:** Generates human-readable threat summaries for the dashboard.

### 👻 2. The Ghost Protocol (Privacy Architecture)
We believe security shouldn't cost you your privacy. The Hive enforces a "Trust No One" data policy:
* **Identity Masking:** All incoming Sentinel IP addresses are cryptographically hashed and masked *before* hitting the database.
* **Tor Integration:** Supports routing command traffic through the Tor network to prevent geolocation tracking of defense nodes.

### 🌍 3. Live Swarm Visualization
The dashboard provides a real-time "God's Eye View" of the global defense grid.
* **WebSocket Telemetry:** Low-latency (<50ms) updates of node health and active threats.
* **Geo-Fencing:** Visualizes attack vectors on a 3D globe without compromising user anonymity.

### 💎 4. DePIN Economy (Proof-of-Protection)
The Hive serves as the validator for the **$SHIELD** utility token ecosystem.
* **Uptime Verification:** Cryptographically validates "Proof-of-Protection" for connected Sentinels.
* **Trust Scoring:** Assigns dynamic reputation scores to nodes based on the accuracy of their threat reports, preventing network spam.

---

## 🏗️ System Architecture
The Titan Hive is built on a high-concurrency **Flask + Socket.IO** asynchronous backbone, designed to handle thousands of simultaneous Sentinel connections.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core Engine** | Python 3.12 (Flask) | REST API & Event Loops |
| **Real-Time Layer** | Flask-SocketIO | Bi-directional Sentinel Communication |
| **AI Logic** | Google Gemini 3 API | Threat Classification & Reasoning |
| **Database** | SQLite / SQLAlchemy | Encrypted Event Persistence |

---

## 🛡️ "Defense in Depth"
Shield AI represents a shift from passive antivirus software to active, coordinated cyber-defense. The Titan Hive is the intelligence that makes this shift possible.

*Submission for the Google Gemini 3 Hackathon.*
