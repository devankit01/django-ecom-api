from .models import User
#This is the function for context process
def first_context_process(request):
    print("THis is our first_context_process")
    list_value = User.objects.all()
    return {'list_value':list_value}
