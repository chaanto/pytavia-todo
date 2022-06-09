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
from bson import ObjectId
import operator

class update_task_view:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
        
    def html(self, todo_id):
        query = {"_id" : ObjectId(todo_id)}
        
        result = list(self.mgdDB.db_todos.find(query))
        complete = [x.get("complete") for x in result]
        
        set_query = {
            "$set" : {
                "complete" : operator.not_(complete[0]),
                "update_by": "admin",
            }
        }
        
        self.mgdDB.db_todos.update_one(query, set_query)
            
        return redirect('/')
    # end def
# end class

