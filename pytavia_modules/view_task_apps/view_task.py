import json
import sys
import traceback
import requests

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper
from datetime import datetime

class task_view:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html(self):
        todo_data = self.mgdDB.db_todos.find().sort("created_at")
        todos = list(todo_data)
        
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            response = render_template(
                '/task_template/index.html', todo_list=todos
            )
        except :
            print(traceback.format_exc())
            response.put( "status"      ,  "VIEW_HTML_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        
        return response
    # end def
# end class

