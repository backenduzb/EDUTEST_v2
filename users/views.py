from .serializers import UserSerializer, RegisterSerializer, CustomAdminLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsStudentUser, IsTeacherUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import CustomUser


class ShowTeacherStudents(APIView):
    permission_classes =[IsTeacherUser]
    serializer_class = UserSerializer

    def get(self, request):
        students = CustomUser.objects.filter(info_token=request.user.students_token)
        serializer = UserSerializer(students, many=True)    
        print(request.user)
        return Response(serializer.data, status=200)


class EditStudentsView(APIView):
    permission_classes = [IsTeacherUser]
    
    def get(self, request, id):
        try:
            student = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"message":"Bunaqa o'quvchi yo'q."},status=404)
        seralizer = UserSerializer(student, many=False)
        return Response(seralizer.data, status=200)
    def delete(self, request, id):
        try:
            student = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"message":"Bunaqa o'quvchi yo'q."}, status=404)
        student.delete()

        return Response({"message":"O'quvchi ochirildi."}, status=200)
    def put(self, request, id):
        try:
            student = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"message":"Bunaqa o'quvchi yo'q."},status=404)
        serializer = UserSerializer(student, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomAdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data

        response = Response({"message":"Login succesful!"}, status=200)

        response.set_cookie(
            key='access_token',
            value=data['access'],
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=604800
        )

        response.set_cookie(
            key='refresh_token',
            value=data['refresh'],
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=604800
        )

        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = serializer.save()

        response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        return response
    
class LogoutView(APIView):

    def get(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"message": "Muvaffaqiyatli chiqildi"}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StudentCityRaitingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
                model = CustomUser.objects.filter(is_student=True, city=request.user.city).order_by("-student_raiting")  
        except CustomUser.DoesNotExist:
                return Response({"message":"Hozircha oquvchilar yo'q."}, status=404)

        serializer = UserSerializer(model, many=True)
        return Response(serializer.data, status=200)


class StudentRegionRaitingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
                model = CustomUser.objects.filter(is_student=True, region=request.user.region).order_by("-student_raiting")  
        except CustomUser.DoesNotExist:
                return Response({"message":"Hozircha oquvchilar yo'q."}, status=404)

        serializer = UserSerializer(model, many=True)
        return Response(serializer.data, status=200)
    

class StudentSchoolRaitingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
                model = CustomUser.objects.filter(is_student=True, school_name=request.user.school_name).order_by("-student_raiting")  
        except CustomUser.DoesNotExist:
                return Response({"message":"Hozircha oquvchilar yo'q."}, status=404)

        serializer = UserSerializer(model, many=True)
        return Response(serializer.data, status=200)

class StudentAllRaitingView(APIView):
     permission_classes = [AllowAny]

     def get(self, request):
        try:
            model = CustomUser.objects.filter(is_student=True).order_by("-student_raiting")
        except CustomUser.DoesNotExist:
            return Response({"message": "Hozircha o'quvchilar yo'q."}, status=404)

        serializer = UserSerializer(model, many=True)
        return Response(serializer.data, status=200)