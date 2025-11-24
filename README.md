MCP_server/ 
.env                     # MySQL credentials and DB info \
mcp_sql_poc.py           # Main MCP server script (Todo Manager) \
pyproject.toml           # uv project metadata & dependencies \
mcp.json                 # MCP configuration for Claude \
README.md                # You're reading it!

### Requirements

| Requirement        | Version                      |
| ------------------ | ---------------------------- |
| Python             | 3.11 or higher               |
| MySQL Server       | Running locally on port 3306 |
| Claude (Anthropic) | For MCP integration          |

### Initially we need uv . uv is a project setup tool where we can create a overall project setup. It is also known as a project management tool.
pip install uv --user \

cd C:\Users\<YourUser>\PycharmProjects\MCP_server \
uv init \
uv python pin 3.13

## Database seyup

MYSQL_HOST=127.0.0.1 \
MYSQL_PORT=3306 \
MYSQL_USER=root \
MYSQL_PASS=YourPassword \
MYSQL_DB=mcp_todo \
uv run python mcp_sql_poc.py 

## Example tools
add_todo("Morning Jog", "2025-11-12 06:00:00", "2025-11-12 07:00:00") \
update_todo(1, "Evening Gym", "2025-11-12 18:00:00", "2025-11-12 19:00:00") 

## claude setup
User: Claude, show me my current todos. \
Claude → Calls `get_todos()` \

User: Update todo 3 to "Buy groceries tomorrow at 6 PM" \
Claude → Calls `update_todo(3, "Buy groceries", "2025-11-12 18:00:00", "2025-11-12 19:00:00")` \

User: Delete completed tasks. \
Claude → Calls `delete_todo(id)`


Images are also been attached in this repository. Please have a look for better understanding.
