from fastapi import APIRouter, HTTPException
import logging

# from routes import service
from database.agent_db import AgentDB
from database.mission_db import MissionDB

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/summary")
def get_summary():
    logger.info("GET /reports/summary called")

    try:
        missions = MissionDB().get_all_missions()
        if not missions:
            logger.info("Mission empty")
            return {
                "active_agents_count": 0,
                "total_missions": 0,
                "open_missions": 0,
                "completed_missions": 0,
                "failed_missions": 0,
                "critical_missions": 0,
            }
        failed = sum(1 for m in missions if m["status"] == "FAILED")
        completed = sum(1 for m in missions if m["status"] == "COMPLETED")
        cancelled = sum(1 for m in missions if m["status"] == "CANCELLED")

        summary = {
            "active_agents_count": AgentDB().count_active_agents(),
            "total_missions": MissionDB().count_all_missions(),
            "open_missions": MissionDB().count_open_missions(),
            "completed_missions": completed,
            "failed_missions": failed,
            "cancelled_missions": cancelled,
        }
        logger.info("Summary ready returning to client")
        return summary
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/missions-by-status")
def missions_by_status():
    logger.info("GET /reports/summary/missions-by-status called")
    try:
        logger.info("Connecting to database")
        missions = MissionDB().get_all_missions()
        if not missions:
            logger.info("Mission empty")
            return {
            "open": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "critical": 0
            }

        open_m = MissionDB().count_open_missions()
        critical = MissionDB().count_critical_missions() 
        failed = sum(1 for m in missions if m["status"] == "FAILED")
        completed = sum(1 for m in missions if m["status"] == "COMPLETED")
        in_progress = sum(1 for m in missions if m["status"] == "IN_PROGRESS")
        report = {
            "open": open_m,
            "in_progress": in_progress,
            "completed": completed,
            "failed": failed,
            "critical": critical
            }
        logger.info("Summary ready returning to client")
        return report
        
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")
    

@router.get("/top-agent")
def top_agent():
    logger.info("GET /reports/summary/top-agent called")

    try:
        logger.info("Connecting to database")
        ret_val = MissionDB().get_top_agent()
        logger.info("Success")
        return ret_val
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")
