from django.shortcuts import render, redirect

def faq(request):
    '''
    Renders faq.html when contact is clicked

    param request: Passes state through system
    returns: renders faq.html

    '''
    context = {}
    return render(request, 'base/faq.html',context)