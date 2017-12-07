from django.db import models

# Create your models here.
class Topic(models.Model):
    """Learning Topic"""
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
class Entry(models.Model):
    """Knowlages"""
    topic=models.ForeignKey(Topic,on_delete=models.DO_NOTHING)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='entries'
        
    def __str__(self):
        if len(self.text)>50:
            fulltext=self.text[:50]+"..."
        else:
            fulltext=self.text
        return fulltext
