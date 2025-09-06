import frappe
import pandas as pd
from frappe.utils import getdate

def create_rooms():
    df = pd.read_excel(r'/home/hussein/frappe-bench/royal.xlsx')
    df = pd.DataFrame(df)
    data = df.to_dict(orient='records')
    
    formatted_data = []
    for item in data:
        formatted_item = {'Employee': item['Employee']}
        shifts = {key: value for key, value in item.items() if key not in ['Employee', 'Employee Name']}
        formatted_item['shifts'] = shifts
        formatted_data.append(formatted_item)

    try:
        for f_data in formatted_data:
            emp_id = f_data['Employee']
            emp_name = frappe.db.get_value("Employee", emp_id, "employee_name")
            for key, value in f_data['shifts'].items():
                if not isinstance(value, str):
                    continue
                value = value.strip().upper()
                shift = ""
                if value == "D":
                    shift = "Day Shift"
                elif value == "N":
                    shift = "Night Shift"
                elif value == "DN":
                    shift = "Day and Night Shift"
                elif value == "ND":
                    shift = "Night Day Shift"
                elif value == "CANTEEN":
                    shift = "CANTEEN"
                elif value in ["OFF", "OF"]:
                    shift = "Free"
                
                if not shift:
                    continue

                try:
                    day_int = int(key)
                    shift_date = f"2025-05-{day_int:02d}"
                except ValueError:
                    continue

                sched_doc = frappe.get_doc({
                    "doctype": "Employee Schedulling",  # Double check spelling!
                    "employee": emp_id,
                    "employee_name": emp_name,
                    "shift": shift,
                    "from_date": getdate(shift_date),
                    "to_date": getdate(shift_date),
                    "day": key,
                    "label": shift_date,
                    "month": "May",
                    "year": "2025"
                })
                sched_doc.insert()

        frappe.db.commit()
    except Exception as error:
        frappe.log_error(frappe.get_traceback(), "Create Rooms Error")
        print(error)
