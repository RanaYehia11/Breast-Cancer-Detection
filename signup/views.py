from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Signup
from django.contrib.auth.hashers import make_password  # Import password hashing

# View function to handle user signup
def signup(request):
    # Check if the request method is POST (i.e., form was submitted)
    if request.method == "POST":
        # Retrieve form data from POST request
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if a user with the same email already exists in the database
        if Signup.objects.filter(email=email).exists():
            # Show error message if email is already registered
            messages.error(request, "This email is already registered. Please use a different email.")
            return redirect("signup")  # Redirect back to the signup page

        # Hash the password for security before storing it in the database
        hashed_password = make_password(password)

        # Create a new Signup object and save it to the database
        new_user = Signup(fname=fname, lname=lname, email=email, password=hashed_password)
        new_user.save()

        # Show success message after successful signup
        messages.success(request, "Signup successful! Please log in.")

        # Redirect to the login page
        return redirect("login")
    return render(request, "pages/signup.html")
