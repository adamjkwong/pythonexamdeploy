from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote
import bcrypt
User_count = User

def index(request):
    return render(request, "index.html")

def delete_quote(request, q_id):
    delete_quote = Quote.objects.get(id=q_id)
    delete_quote.delete()
    return redirect("/quotes")

def favorite(request, q_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=q_id)
    user.favorite_quotes.add(quote)
    return redirect('/quotes')

def unfavorite(request, q_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=q_id)
    user.favorite_quotes.remove(quote)
    return redirect('/quotes')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            # see if the username provided exists in the database
            user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
            if user: # note that we take advantage of truthiness here: an empty list will return false
                logged_user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                    request.session['user_id'] = logged_user.id
                # never render on a post, always redirect!
                    messages.success(request, "Successful login")
                    return redirect('/quotes')
                messages.error(request,"Incorrect login credentials")
            else:
                messages.error(request, "Could not find email address")
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def post_quote(request):
    if not 'user_id' in request.session:
            return redirect("/")
    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0: 
            for value in errors.values():
                messages.error(request, value)
            return redirect("/quotes")
        else:
            new_quote = Quote.objects.create(
            quote=request.POST['quote'],
            quoted=request.POST['quoted'],
            poster=User.objects.get(id=request.session['user_id']))
    return redirect("/quotes")

def myaccount(request, id):
    if not 'user_id' in request.session:
            return redirect("/")
    context = {
        "user": User.objects.get(id=id),
        "all_the_quotes": Quote.objects.all(),
    }
    return render(request, "myaccount.html", context)

def myaccount_edit (request, id):
    if not 'user_id' in request.session:
            return redirect("/")
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0: 
            for value in errors.values():
                messages.error(request, value)
        else:
            # see if the username provided exists in the database
            user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
            if user: # note that we take advantage of truthiness here: an empty list will return false
                logged_user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if len(request.POST['new_password']) > 0:
                if bcrypt.checkpw(request.POST['old_password'].encode(), logged_user.password.encode()):
                    password = request.POST['new_password']
                    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    user.password = pw_hash
                else: 
                    messages.error(request,"Incorrect login credentials")
            user = User.objects.get(id=id)
            user.first_name=request.POST['first_name']
            user.last_name=request.POST['last_name']
            user.email=request.POST['email']
            user.save()
            messages.success(request, "Profile has been updated!")
            return redirect(f"/myaccount/{id}")
    return redirect(f"/myaccount/{id}")


def user(request, id):
    if not 'user_id' in request.session:
            return redirect("/")
    context = {
        "user": User.objects.get(id=id),
        "all_the_quotes": Quote.objects.all(),
    }
    return render(request, "user.html", context)

def quotes(request):
    if not 'user_id' in request.session:
            return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_the_quotes": Quote.objects.all(),
    }
    return render(request, "quotes.html", context)

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0: 
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'], 
                password=pw_hash) 
            request.session['user_id'] = user.id
            return redirect("/quotes")
    return redirect("/")



