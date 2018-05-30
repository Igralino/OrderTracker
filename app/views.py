from flask import redirect

from . import app


@app.route('/')
def index():
    return redirect('/business_client/')
