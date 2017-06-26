from django.shortcuts import render
from django.template import RequestContext


@app.route("/")
def index(request):
    return render(request, 'index.html')
