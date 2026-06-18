from database.db_connection import DBConnection as db
import database.mission_db


class AgentDB:
    def create_agent(self, data: dict):
        allowed_keys = ["name", "specialty", "agent_rank"]
        keys = [k for k in data.keys() if k in allowed_keys]
        # data["agent_rank"] = data.get("agent_rank").capitalize()
        keys_str = ", ".join(keys)
        values = [data[k] for k in keys]
        place_holders = ", ".join(["%s" for _ in values])
        sql = f"INSERT INTO agents ({keys_str}) VALUES ({place_holders})"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                new_id = cursor.lastrowid
                conn.commit()
        new_agent = self.get_agent_by_id(new_id)
        return new_agent

    def get_all_agents(self):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM agents")
                agents = cursor.fetchall()
        return agents

    def get_agent_by_id(self, id):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT * FROM agents WHERE id = %s", (id,))
                agent = cursor.fetchone()
        return agent

    def update_agent(self, id, data):
        allowed_keys = [
            "name",
            "specialty",
            "agent_rank",
            "is_active",
            "completed_missions",
            "failed_missions"
        ]
        valid_keys = [k for k in data.keys() if k in allowed_keys]
        keys = [f"{k}=%s" for k in valid_keys]
        keys_str = ", ".join(keys)
        values = [data[k] for k in valid_keys] + [id]
        sql = f"UPDATE agents SET {keys_str} WHERE id = %s"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                is_success = cursor.rowcount > 0
                conn.commit()
        return is_success

    def deactivate_agent(self, id):
        sql = f"UPDATE agents SET is_active = FALSE WHERE id = %s"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id,))
                is_success = cursor.rowcount > 0
                conn.commit()
        return is_success

    def increment_completed(self, id):
        sql = f"UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id,))
                is_success = cursor.rowcount > 0
                conn.commit()
        return is_success

    def increment_failed(self, id):
        sql = f"UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"
        with db().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id,))
                is_success = cursor.rowcount > 0
                conn.commit()
        return is_success

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        total_missions = database.mission_db.MissionDB().get_open_missions_by_agent(id)
        completed_missions = agent.get("completed_missions")
        failed_missions = agent.get("failed_missions")
        total_completed = completed_missions + failed_missions
        success_rate = 0
        if total_completed > 0:
            success_rate = (completed_missions / total_completed) * 100
        result = {
            "total": total_missions,
            "completed_missions": completed_missions,
            "failed_missions": failed_missions,
            "success_rate": success_rate
        }
        return result

    def count_active_agents(self):
        with db().get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = TRUE")
                active_agents = cursor.fetchone()
        return active_agents["COUNT(*)"]



# if __name__ == "__main__":

#     # data = {"name": "Moshe", "specialty": "python", "agent_rank": "Senior", }

#     # a = AgentDB().count_active_agents()
#     # print(a)
