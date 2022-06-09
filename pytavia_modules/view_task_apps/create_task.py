import json
import sys
import traceback
from matplotlib.pyplot import title
import requests
from datetime import datetime

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from flask          import render_template
from flask          import request
from flask          import url_for
from flask          import redirect
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper
from pytavia_core   import bulk_db_multi

class create_task_view:

    mgdDB = database.get_db_conn(config.mainDB)
    

    def __init__(self, app):
        self.webapp = app
    # end def
        
    def html(self):
        if request.method == 'POST' :
            data = request.form
            mdl_create_todo = database.new(
            self.mgdDB, "db_todos"
            )
            
            mdl_create_todo.put("title", data["title"])
            mdl_create_todo.put("create_at", datetime.now()) #default now
            mdl_create_todo.put("complete", False) #default false
            mdl_create_todo.put("update_by", "admin") #no user currently so put admin as default
            
            db = database.get_database(config.mainDB)
            multi_create = bulk_db_multi.bulk_db_multi(
                {
                    "db_handle": db,
                    "app": self.webapp,
                }
            )
            
            multi_create.add_action(
                bulk_db_multi.ACTION_INSERT,
                mdl_create_todo
            )
            
            multi_create.execute({})
        
        return redirect('/')
    # end def
# end class

