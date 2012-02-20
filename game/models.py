from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
	t_map = models.CharField(max_length=10000)
	p_map = models.CharField(max_length=10000)
	map = models.CharField(max_length=10000)
	activeplayer = models.IntegerField()
	turn = models.IntegerField()