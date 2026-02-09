# File: hive_core/models.py
# SQLAlchemy Models - Aligned with existing titan_hive_v2.db schema

import json
from datetime import datetime, UTC
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Agent(db.Model):
    """
    Represents a connected Sentinel/Shield AI client.
    Schema matches existing database exactly.
    """
    __tablename__ = 'agent'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), unique=True)
    ip_address = db.Column(db.String(50))
    location = db.Column(db.String(100), default="Unknown")
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    status = db.Column(db.String(20), default="Online")
    
    # Intelligence fields for Gemini analysis
    threat_score = db.Column(db.Integer, default=0)
    recent_logs = db.Column(db.Text, default="[]")  # JSON string of last 5 events

    def __repr__(self):
        return f'<Agent {self.agent_id} [{self.status}]>'
    
    def mask_ip(self, ip_address):
        """Mask last 2 octets for privacy: 192.168.1.100 -> 192.168.***.***"""
        if not ip_address:
            return 'N/A'
        parts = ip_address.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.***.***"
        return ip_address  # Return as-is if not IPv4
    
    def get_logs(self):
        """Parse recent_logs JSON string to list."""
        try:
            return json.loads(self.recent_logs or '[]')
        except:
            return []
    
    def add_log(self, log_entry):
        """Add a log entry, keeping only the last 5."""
        logs = self.get_logs()
        logs.insert(0, {'timestamp': datetime.now(UTC).isoformat(), 'message': log_entry})
        self.recent_logs = json.dumps(logs[:5])  # Keep last 5
    
    def to_dict(self):
        """Full dict with real IP (for internal use)."""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'ip_address': self.ip_address,
            'location': self.location,
            'status': self.status,
            'threat_score': self.threat_score,
            'recent_logs': self.get_logs(),
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }
    
    def to_dict_masked(self):
        """Dict with masked IP (for public API/dashboard)."""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'ip_address': self.mask_ip(self.ip_address),
            'location': self.location,
            'status': self.status,
            'threat_score': self.threat_score,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class Threat(db.Model):
    """
    Threat intelligence records from agents.
    Restored from original hive_models.py schema.
    """
    __tablename__ = 'threat'
    
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(128), unique=True, nullable=False)
    threat_name = db.Column(db.String(128), nullable=False)
    report_count = db.Column(db.Integer, default=1)
    validated = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    # Analysis fields
    last_known_score = db.Column(db.Integer, default=0)
    last_known_reasons = db.Column(db.String(1024), default="")
    ai_analysis = db.Column(db.Text, default="Pending Analysis")

    def __repr__(self):
        return f'<Threat {self.threat_name} [Score: {self.last_known_score}]>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_hash': self.file_hash,
            'threat_name': self.threat_name,
            'report_count': self.report_count,
            'validated': self.validated,
            'last_known_score': self.last_known_score,
            'last_known_reasons': self.last_known_reasons,
            'ai_analysis': self.ai_analysis,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class Job(db.Model):
    """
    Commands/tasks queued for agents to execute.
    """
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), nullable=False, index=True)
    
    command = db.Column(db.String(128), nullable=False)
    payload = db.Column(db.Text)
    
    status = db.Column(db.String(24), default="Pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    completed_at = db.Column(db.DateTime)
    
    result = db.Column(db.Text)

    def __repr__(self):
        return f'<Job {self.id} [{self.status}] {self.command}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'command': self.command,
            'payload': self.payload,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result
        }
