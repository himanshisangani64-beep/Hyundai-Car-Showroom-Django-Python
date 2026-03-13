from django.db import models

class Register(models.Model):
    cid = models.CharField(max_length=100, unique=True)
    cname = models.CharField(max_length=100)
    cpassword = models.CharField(max_length=100)
    cemail = models.EmailField()
    cmob = models.CharField(max_length=15)
    ccity = models.CharField(max_length=100)
    ccon = models.CharField(max_length=100)
    cstate = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.cname
    

class Review(models.Model):
    rid = models.CharField(max_length=100, unique=True)
    rname = models.CharField(max_length=100)
    remail = models.EmailField()
    rmob = models.CharField(max_length=15)
    rmes=models.TextField(max_length=255)

    def __str__(self):
     return f"Review #{self.id}"


