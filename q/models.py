from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,related_name='question',on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question = models.ForeignKey(Question,related_name='answer',on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text
