from database.db_connection import DBConnection as db
from database.agent_db import AgentDB
from database.mission_db import MissionDB



def is_exist_agent(id):
    agent = AgentDB().get_agent_by_id(id)
    if agent is None:
        return False
    return True

def is_exist_mission(id):
    mission = MissionDB().get_mission_by_id(id)
    if mission is None:
        return False
    return True



def validate_mission_assignment(m_id, a_id):
    """For assign_mission()
    Returns: bool
    """
    if is_exist_mission(m_id) and is_exist_agent(a_id):
        mission = MissionDB().get_mission_by_id(m_id)
        if mission.get("status") == "NEW":
            raise ValueError("Mission not 'NEW'")

        agent = AgentDB().get_agent_by_id(a_id)
        if not agent.get("is_active"):
            raise ValueError("Agent not active")
        if MissionDB().get_open_missions_by_agent(a_id) >= 3:
            raise ValueError("Agent have 3 open missions")
        if mission.get("risk_level") == "CRITICAL":
            if agent.get("agent_rank") != "Commander":
                raise ValueError("CRITICAL mission Commander only")
        return True