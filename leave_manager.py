from mcp.server.fastmcp import FastMCP
from typing import List

employee_leaves={
    "1123":{"balance":18,"history":["2024-12-15","2025-01-01"]},
    "1124":{"balance":20,"history":[]}
}

## creating a MCP server

mcp=FastMCP("LeaveManager2")

#Tool: check Leave Balance

@mcp.tool()
def get_leaves_balance(employee_id: str)-> str:
    """ check how many leave days are left fo the employee"""
    try:
        data=employee_leaves[employee_id]
        if data:
            return f"{employee_id} has {data["balance"]} leaves days remaining"
        return "Employee id not found please check the input again"
    except Exception as e:
        return "Cannot get balance leaves data. Contact Administrator"

@mcp.tool()
def apply_for_leave(employe_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates (e.g , ["2025-04-17", "2025-05-01"]"""
    try:
        if employe_id not in employee_leaves:
            return "Employee ID not found"

        request_days=len(leave_dates)
        available_balance=employee_leaves[employe_id]["balance"]

        if available_balance<request_days:
            return f"Insufficient leaves you only have {available_balance} number of leaves to apply."

        #Deduct balance and add to history
        employee_leaves[employe_id]["balance"] -= request_days
        employee_leaves[employe_id]["history"].extend(leave_dates)

        return f"leave applied for {request_days} day(s). Remaining balance : {employee_leaves[employe_id]["balance"]}"
    except Exception as e:
        return "Cannot apply for leaves. Contact Administrator"
@mcp.tool()
def get_leaves_details(employee_id: str) -> str:
    """Get the detailed list of all leaves dates of a particular id given"""
    try:
        if employee_id not in employee_leaves:
            return f"Given ID is incorrect please give again."
        list_of_dates=employee_leaves[employee_id]["history"]

        return f"List of date(s) {employee_id} is on leave are {list_of_dates}"
    except Exception as e:
        return "Unable to find the leaves history contact Administrator"





if __name__=='__main__':
    mcp.run()