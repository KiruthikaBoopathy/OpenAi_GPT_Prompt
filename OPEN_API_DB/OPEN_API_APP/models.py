from django.db import models


class PDF_pathfiles(models.Model):
    pdf = models.FileField()





class PDF_fields(models.Model):

    name = models.CharField(max_length=1000)
    email_id = models.CharField(max_length=100)
    mob_no = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    skills = models.CharField(max_length=1000)
    education = models.CharField(max_length=100, blank=True, null=True)
    speaking_languages = models.CharField(max_length=100, blank=True, null=True)
    d_o_b = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)



#
