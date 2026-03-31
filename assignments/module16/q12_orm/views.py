from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student

def item_list(request):
    students = Student.objects.all()
    return render(request, 'q12_orm/list.html', {'students': students})

def item_add(request):
    if request.method == 'POST':

        try:
            Student.objects.create(
                name=request.POST['name'],
                roll_no=request.POST['roll_no'],
                course=request.POST['course'],
                marks=request.POST.get('marks', 0),
                email=request.POST['email'],
            )
            messages.success(request, 'Student added successfully!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('q12_list')
    return render(request, 'q12_orm/form.html', {'action': 'Add', 'student': None})

def item_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':

        student.name = request.POST['name']
        student.roll_no = request.POST['roll_no']
        student.course = request.POST['course']
        student.marks = request.POST.get('marks', 0)
        student.email = request.POST['email']
        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('q12_list')
    return render(request, 'q12_orm/form.html', {'action': 'Edit', 'student': student})

def item_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':

        student.delete()
        messages.success(request, 'Student deleted!')
    return redirect('q12_list')