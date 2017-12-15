from django.shortcuts import render


def docs(request):
    """
    View function for documentation
    """
    return render(request, 'golf/documentation.html', {})

def docscodestyle(request):
    """
    View function for code style documentation
    """
    return render(request, 'golf/docscodestyle.html', {})

def docsinstall(request):
    """
    View function for software installation documentation
    """
    return render(request, 'golf/docsinstall.html', {})

def docseditting(request):
    """
    View function for source code editting documentation
    """
    return render(request, 'golf/docseditting.html', {})