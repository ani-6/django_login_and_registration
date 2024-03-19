from .forms import *

def feedbackManager(self, request, comment, *args, **kwargs):
    try:
        form = form.save(commit=False)
        form.user = request.user
        form.email = request.user.email
        form.comment = comment
        form.save()
    except:
        Exception()