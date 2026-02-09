# 🛡️ Shield AI: Titan Hive (C2)

> **⚠️ SECURITY NOTICE: JUDGE EVALUATION BUILD**
> This repository contains the **Reference Source Code** for the Titan Hive Command & Control (C2) server.
> To protect the integrity of the active Shield Defense Grid, critical cryptographic keys, production API secrets, and the core "Ghost Protocol" routing engine have been **redacted or decoupled** in this public release.

---

## 🦅 Overview
**Titan Hive** is the central "Brain" of the Shield AI ecosystem. It acts as a sovereign, self-hosted Command & Control center that orchestrates a swarm of **Shield Sentinel** nodes.

Powered by **Google Gemini 3**, the Hive doesn't just log threats—it understands them. It ingests telemetry from thousands of endpoints, uses Generative AI to analyze attack patterns in real-time, and issues autonomous defense commands to the fleet.

## 🔒 Security & Privacy Architecture
We treat our infrastructure as a fortress. To prevent reverse-engineering of our active defense capabilities, this repository is structured as a **"Glass Box"** for evaluation:

* **Code Transparency:** Judges can review the architectural logic, Flask route structures, and Gemini 3 integration patterns.
* **Operational Security:** The live, weaponized defense modules (used for active countermeasures) are hosted on our private air-gapped internal repo.
* **Judge Edition Binary:** For a fully functional, easy-to-test experience, we have provided a compiled **"Judge Edition" executable** (with a strict 60-minute security session limit) in the releases section.

## 🚀 Key Features
* **🧠 Cognitive Threat Analysis:** Integrated with **Google Gemini 3** to provide zero-shot analysis of suspicious process behavior.
* **👻 Ghost Protocol Compliance:** Enforces privacy by default. All incoming Sentinel IP addresses are cryptographically masked before storage.
* **🌍 Live Threat Map:** Real-time WebSocket visualization of active nodes and intercepted attacks.
* **⚡ DePIN Ready:** Built-in logic for the **$SHIELD** utility token, tracking "Proof-of-Protection" uptime for future rewards.

## 🛠️ Installation & Testing
**Recommended for Judges:**
Please download the **Pre-Compiled Demo (Titan_Hive_Judge_Edition.exe)** from the release tab or the provided Google Drive link. This version comes pre-packaged with all dependencies and the "Judge Security Protocol" active.

**For Code Review:**
If you wish to inspect the codebase:
```bash
# Clone the repository
git clone [https://github.com/Collistus-Kibe/Shield_hive.git](https://github.com/Collistus-Kibe/Shield_hive.git)

# Install dependencies (Note: 'shield-neural-link' is a private internal lib)
pip install -r requirements.txt

# Run the reference server
python run_hive.py
