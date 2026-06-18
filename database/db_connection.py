import mysql.connector


class DBConnection:

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="1234",
                database="Intelligence_db",
            )
            return conn
        except Exception as e:
            print(f"Error with the connection {e}")
            return None

    def create_database(self):
        sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        conn = self.get_connection()
        if conn is None:
        # If I'll use get_connection() and there is no database it will return None
            conn = mysql.connector.connect(
                host="localhost", port=3306, user="root", password="1234"
            )
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.close()

    def create_table(self):
        agent_table = """
            CREATE TABLE IF NOT EXISTS agents(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialty VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM('Junior', 'Senior', 'Commander')
            )
        """
        missions_table = """
            CREATE TABLE IF NOT EXISTS missions(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                location VARCHAR(100) NOT NULL,
                difficulty INT CHECK (difficulty >= 0 and difficulty <= 10) NOT NULL,
                importance INT CHECK (importance >= 0 and importance <= 10) NOT NULL,
                status VARCHAR(100) NOT NULL DEFAULT 'NEW',
                risk_level VARCHAR(100) NOT NULL,
                assigned_agent_id INT DEFAULT NULL
            )
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(agent_table)
                cursor.execute(missions_table)
                conn.commit()


if __name__ == "__main__":
    DBConnection().create_database()
    DBConnection().create_table()
