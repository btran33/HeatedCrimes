from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
from datetime import date

user_id = 0
usr_name = db_helper.get_user_name(user_id)

date_ = date.today()
user_reports = db_helper.get_user_reports(user_id,date_)

predictions = ("", "", "", "", "", "")
trend = 2
items = []
report = []


@app.route("/")
def homepage():
    return render_template("index.html", 
                            usr_name = usr_name, 
                            user_reports=user_reports,
                            prediction=predictions,
                            trend = trend,
                            date_=date_)

@app.route('/load')
def background_process():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)
    return render_template("index.html", 
                            usr_name= usr_name,
                            items=items,
                            prediction=predictions, 
                            user_reports=user_reports,
                            date_=date_)


@app.route('/report-search', methods = ['POST', 'GET'])
def report_search_function():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)

    if request.method == 'POST':
        if "Predict Crimes" in request.form:
            report_status, prediction = db_helper.predict_crime(request.form)
            trends = db_helper.get_trend(request.form)
            print(f'trend is: {trends}')
            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction = prediction,
                            trend = trends,
                            pred = prediction[4],
                            date_=date_,
                            reported=False,
                            report_status=report_status)

        elif "Report Crimes" in request.form:
            report_status = db_helper.report_crime(request.form,user_id, date_)
            user_reports = db_helper.get_user_reports(user_id,date_)
            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            reported=True,
                            report_status=report_status)
        elif 'Search Similar Crimes' in request.form:
            report_status, searched = db_helper.get_search_result(request.form)
            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            reported=False,
                            report_status=report_status,
                            searched=searched)
        
    elif request.method == 'GET':
        return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_)
    

@app.route('/adv_querry1', methods = ['POST', 'GET'])
def adv_querry1():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)

    if request.method == 'POST':
        if "See Results" in request.form:
            adv_querry1 = db_helper.adv_querry1(request.form)
            user_reports = db_helper.get_user_reports(user_id,date_)
            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            adv_querry1=adv_querry1)
        
    elif request.method == 'GET':
        return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_)

@app.route('/adv_querry2', methods = ['POST', 'GET'])
def adv_querry2():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)

    if request.method == 'POST':
        if "See Results" in request.form:
            adv_querry2 = db_helper.adv_querry2(request.form)
            user_reports = db_helper.get_user_reports(user_id,date_)
            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            adv_querry2=adv_querry2)
        
    elif request.method == 'GET':
        return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_)


@app.route('/usr_name', methods = ['POST', 'GET'])
def update_username():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)
    usr_name = db_helper.get_user_name(0) 

    if request.method == 'POST':
        if "Update Username" in request.form:
            status = db_helper.update_username(request.form, id_=user_id)
            user_reports = db_helper.get_user_reports(user_id, date_)
            usr_name = db_helper.get_user_name(user_id)

            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            updated = status,
                            display=True)
        
    elif request.method == 'GET':
        return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_)

@app.route('/deletion', methods = ['POST', 'GET'])
def delete_reports():
    items = db_helper.fetch()
    user_reports = db_helper.get_user_reports(user_id,date_)
    usr_name = db_helper.get_user_name(0) 

    if request.method == 'POST':
        if "Delete Reports" in request.form:
            status = db_helper.delete_reports(request.form, id_=user_id)
            user_reports = db_helper.get_user_reports(user_id, date_)
            usr_name = db_helper.get_user_name(user_id)

            return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_,
                            deleted = status,
                            display=True)
        
    elif request.method == 'GET':
        return render_template("index.html", 
                            usr_name= usr_name,
                            items=items, 
                            user_reports=user_reports,
                            prediction=predictions,
                            date_=date_)