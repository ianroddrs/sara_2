from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.base.decorators import secure_module_access

@secure_module_access
def home(request):
    return render(request, 'nexus.html')