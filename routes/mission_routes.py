from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from mysql.connector.errors import DatabaseError
import logging
from routes import service
from database.mission_db import MissionDB
from database.agent_db import AgentDB

logger = logging.getLogger(__name__)

db = MissionDB()
router = APIRouter()


class NewMission(BaseModel):
    title: str = Field(max_length=100)
    description: str
    location: str = Field(max_length=100)
    difficulty: int
    importance: int
    status: str | None = Field(max_length=100, default=None)


class UpdateMission(BaseModel):
    title: str | None = Field(max_length=100, default=None)
    description: str | None = None
    location: str | None = Field(max_length=100, default=None)
    difficulty: int | None = None
    importance: int | None = None
    status: str | None = Field(max_length=100, default=None)


@router.post("", status_code=201)
def create_new_mission(body: NewMission):
    logger.info("POST /missions called")
    data = body.model_dump(exclude_none=True)
    try:
        logger.info("Creating new mission in tha database")
        mission = db.create_mission(data)
        logger.info(f"Mission created successfully: id={mission['id']}")
        return mission
    except DatabaseError as e:
        if e.errno == 3819 :
            raise HTTPException(
                status_code=400,
                detail="Numbers in difficulty or importance are not between 1-10 ",
            )
        raise
    except Exception:
        logger.exception("Error with the database")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("")
def get_all_missions():
    logger.info("GET /missions called")
    try:
        logger.info("connecting to database")
        missions = db.get_all_missions()
        logger.info("Returning all missions")
        return missions
    
    except Exception:
        logger.exception("Error with the database")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/{id}")
def get_mission_by_id(id: int):
    logger.info(f"GET /missions/{id} called")
    try:
        logger.info("Checking if mission ID exists")
        exist = service.is_exist_mission(id)
        if not exist:
            raise HTTPException(status_code=404, detail=f"Mission {id} not found")
        logger.info("Getting mission from database")
        mission = db.get_mission_by_id(id)
        logger.info(f"Returning mission: {id}")
        return mission
    except HTTPException as e:
        logger.error(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int, agent_id: int):
    logger.info(f"PUT /missions/{id}/assign/{agent_id} called")
    try:
        logger.info("Starting validation process for assignment")
        is_valid = service.validate_mission_assignment(m_id=id, a_id=agent_id)
        if is_valid:
            logger.info("Assignment is valid")
            success = db.assign_mission(m_id=id, a_id=agent_id)
            if success:
                return {"status": "success"}
            raise HTTPException(status_code=500, detail="Server error")

    except HTTPException as e:
        logger.error(str(e))
        raise
    except KeyError as e:
        logger.exception("404 error")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.exception("Error assigning mission")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/{id}/start")
def start_mission(id: int):
    logger.info(f"PUT /missions/{id}/start called")
    try:
        logger.info("Checking if mission ID exists")
        if not service.is_exist_mission(id):
            raise HTTPException(status_code=404, detail=f"Mission {id} not found")
        success = db.update_mission_status(id, "IN_PROGRESS")
        if success:
            return {"status": "success"}
        raise HTTPException(status_code=500, detail="Server error")
    except HTTPException as e:
        logger.error(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info(f"PUT /missions/{id}/complete called")
    try:
        logger.info("Checking if mission ID exists")
        if not service.is_exist_mission(id):
            raise HTTPException(status_code=404, detail=f"Mission {id} not found")
        success = db.update_mission_status(id, "COMPLETED")
        agent_id = db.get_mission_by_id(id).get("assigned_agent_id")
        if success:
            logger.info("Found data returning to client")
            logger.info("Incrementing agent complete")
            AgentDB().increment_completed(agent_id)
            return {"status": "success"}
        raise HTTPException(status_code=400, detail="Mission already complete")
    except HTTPException as e:
        logger.error(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/{id}/fail")
def complete_failed_mission(id: int):
    logger.info(f"PUT /missions/{id}/fail called")
    try:
        logger.info("Checking if mission ID exists")
        if not service.is_exist_mission(id):
            raise HTTPException(status_code=404, detail=f"Mission {id} not found")
        success = db.update_mission_status(id, "FAILED")
        if success:
            logger.info("success")
            agent_id = db.get_mission_by_id(id).get("assigned_agent_id")
            logger.info("Incrementing agent Fails")
            AgentDB().increment_failed(agent_id)
            return {"status": "success"}
        raise HTTPException(status_code=400, detail="Mission already done")
    except HTTPException as e:
        logger.error(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    logger.info(f"PUT /missions/{id}/cancel called")
    try:
        logger.info("Checking if mission ID exists")
        if not service.is_exist_mission(id):
            raise HTTPException(status_code=404, detail=f"Mission {id} not found")
        success = db.update_mission_status(id, "CANCELLED")
        if success:
            logger.info("success")
            return {"status": "success"}
        raise HTTPException(status_code=500, detail="Server error")
    except HTTPException as e:
        logger.error(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")
