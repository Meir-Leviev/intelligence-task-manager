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


    is_mission = is_exist_mission(m_id)
    if not is_mission:
        raise KeyError(f"mission {m_id} not found")
    is_agent = is_exist_agent(a_id)
    if not is_agent:
        raise KeyError(f"Agent {a_id} not found")

    mission = MissionDB().get_mission_by_id(m_id)
    if mission.get("status").upper() != "NEW":
        raise ValueError("Mission not available")

    agent = AgentDB().get_agent_by_id(a_id)
    if not agent.get("is_active"):
        raise ValueError("Agent is not active")
    if MissionDB().get_open_missions_by_agent(a_id) >= 3:
        raise ValueError("Agent has reached maximum missions")
    if mission.get("risk_level") == "CRITICAL":
        if agent.get("agent_rank").capitalize() != "Commander":
            raise ValueError("Only Commander can handle critical missions")
    return True