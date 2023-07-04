from django.shortcuts import render,redirect
from app.models import Student_Notification,Student,Student_Feedback,Student_leave,Subject,Attendance,Attendance_Report,StudentResult,Staff,Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()


    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,

    }
    return render(request,'Student/home.html',context)

@login_required(login_url='/')
def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id = student_id)

        context = {
            'notification':notification,
        }
        return render(request,'Student/notification.html',context)
    
@login_required(login_url='/')
def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()

    return redirect('student_notification')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        "feedback_history" : feedback_history,
    }
    return render(request,'Student/feedback.html',context)

@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin = request.user.id)
        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply = "",
        )
        feedbacks.save()

        return redirect('student_feedback')
    
@login_required(login_url='/')
def STUDENT_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    student_leave_history = Student_leave.objects.filter(student_id = student)
    context = {
        'student_leave_history':student_leave_history,
    }
    return render(request,'Student/apply_leave.html',context)

@login_required(login_url='/')
def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_id = Student.objects.get(admin = request.user.id)

        student_leave = Student_leave(
            student_id = student_id,
            data = leave_date,
            message = leave_message
        )
        student_leave.save()
        messages.success(request,'Successfully Applied For Leave !!')
        return redirect('student_leave')

@login_required(login_url='/')
def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id = subject_id)
            attendance_report = Attendance_Report.objects.filter(student_id = student,attendance_id__subject_id = subject_id)
   
    
    context = {
        'subjects':subjects,
        'action':action,
        'get_subject':get_subject,
        'attendance_report':attendance_report,
    }
    return render(request,'Student/view_attendance.html',context)

@login_required(login_url='/')
def VIEW_RESULT(request):

    student = Student.objects.get(admin = request.user.id)

    result = StudentResult.objects.filter(student_id = student)

    mark = None

    for i in result:
        assignment_mark = i.assignment_mark
        exam_marks = i.exam_marks

        mark = assignment_mark + exam_marks

    context = {
        'result':result,
        'mark':mark,
    }

    return render(request,'Student/view_result.html',context)