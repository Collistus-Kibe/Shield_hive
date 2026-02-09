# Shield Hive - Hackathon Submission
## 🛡️ AI-Powered Cybersecurity Command & Control Server

---

### Quick Start (For Judges)

1. **Run the Server:**
   - Double-click `ShieldHive_Server.exe`
   - Wait for the startup banner

2. **Open Dashboard:**
   - Navigate to: `http://localhost:5000`

3. **Connect Agents:**
   - Sentinel agents connect via `POST /api/v1/heartbeat`
   - View live agent status on the dashboard

---

### Security Notice
```
🔒 JUDGE EVALUATION BUILD
This demo server automatically shuts down after 60 minutes
to protect intellectual property.
```

---

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/heartbeat` | POST | Agent check-in |
| `/api/v1/agents` | GET | List all agents (masked IPs) |
| `/api/ai_brief` | GET | AI threat analysis |
| `/api/v1/commands/<id>` | GET | Get pending commands |
| `/api/v1/results` | POST | Submit job results |
| `/api/v1/threat` | POST | Report threat intel |

---

### Features
- ✅ Real-time agent monitoring
- ✅ AI-powered threat analysis (Gemini Commander)
- ✅ Interactive world map visualization
- ✅ Privacy-first design (masked IPs)
- ✅ Secure log ingestion

---

**Team Shield AI** | Hackathon 2026
