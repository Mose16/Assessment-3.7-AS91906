from bottle import run, route, view, get, post, request, static_file
from itertools import count


###Pages###
#Index page
@route('/')
@view('index')
def index():
    pass

run(host='0.0.0.0', port = 399, reloader = True, debug = True)