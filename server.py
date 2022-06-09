import json
import time
from urllib import response
from django.shortcuts import render
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/rest_api_controller") 

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model
from pytavia_stdlib  import idgen 

from rest_api_controller import module1 
from view_task_apps import view_task, create_task, delete_task, update_task


##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
csrf            = CSRFProtect(app)
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

########################## CALLBACK API ###################################

# @app.route("/v1/api/api-v1", methods=["GET"])
# def api_v1():
#     params = request.args.to_dict()
#     response = module1.module1(app).process( params )
#     return response.stringify_v1()
# # end def

# @app.route("/v1/api/api-post-v1", methods=["POST"])
# def api_post_v1():
#     params = request.form.to_dict()
#     response = module1.module1(app).process( params )
#     return response.stringify_v1()
# # end def



@app.route('/', methods=["GET"])
def task_view() :
    #params = request.args.to_dict() -> i believe this always give us empty dict, so better to comment
    html_page = view_task.task_view(app).html()
    return html_page

@app.route('/create', methods=["POST"])
def task_create() :
    """
        Here we try to pass the "app" to "create_task_view" class
        So in that class can initialize the "app" on def __init__
        What the function done was inserting new record into collection we define in models.py
        and instead following the gomgom file, i was trying to avoid to stuck on "url/create" after querying done.
        So instead of calling the view to get records in each class, i trying redirect to "url/" instead
        
        ^ this comment applied to others routing path 
        
    """
    html_page = create_task.create_task_view(app).html()
    return html_page

@app.route('/delete/<string:todo_id>')
def task_delete(todo_id) :
    html_page = delete_task.delete_task_view(app).html(todo_id)
    return html_page

@app.route('/update/<string:todo_id>')
def task_update(todo_id) :
    html_page = update_task.update_task_view(app).html(todo_id)
    return html_page
    
    


#################################################################################

### Sample generic endpoints
"""
# TODO: update example using new db actions
### sample generic archive -- archive book
@app.route("/process/book/archive", methods=["POST"])
def book_proc_archive():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).archive({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample generic restore -- restore book
@app.route("/process/book/restore", methods=["POST"])
def book_proc_restore():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).restore({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample two way reference -- reference book to author and author to book
@app.route("/process/book/add_author", methods=["POST"])
def book_proc_add_author():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).add_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample remove two way reference -- dereference book to author and vise versa
@app.route("/process/book/remove_group", methods=["POST"])
def book_proc_remove_group():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).remove_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()
"""