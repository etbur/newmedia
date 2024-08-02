from chat_app.models import Student
from chat_app.serializers import StudentSerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics

# Create your views here.
class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        student = serializer.save()
        student.created_by = self.request.user
        student.save()