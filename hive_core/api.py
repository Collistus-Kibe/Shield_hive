# File: hive_core/api.py
# Shield Hive - Sentinel API Interface (C2 Endpoints)

from datetime import datetime, UTC
from flask import Blueprint, request, jsonify
from .models import db, Agent, Job, Threat

api_bp = Blueprint('api', __name__)


# =============================================================================
# HEARTBEAT - Update Agent Status
# =============================================================================
@api_bp.route('/heartbeat', methods=['POST'])
def heartbeat():
    """
    POST /api/v1/heartbeat
    
    Expected JSON:
    {
        "agent_id": "SHIELD-XXXXXX",
        "ip_address": "192.168.1.100",
        "location": "Nairobi, Kenya",
        "logs": ["Event 1", "Event 2"]  // Optional
    }
    """
    data = request.get_json()
    
    if not data or not data.get('agent_id'):
        return jsonify({'success': False, 'error': 'agent_id is required'}), 400
    
    agent_id = data.get('agent_id')
    
    try:
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        
        if not agent:
            agent = Agent(
                agent_id=agent_id,
                ip_address=data.get('ip_address', request.remote_addr),
                location=data.get('location', 'Unknown'),
                status='Online'
            )
            db.session.add(agent)
        else:
            agent.ip_address = data.get('ip_address', agent.ip_address)
            agent.location = data.get('location', agent.location)
            agent.status = 'Online'
            agent.last_seen = datetime.now(UTC)
        
        # Process logs if provided (for Gemini analysis)
        logs = data.get('logs', [])
        if logs and isinstance(logs, list):
            for log_entry in logs[-5:]:  # Only process last 5
                agent.add_log(str(log_entry))
        
        db.session.commit()
        
        pending_jobs = Job.query.filter_by(agent_id=agent_id, status='Pending').count()
        
        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'pending_jobs': pending_jobs
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# COMMANDS - Send Pending Jobs to Sentinel
# =============================================================================
@api_bp.route('/commands/<agent_id>', methods=['GET'])
def get_commands(agent_id):
    """
    GET /api/v1/commands/<agent_id>
    
    Returns pending jobs for the agent, marks them as 'Sent'.
    """
    try:
        pending_jobs = Job.query.filter_by(
            agent_id=agent_id,
            status='Pending'
        ).order_by(Job.created_at.asc()).all()
        
        commands = []
        for job in pending_jobs:
            commands.append({
                'job_id': job.id,
                'command': job.command,
                'payload': job.payload
            })
            job.status = 'Sent'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'commands': commands
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# RESULTS - Receive Job Results from Sentinel
# =============================================================================
@api_bp.route('/results', methods=['POST'])
def post_results():
    """
    POST /api/v1/results
    
    Expected JSON:
    {
        "job_id": 123,
        "status": "Completed",
        "result": "Scan completed successfully"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('job_id'):
        return jsonify({'success': False, 'error': 'job_id is required'}), 400
    
    try:
        job = Job.query.get(data.get('job_id'))
        
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        job.status = data.get('status', 'Completed')
        job.result = data.get('result')
        job.completed_at = datetime.now(UTC)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'job_id': job.id,
            'message': 'Result recorded'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# THREAT REPORT - Record threat from Sentinel
# =============================================================================
@api_bp.route('/threat', methods=['POST'])
def report_threat():
    """
    POST /api/v1/threat
    
    Expected JSON:
    {
        "file_hash": "abc123...",
        "threat_name": "Trojan.Generic",
        "score": 85,
        "reasons": "Suspicious behavior detected"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('file_hash'):
        return jsonify({'success': False, 'error': 'file_hash is required'}), 400
    
    try:
        threat = Threat.query.filter_by(file_hash=data.get('file_hash')).first()
        
        if not threat:
            threat = Threat(
                file_hash=data.get('file_hash'),
                threat_name=data.get('threat_name', 'Unknown'),
                last_known_score=data.get('score', 0),
                last_known_reasons=data.get('reasons', '')
            )
            db.session.add(threat)
        else:
            threat.report_count += 1
            threat.last_known_score = data.get('score', threat.last_known_score)
            threat.last_known_reasons = data.get('reasons', threat.last_known_reasons)
            threat.last_seen = datetime.now(UTC)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'threat_id': threat.id,
            'report_count': threat.report_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# =============================================================================
# AI BRIEF - Dashboard AI Analysis Summary
# =============================================================================
@api_bp.route('/ai_brief', methods=['GET'])
def ai_brief():
    """
    GET /api/v1/ai_brief
    
    Returns AI-generated threat analysis for the dashboard.
    """
    try:
        # Get current stats
        total_agents = Agent.query.count()
        online_agents = Agent.query.filter_by(status='Online').count()
        total_threats = Threat.query.count()
        high_severity = Threat.query.filter(Threat.last_known_score >= 70).count()
        
        # Determine threat level
        if high_severity > 5:
            threat_level = "CRITICAL"
            recommendation = f"⚠️ {high_severity} high-severity threats detected. Immediate action required. Recommend isolation of affected systems."
        elif high_severity > 0:
            threat_level = "ELEVATED"
            recommendation = f"🔶 {high_severity} elevated threat(s) detected. Active monitoring in progress. Review threat intel feed."
        elif total_threats > 0:
            threat_level = "LOW"
            recommendation = f"✅ {total_threats} known signature(s) catalogued. No active threats detected. Systems nominal."
        else:
            threat_level = "NOMINAL"
            recommendation = f"🟢 All systems operational. {online_agents}/{total_agents} agents reporting. No threats detected."
        
        return jsonify({
            'status': 'active',
            'threat_level': threat_level,
            'recommendation': recommendation,
            'summary': f"{online_agents} agent(s) online. {total_threats} threat(s) tracked."
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'threat_level': 'UNKNOWN',
            'recommendation': 'Unable to analyze threat data.',
            'error': str(e)
        }), 500


# =============================================================================
# AGENTS LIST - Get All Agents (JSON)
# =============================================================================
@api_bp.route('/agents', methods=['GET'])
def get_agents():
    """
    GET /api/v1/agents
    
    Returns a list of all registered agents for dashboard/map updates.
    """
    try:
        agents = Agent.query.order_by(Agent.last_seen.desc()).all()
        
        return jsonify({
            'success': True,
            'count': len(agents),
            'agents': [agent.to_dict_masked() for agent in agents]  # Use masked IPs
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
