from django.shortcuts import render, redirect

def contact(request):
    '''
    Renders contact.html when contact is clicked

    param request: Passes state through system
    returns: renders contact.html

    '''
    context = {}
    return render(request, 'base/contact.html',context)