# decorators.py

from django.shortcuts import redirect, render

def admin_logout_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (not (request.user.is_staff)):
            # This is a customer; allow access
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated and request.user.is_staff:
            # This is an admin or a user who is not a customer; redirect to admin logout
             next_url = request.get_full_path()
             context = {
                 'next_url':next_url,
             }
             return render(request, 'admin_logout_choice.html', context)  
        else:
            # The user is already logged out, proceed with the view
            return view_func(request, *args, **kwargs)
    return _wrapped_view




