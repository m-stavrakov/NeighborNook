from django.shortcuts import render

def home(request):

    # if request.user.is_authenticated:
    #     return render(request, 'home/home_loggedin.html', {
    #         'user': request.user,
    #     })
    # else:
    return render(request, 'home/home_not_loggedin.html', {
            'user': request.user,
        })

def home_loggedin(request):
    return render(request, 'home/home_loggedin.html', {
            'user': request.user,
        })