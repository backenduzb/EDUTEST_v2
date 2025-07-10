from django.db import models
from .utils import ANSWERS, CLASSES_CHOICE

class Subjects(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Darsning nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
  
class TestCase(models.Model):

    title = models.CharField(max_length=1024, verbose_name='Nomi')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name="Qaysi fan boyicha")
    created_at = models.DateTimeField(auto_now_add=True)
    tests_count = models.IntegerField(default=0)
    class_number = models.CharField(max_length=256, choices=CLASSES_CHOICE)
    
    tests = models.ManyToManyField('Tests', blank=True, related_name='test_cases', verbose_name="Savollar")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Test bolimi"
        verbose_name_plural = "Test bolimlari"

def latest_test_case():
    return TestCase.objects.latest('created_at')    

class Tests(models.Model):

    _case = models.ForeignKey(TestCase, on_delete=models.CASCADE, default=latest_test_case, related_name='test_set')

    question = models.TextField()

    correct_answer = models.CharField(max_length=2, choices=ANSWERS, default='A')

    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._case.tests.add(self)
    
    def __str__(self):
        return self.question[:50] 

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
