# File: hive_core/routes.py
# Shield Hive - Web Interface Routes

from flask import Blueprint, render_template
from .models import db, Agent, Threat, Job

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
@web_bp.route('/dashboard')
def dashboard():
    """
    Serve the main dashboard with live stats.
    """
    # Agent stats
    total_agents = Agent.query.count()
    online_agents = Agent.query.filter_by(status='Online').count()
    
    # Threat stats
    total_threats = Threat.query.count()
    validated_threats = Threat.query.filter_by(validated=True).count()
    
    # Job stats
    pending_jobs = Job.query.filter_by(status='Pending').count()
    completed_jobs = Job.query.filter_by(status='Completed').count()
    
    # Recent data
    agents = Agent.query.order_by(Agent.last_seen.desc()).all()
    recent_agents = agents[:10]  # First 10 for quick access
    recent_threats = Threat.query.order_by(Threat.last_seen.desc()).limit(10).all()
    
    return render_template(
        'dashboard.html',
        agents=agents,
        total_agents=total_agents,
        online_agents=online_agents,
        total_threats=total_threats,
        validated_threats=validated_threats,
        pending_jobs=pending_jobs,
        completed_jobs=completed_jobs,
        recent_agents=recent_agents,
        recent_threats=recent_threats
    )
