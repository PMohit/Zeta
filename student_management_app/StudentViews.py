import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.models import Courses, Students, Subjects, CustomUser, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent


def student_home(request):
    return render(request, "student_template/student_home_template.html")

def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance_template.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_date_parse=datetime.datetime.striptime(start_date,"%Y-%m-%d").date()
    end_date_parse=datetime.datetime.striptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_obj=CustomUser.objects.get(id=request.user.id)
    stu_obj=Students.objects.get(admin=user_obj)

    attendance=Attendance.objects.filter(attendance_date_range=(start_date_parse,end_date_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stu_obj)

    # for attendance_report in attendance_reports:
    #      print("Date:"+str(attendance_report.attendance_id.attendance_date),"Status :"+str(attendance_report.status))


    return render(request, "student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    student = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=student)
    return render(request, "student_template/student_apply_leave.html",{"leave_data":leave_data})


def student_apply_leave_save(request):
   if request.method !="POST":
       return HttpResponseRedirect(reverse("student_apply_leave"))
   else:
       leave_date = request.POST.get("leave_date")
       leave_msg = request.POST.get("leave_msg")

       student_obj = Students.objects.get(admin=request.user.id)
       try:
           leave_report = LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
           leave_report.save()

           messages.success(request, "Suceessufly Applied for leave")
           return HttpResponseRedirect(reverse("student_apply_leave"))
       except:
               messages.error(request, "Failed To Apply for leave")
               return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=staff_obj)
    return render(request, "student_template/student_feedback_leave.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()

            messages.success(request, "Suceessufly Sent Feedback for leave")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To  Sent Feedback for leave")
            return HttpResponseRedirect(reverse("student_feedback"))