from db_connection import DBConnection as db


class AgentDB:
    def create_agent(self, data: dict):
        allowed_keys = ['name', 'specialty', 'agent_rank']
        keys = [k for k in data.keys() if k in allowed_keys]
        keys_str = ", ".join(keys)
        values = [v for v in data.values()]
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
                cursor.execute(f"SELECT * FROM agents WHERE id = {id}")
                agent = cursor.fetchone()
        return agent

    def update_agent(self, id, data):
        pass

    def deactivate_agent(self, id):
        pass

    def increment_completed(self, id):
        pass

    def increment_failed(self, id):
        pass

    def get_agent_performance(self, id):
        pass

    def count_active_agents(self):
        pass


data = {
    'name': "meir", 
    'specialty': 'python',
    'agent_rank': 'Junior'
}

a = AgentDB().create_agent(data)
print(a)