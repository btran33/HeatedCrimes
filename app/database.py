"""Defines all the functions related to the database"""
from datetime import date
from app import db
from sqlalchemy.sql import text

def fetch() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Official_Crimes Order By Date").fetchall()
    conn.close()
    todo_list = []
    query_results = query_results[-10:]
    query_results.sort(key=lambda x:x[4])
    for result in query_results:
        item = {
            "Location": result[5],
            "Crime_Type": result[1],
            "Description": result[2],
            "Date": result[4]
        }
        todo_list.append(item)
    return todo_list

def get_user_name(id_):
    conn = db.connect()
    user_name = conn.execute(f'Select User_Name From User Where User_ID = {id_};').fetchall()

    return user_name[0][0]

def get_user_id(user_name):
    conn = db.connect()
    user_id = conn.execute(f'Select User_ID From User Where User_Name = "{user_name}";').fetchall()

    return user_id

def get_user_reports(user_id, date_) -> dict:
    conn = db.connect()
    query_results = conn.execute(f'Select * From User_Reports WHERE Date = "{date_}";').fetchall()
    conn.close()
    reports = []
    for result in query_results:
        item = {
            "Crime_Type": result[1],
            "Description": result[2],
            "Date": result[5],
            "Location": result[6]
        }
        reports.append(item)
    print(reports)
    return reports

def predict_crime(request):
    conn = db.connect()
    pred = ""
    try:
        location = request["location"]
        temperature = request["temperature"]

        result = conn.execute(text(f'''
                                CALL GetPrediction("{location}", {temperature});
                               ''')).fetchall()
    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return False, pred, []

    return False, pred, result

def report_crime(request, id_, date_):
    try:
        conn = db.connect()
        crime_type = request["type"]
        description = request["description"]
        date = date_ if len(request["time"]) == 0 else request["time"]
        location = request["location"]

        if len(request["temperature"]) != 0:
            print("INSERT INTO User_Reports(Crime_Type, Description, Date, Location, Temperature) \n",
            f'VALUES("{crime_type}", "{description}", "{date}", "{location}", {request["temperature"]})')

            conn.execute(f'''INSERT INTO User_Reports(User_ID, Crime_Type, Description, Date, Location, Temperature) 
                            VALUES("{id_}","{crime_type}", "{description}", "{date}", "{location}", {request["temperature"]})
                        ''')
        else:
            print("INSERT INTO User_Reports (Crime_Type, Description, Date, Location) \n",
                    f'VALUES("{crime_type}", "{description}", "{date}", "{location}")')
            conn.execute(f'INSERT INTO User_Reports (User_ID, Crime_Type, Description, Date, Location) VALUES ("{id_}", "{crime_type}", "{description}","{date}","{location}")')

    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return False

    conn.close()
    return True

def get_search_result(request):
    conn = db.connect()
    try:
        where_clause = "WHERE "
        i = 0
        if len(request["time"]) != 0:
            i+=1
            where_clause+= f'Date = "{request["time"]}" '
        if len(request["type"]) != 0:
            if i > 0:
                where_clause += "and "
            where_clause+= f'Crime_Type = "{request["type"]}" '
        if len(request["location"]) != 0:
            if i > 0:
                where_clause += "and "
            where_clause+= f'Block  LIKE "%{request["location"]}%" '
        print(where_clause)
        result = conn.execute(text(f'''
                                SELECT Date, Block as Location, Crime_Type, Description
                                FROM Official_Crimes
                                {where_clause};
                               ''')).fetchall()
    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return False, []

    conn.close()
    return True, result


def adv_querry1(request):
    conn = db.connect()
    try:

        result = conn.execute(f'''
                                SELECT Crime_Type, COUNT(Crime_Type) as cnt
                                FROM Official_Crimes LEFT JOIN Weather USING(Date)
                                WHERE Avg_Temp>{request["min"]} and Avg_Temp<{request["max"]}
                                GROUP BY Crime_Type
                                ORDER BY COUNT(Crime_Type) DESC;
                               ''').fetchall()

    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return []

    conn.close()
    return result


def adv_querry2(request):
    conn = db.connect()
    try:
        result = conn.execute(f'''
                                SELECT Block
                                FROM Official_Crimes o
                                WHERE IsArrest+0 = 1 and Crime_Type = "THEFT"
                                GROUP BY Block
                                HAVING Count(Crime_ID) / (SELECT COUNT(*) FROM Official_Crimes p WHERE p.Block = o.Block AND Crime_Type = "THEFT") >= {int(request["percent"])/100};
                               ''').fetchall()

    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return []

    conn.close()
    return result

def update_username(request, id_):
    conn = db.connect()
    try:
        conn.execute(f'''
                        UPDATE User
                        SET User_Name = "{request["new_username"]}"
                        WHERE User_ID = {id_};
                        ''')

    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return False

    conn.close()
    return True

def delete_reports(request, id_):
    conn = db.connect()
    try:
        conn.execute(f'''
                        DELETE FROM User_Reports
                        WHERE User_ID = {id_};
                        ''')

    except Exception as e:
        print("Error is: ", e)
        conn.close()
        return False

    conn.close()
    return True