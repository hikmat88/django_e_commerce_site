from django.shortcuts import redirect

# check if user is logged in or not
def unauthentication_user(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authentication:
            return redirect('/')
        else:
            return view_function(request,*args,**kwargs)
        

# redirect user according to role if user is admin then redirect to admin dashboard otherwise redirect to normal user page
def admin_only(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_staff:
            return view_function(request,*args,**kwargs)
        else:
            return redirect('/')
    return wrapper_function