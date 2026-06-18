from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Literal
from routes import service
from database.mission_db import AgentDB


logger = logging.getLogger(__name__)

class NewAgent(BaseModel):
    name: str = Field(max_length=100)
    specialty: str = Field(max_length=100)
    agent_rank: Literal["Junior", "Senior", "Commander"]


class UpdateAgent(BaseModel):
    name: str | None = Field(max_length=100, default=None)
    specialty: str | None = Field(max_length=100, default=None)
    agent_rank: None | Literal["Junior", "Senior", "Commander"] = None
    is_active: bool | None = None

db = AgentDB()
router = APIRouter()


@router.post("", status_code=201)
def add_new_agent(body: NewAgent):
    logger.info("POST /agents called")
    data = body.model_dump()
    try:
        logger.info("Creating new agent in tha database")
        agent = db.create_agent(data)
        logger.info(f"Agent created successfully: id={agent["id"]}")
        return agent
    except Exception:
        logger.exception("Error with the database")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("")
def get_all_agents():
    logger.info("GET /agents called")
    try:
       logger.info("Getting agents from database")
       agents = db.get_all_agents()
       logger.info("Returning agents list")
       return agents
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/{id}")
def get_agent_by_id(id: int):
    logger.info(f"GET /agents/{id} called")
    try:
        logger.info("Checking if agent ID exists")
        exist = service.is_exist_agent(id)
        if not exist:
            raise HTTPException(status_code=404 , detail=f"Agent {id} not found")
        logger.info("Getting agent from database")
        agent = db.get_agent_by_id(id)
        logger.info(f"Returning agent: {id}")
        return agent
    except HTTPException:
        logger.error("Agent not found")
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")



@router.put("/{id}")
def update_agent(id: int, body: UpdateAgent):
    logger.info(f"PUT /agents/{id} called")
    try:
        logger.info("Checking if agent ID exists")
        exist = service.is_exist_agent(id)
        if not exist:
            raise HTTPException(status_code=404 , detail=f"Agent {id} not found")
        data = body.model_dump(exclude_none=True)
        logger.info(f"Updating agent {id}")
        success = db.update_agent(id, data)
        if success:
            logger.info("Agent updated successfully")
            return {"status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Server error")
    except HTTPException as e:
        logger.exception(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    logger.info(f"PUT /agents/{id}/deactivate called")
    try:
        logger.info("Checking if agent ID exists")
        exist = service.is_exist_agent(id)
        if not exist:
            logger.error(f"Agent {id} not found")
            raise HTTPException(status_code=404 , detail=f"Agent {id} not found")
        success = db.deactivate_agent(id)
        if success:
            logger.info("Agent deactivate successfully")
            return {"status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Server error")
    except HTTPException as e:
        logger.exception(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    logger.info(f"PUT /agents/{id}/performance called")
    try:
        logger.info("Checking if agent ID exists")
        exist = service.is_exist_agent(id)
        if not exist:
            logger.error(f"Agent {id} not found")
            raise HTTPException(status_code=404 , detail=f"Agent {id} not found")
        performance = db.get_agent_performance(id)
        logger.info(f"Returning agent {id} performance")
        return performance
    
    except HTTPException as e:
        logger.exception(str(e))
        raise
    except Exception:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Server error")
