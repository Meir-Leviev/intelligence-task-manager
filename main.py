from fastapi import FastAPI
import uvicorn
from logs import logging_config
from database.db_connection import DBConnection
from routes import agent_routes, mission_routes, report_routes

logging_config.config_logging()

DBConnection().create_database()
DBConnection().create_table()

app = FastAPI()

app.include_router(router=agent_routes.router, prefix="/agents", tags=["Agents"])
app.include_router(router=mission_routes.router, prefix="/missions", tags=["Missions"])
app.include_router(router=report_routes.router, prefix="/reports", tags=["Reports"])



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
