from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher


@login_required
def profile(request):
    if not request.user.is_teacher_user():
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.warning(request, 'Teacher profile not found.')
        return redirect('accounts:dashboard')
    
    return render(request, 'teachers/profile.html', {'teacher': teacher})

