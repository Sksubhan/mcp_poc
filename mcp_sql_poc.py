from socket import create_connection

from anyio import current_time

from mysql.connector import connect
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
load_dotenv()
#from enum import verify

#import certifi
from sendgrid import SendGridAPIClient
#import ssl
import urllib3
os.environ["SSL_CERT_FILE"]=r"C:\Users\SubaniShaik\AppData\Local\.certifi\cacert.pem"
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()
#ssl_context=ssl.create_default_context(cafile=certifi.where())
#print(ssl_context)
urllib3.disable_warnings()
app=FastMCP("mytodo_agent")

def test_mysql_connection():
    """ return a healthy mysql conneciton connection"""
    try:
        conn = connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASS"),
            database=os.getenv("MYSQL_DB"),
            autocommit=True
        )
        conn.ping(reconnect=True,attempts=3,delay=2)
        return conn
    except Exception as e:
        return None

@app.resource("http://127.0.0.1/resources/todos")
def get_todos():
    """Return all the todo items"""
    conn=test_mysql_connection()
    if not conn:
        return {"error":"connection failed"}
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute("select * from todos order by date_time_from")
        todos=cursor.fetchall()
        return {"todos":todos}
    except Exception as e:
        return {"error":"Unable to get todo list"}
    finally:
        if cursor:
            cursor.close()
        conn.close()

@app.tool()
def get_particular_todos(id:int):
    """Return particular todo from the todos table
    Example:
    get_particular_todos(1)
    """
    conn=test_mysql_connection()
    if not conn:
        return {"error":"connection failed"}
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute("select * from todos where id=%s",(id,))
        todos=cursor.fetchall()
        return {"todos":todos}
    except Exception as e:
        return {"error":"Unable to get todo"}
    finally:
        if cursor:
            cursor.close()
        conn.close()

@app.tool()
def add_todo(todo_name:str,date_time_from: str,date_time_to:str):
    """
    Add a new to-do item
    date_time_from and date_time_to should be in "YYYY-MM-DD HH:MM:SS" format and beaware that if the similar todo is already there in the list let me know once before adding it to the db
    """
    conn=test_mysql_connection()
    if not conn:
        return {"error":"unable to connect to server"}
    try:
        cursor=conn.cursor()
        cursor.execute("Insert into todos (todo_name,date_time_from,date_time_to) values (%s,%s,%s);",(todo_name,date_time_from,date_time_to))
        conn.commit()
        return {"message":f"Added task {todo_name}"}
    except Exception as e:
        return {"error":"unable to add this todo into todo list"}
    finally:
        if cursor:
            cursor.close()
        conn.close()

@app.tool()
def update_todo(todo_name: str,date_time_from:str,date_time_to:str,id:int):
    """
    Update an existing to-do item.
    Example:
    update_todo(1, "Go to gym", "2025-11-11 07:00:00", "2025-11-11 08:00:00")
    """
    conn=test_mysql_connection()
    if not conn:
        return {"error":"unable to connect with the server"}
    try:
        cursor=conn.cursor()
        cursor.execute("update todos set todo_name=%s,date_time_from=%s,date_time_to=%s where id=%s",(todo_name,date_time_from,date_time_to,id))
        conn.commit()
    except Exception as e:
        return {"error":f"error while updating todo {e}"}
    finally:
        if cursor:
            cursor.close()
        conn.close()

@app.tool()
def delete_todo(id:int):
    """delete an existing todo item by its id
    Example:
        delete_todo(3)
    """
    conn=test_mysql_connection()
    try:
        if not conn:
            return {"error":"server connection failed"}
        cursor=conn.cursor()
        cursor.execute("delete from todos where id=%s",(id,))
        conn.commit()
    except Exception as e:
        return {"error":"Unable to delete todo form list"}
    finally:
        if cursor:
            cursor.close()
        conn.close()

def get_data_to_send_email():
    """get all the data from todos table and store it for sending it through the email"""
    conn = test_mysql_connection()
    try:
        if not conn:
            return {"error":"connection failed to server"}
        else:
            cursor=conn.cursor()
            cursor.execute("select * from todos")
            data=cursor.fetchall()
        # Convert data to an HTML table
        html_table = "<table border='1' cellspacing='0' cellpadding='5'><tr><th>ID</th><th>Todo name</th><th>datetime_from</th><th>datetime_to</th></tr>"
        for row in data:
            if len(data)>0:
                html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"

            else:
                html_table+=f"<tr><td>No todos chill your free time or come lets have some discussion I am always ready to help you...</td></tr>"
        html_table += "</table>"

        html_content = f"""
        <h3>All your todos</h3>
        <p>Here are the todos. This email is generated by claude mcp do not reply to this email it is old. come have a chat with me regarding any doubts lets deal face to face.</p>
        {html_table}
        """
        return html_content
    except Exception as e:
        return {"error":e}
    finally:
        if cursor:
            cursor.close()
        conn.close()


def email_setup(to_email):
    """Email setup with from to subject and html_content details"""
    setup_email=Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject="TODS of today",
        html_content=get_data_to_send_email()
    )
    return setup_email

@app.tool()
def send_email(email_id:str):
    """
    send email to respective mail given as input which contains there all todos
    :param email_id:
    :return: Email sent successfully

    Example:
    send_email(example@gmail.com)
    """
    try:
        sg=SendGridAPIClient(os.getenv("API_KEY"))
        sg.client.session.verify=os.environ["SSL_CERT_FILE"]
        response=sg.send(email_setup(email_id))

        if response.status_code == 202:
            return {"message":"Email sent successfully"}
        else:
            return {"error":f"{response.status_code} something went wrong"}
    except Exception as e:
        return e



if __name__=='__main__':
    app.run()