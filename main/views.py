from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsStudentUser
from rest_framework.views import APIView
from django.shortcuts import render
from users.models import CustomUser
from rest_framework import status

from .serializers import (
    TestCaseSerializer,
    TestsSerializer
)
from .models import (
    Subjects,
    TestCase,
    Tests
)


class TestCasesView(APIView):
    permission_classes = [IsStudentUser]
    
    def get(self, request):
        class_number = request.user.class_number
        try:
            tests = TestCase.objects.filter(class_number=class_number).order_by('-created_at')
        except TestCase.DoesNotExist:
            return Response({"message":"Sizga mos savollar topilmadi."}, status=404)
        
        serializer = TestCaseSerializer(tests, many=True)

        return Response(serializer.data, status=200)

class TestsView(APIView):
    permission_classes = [IsStudentUser]
    
    def get(self, request, id):
        try:
            tests = Tests.objects.get(id=id)
        except TestCase.DoesNotExist:
            return Response({"message":"Sizga mos savollar topilmadi."}, status=404)
        
        serializer = TestsSerializer(tests)

        return Response(serializer.data, status=200)
    
    def post(self, request, id):
        try:
            tests = Tests.objects.get(id=id)
        except Tests.DoesNotExist:
            return Response({"message": "Sizga mos savollar topilmadi."}, status=404)

        user_answer = request.data.get('user_answer')
        if user_answer == tests.correct_answer:
            request.user.student_raiting += 1
            request.user.save()

            try:
                teacher = CustomUser.objects.get(students_token=request.user.info_token)

                students = CustomUser.objects.filter(info_token=teacher.students_token)

                total_rating = sum(student.student_raiting for student in students)
                student_count = students.count()

                average_rating = total_rating / student_count if student_count > 0 else 0

                teacher.class_raiting = average_rating  
                teacher.save()

                return Response({
                    "message": "To'g'ri topdingiz.",
                    "student_raiting": request.user.student_raiting,
                    "class_average_rating": average_rating
                }, status=200)

            except CustomUser.DoesNotExist:
                return Response({
                    "message": "Testga to‘g‘ri javob berdingiz. Lekin ustozingizni topa olmadik.",
                    "student_raiting": request.user.student_raiting
                }, status=404)

        return Response({"message": "Noto‘g‘ri javob berdingiz!"})
