from rest_framework import serializers 
from .models import Subjects, TestCase, Tests

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['name']
    
class TestsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tests
        fields = ['id', 'question', 'correct_answer', 'answer_A', 'answer_B', 'answer_C', 'answer_D']


class TestCaseSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    tests = TestsSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = ['id', 'subject', 'title', 'created_at', 'tests_count', 'class_number', 'tests']
       
