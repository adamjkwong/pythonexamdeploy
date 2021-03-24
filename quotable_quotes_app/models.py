from django.db import models
from datetime import datetime
import re, bcrypt
# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2: 
            errors['first_name'] = "first name must be at least 2 characters long"
        if len(postData['last_name']) < 2: 
            errors['last_name'] = "last name must be at least 2 characters long"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        if not postData['password'] == postData['confirm_password']:
            errors['confirm_password'] = "These passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        emails = User.objects.filter(email=postData['email'])
        if len(emails) == 0:
            errors['unused_email'] = "Email is not tied to an account!"
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2: 
            errors['first_name'] = "first name must be at least 2 characters long"
        if len(postData['last_name']) < 2: 
            errors['last_name'] = "last name must be at least 2 characters long"
        if len(postData['old_password']) < 8:
            errors['old_password'] = "Old password should be at least 8 characters long"
        if len(postData['new_password']) < 8:
            errors['new_password'] = "New password should be at least 8 characters long"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quote']) < 11: 
            errors['quote'] = "Quote must be more than 10 characters long"
        if len(postData['quoted']) < 4: 
            errors['quoted'] = "Author must be more than 3 characters long"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    poster = models.ForeignKey(User, related_name="posted_quotes", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorite_quotes")
    quote = models.TextField()
    quoted = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()