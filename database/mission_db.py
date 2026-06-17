from db_connection import DBConnection as db
from agent_db import AgentDB


class MissionDB:
    def calc_risk_level(self, difficulty: int, importance: int):
        """For 'risk_level' set in create_mission()
        Returns: int
        """
        risk_level = None
        total = difficulty + importance
        if 0 <= total <= 9:
            risk_level = "LOW"
        elif 10 <= total <= 17:
            risk_level = "MEDIUM"
        elif 18 <= total <= 24:
            risk_level = "HIGH"
        elif total >= 25:
            risk_level = "CRITICAL"
        return risk_level

    def create_mission(self, data: dict):
        allowed_keys = [
            "title",
            "description",
            "location",
            "difficulty",
            "importance",
            "status",
            "risk_level",
        ]
        risk_level = self.calc_risk_level(
            data.get("difficulty"), data.get("importance")
        )
        data["risk_level"] = risk_level
        keys = [k for k in data.keys() if k in allowed_keys]
        keys_str = ", ".join(keys)
        values = [data[k] for k in keys]
        place_holders = ", ".join(["%s" for _ in values])
        sql = f"INSERT INTO missions ({keys_str}) VALUES ({place_holders})"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                new_id = cursor.lastrowid
                conn.commit()
        new_mission = self.get_mission_by_id(new_id)
        return new_mission

    def get_all_missions(self):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM missions")
                missions = cursor.fetchall()
        return missions

    def get_mission_by_id(self, id):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
                mission = cursor.fetchone()
        return mission

    def validate_mission_assignment(self, m_id, a_id):
        """For assign_mission()
        Returns: bool
        """
        mission = self.get_mission_by_id(m_id)
        if mission.get("status") not in ["NEW", "ASSIGNED"]:
            raise ValueError("Mission not 'NEW' or 'ASSIGNED'")

        agent = AgentDB().get_agent_by_id(a_id)
        if not agent.get("is_active"):
            raise ValueError("Agent not active")
        if self.get_open_missions_by_agent(a_id) >= 3:
            raise ValueError("Agent have 3 open missions")
        if mission.get("risk_level") == "CRITICAL":
            if agent.get("agent_rank") != "Commander":
                raise ValueError("CRITICAL mission Commander only")
        return True

    def assign_mission(self, m_id, a_id):
        mission = self.get_mission_by_id(m_id)
        if mission is None:
            raise KeyError(f"Mission ID {m_id} not found")
        agent = AgentDB().get_agent_by_id(a_id)
        if agent is None:
            raise KeyError(f"Agent ID {a_id} not found")
        if self.validate_mission_assignment(m_id, a_id):
            sql = "UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s"
            with db().get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (a_id, m_id))
                    is_success = cursor.rowcount > 0
                    conn.commit()
            return is_success

    def update_mission_status(self, id, status):
        sql = "UPDATE missions SET status = %s WHERE id = %s"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (status, id))
                is_success = cursor.rowcount > 0
                conn.commit()
        return is_success

    def get_open_missions_by_agent(self, id):
        sql = """
            SELECT COUNT(*) FROM missions
            WHERE assigned_agent_id = %s AND (status = 'ASSIGNED' or status = 'IN_PROGRESS') 
        """
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
        return result["COUNT(*)"]

    def count_all_missions(self):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT COUNT(*) FROM missions")
                active_agents = cursor.fetchone()
        return active_agents["COUNT(*)"]

    def count_open_missions(self):
        sql = """
            SELECT COUNT(*) FROM missions
            WHERE status = 'ASSIGNED'
            or status = 'IN_PROGRESS' 
            or status = 'NEW'
        """
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                active_agents = cursor.fetchone()
        return active_agents["COUNT(*)"]

    def count_critical_missions(self):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = 'CRITICAL'")
                active_agents = cursor.fetchone()
        return active_agents["COUNT(*)"]

    def get_top_agent(self):
        agents = AgentDB().get_all_agents()
        top_agent = max(agents, key=lambda a: a["completed_missions"])
        return top_agent


if __name__ == "__main__":
    m = MissionDB()
    print(m.count_open_missions())



    # mock = {
    #     "title": "banana",
    #     "description": None,
    #     "location": "my shoe",
    #     "difficulty": 6,
    #     "importance": 5,
    # }
    # mission = m.create_mission(mock)
    # print(mission)
    # print()
    # all = m.get_all_missions()
    # print(all)
    # print()
    # print(m.get_mission_by_id(3))
    # print()
    # update = m.update_mission_status(3, "NEW")
    # assign = m.assign_mission(3,2)
    # print(f"{assign=}")
    # print()
    # open = m.get_open_missions_by_agent(2)
    # print(f"{open=}")
    # print()
    # count = m.count_all_missions()
    # print(f"{count=}")
    # print()
    # print("open cnt", m.count_open_missions())
    # print()
    # print(m.count_critical_missions())
    # print()
    # print("top", m.get_top_agent())
