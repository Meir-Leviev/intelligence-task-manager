# Intelligence Task Manager
A system for managing agents and mission using mysql database
<br>
---

## File Structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

```
<br>

---
## Tables

### `Agents Table`

| field | type | notes |
| :--- | :--- | :--- |
| `id` | INT, AUTO_INCREMENT, PK | agent spacial ID |
| `name` | VARCHAR(100) | agent name |
| `specialty` | VARCHAR(100) | agent specialty |
| `is_active` | BOOLEAN | DEFAULT TRUE |
| `completed_missions` | INT | DEFAULT 0 |
| `failed_missions` | INT | DEFAULT 0 |
| `agent_rank` | ENUM / VARCHAR | can only be: Junior / Senior / Commander

<br>

### `Missions Table`

| field | type | notes |
| :--- | :--- | :--- |
| `id` | INT, AUTO_INCREMENT, PK | mission spacial ID |
| `title` | VARCHAR(100) | mission title |
| `description` | TEXT | detailed description of the mission |
| `location` | VARCHAR(100) | location |
| `difficulty` | INT | only 1-10 |
| `importance` | INT | only 1-10 |
| `status` | VARCHAR(100) | DEFAULT 'NEW' |
| `risk_level` | VARCHAR(100) | automatically calculated - not coming from user |
| `assigned_agent_id` | INT | DEFAULT NULL until assigned |

---

<br>

- `risk_level` : 0-9 -> LOW | 10-17 -> MEDIUM | 18-24 -> HIGH | 

---

<br>

## Classes

### class `DBConnection`
| method | description |
| :--- | :--- |
| `get_connection()` | return a connection to the mysql database |
| `create_database()` | create the database if not exists |
| `create_tables()` | create the tables if not exists |

- `create_database()` and `create_tables()` will run at system startup

---

### class `AgentDB`
| method | description |
| :--- | :--- |
| `create_agent()` | create a new agent and return agent object |
| `get_all_agents(id)` | return a list of all agents |
| `get_agent_by_id()` | return one agent by his ID or None |
| `update_agent(id, data)` | UPDATE to the row (except id) |
| `deactivate_agent(id)` | set is_active = FALSE |
| `increment_completed(id)` | update the completed missions |
| `increment_failed(id)` | update the failed missions |
| `get_agent_performance(id)` | return a dict with `completed, failed, total, success_rate` |
| `count_active_agents()` | return the number of active agents |

---
### class `MissionDB`
| method | description |
| :--- | :--- |
| `create_mission(data)` | create new mission and return mission object |
| `get_all_missions()` | return all missions list |
| `get_mission_by_id(id)` | return one mission by its ID or None |
| `assign_mission(m_id, a_id)` | assigning mission to agent |
| `update_mission_status(id, status)` | for changing status |
| `get_open_missions_by_agent(id)` | return a list of missions `ASSIGNED/IN_PROGRESS` of an agent |
| `count_all_missions()` | sum of missions |
| `count_by_status(status)` | return a count by the given status |
| `count_open_missions()` | return count of open missions |
| `count_critical_missions()` | return count of critical missions |
| `get_top_agent()` | return the agent with most completed missions |


---

<br>

## Rules

1. `rank` must be ` Junior / Senior / Commander` else you'll get an error
2. `difficulty` and `importance` must be 1 - 10
3. `risk_level`  automatically calculated - not coming from user
4. Deactivated agent can not get a mission
5. One agent can not hold more than 3 open missions
6. If `risk_level=CRITICAL` only a  `Commander` rank agent can get the mission
7. Only a `status=NEW` mission can be assigned after that it becomes `status=ASSIGNED`
8. Only a `status=ASSIGNED` mission can be started after that it becomes ` status=IN_PROGRESS`
9.  Only a `status=IN_PROGRESS` mission can be ended after that change it to  failed or completed
10. Only a NEW or ASSIGNED mission can be canceled else you'll get an error

___

<br>

# How To Run

#### Run the docker
```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```
- Create a virtual environment
```
# windows

python -m venv .venv
./.venv/Scripts/activate
```
```
# macOS/linux

python3 -m venv .venv
source .venv/bin/activate

```
- install requirements
```
pip install -r requirements.txt
```
- Run `python main.py`  to activate the server
```
cd <where the project is>/intelligence-task-manager
python main.py
```

