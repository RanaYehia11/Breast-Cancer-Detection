from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, hashers
from signup.models import Signup  # type: ignore 
from .models import Login  # Import the Login model

# View function to handle user login
def index(request):
    # Check if the request method is POST (i.e., form submitted)
    if request.method == "POST":
        # Get email and password from the submitted form
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Try to get the user from the Signup model using the provided email
            user = Signup.objects.get(email=email)

            # Check if the provided password matches the hashed password in the database
            if hashers.check_password(password, user.password):
                # If password is correct, show a success message
                messages.success(request, "Login successful!")

                # Create or update the user's login record
                Login.objects.update_or_create(
                    email=email, defaults={"password": user.password}
                )

                # Redirect to the home page after successful login
                return redirect("home")
            else:
                # If password is incorrect, show an error message
                messages.error(request, "Invalid password. Please try again.")
        except Signup.DoesNotExist:
            # If email is not found in the Signup model, show an error message
            messages.error(request, "Invalid email or password. Please sign up first.")

   
    return render(request, "pages/login.html")


# View function to handle user logout
def user_logout(request):
    # Clear any previous messages to avoid showing them again
    storage = messages.get_messages(request)
    storage.used = True  

    # Log out the user using Django's built-in logout function
    logout(request)

    # Show a success message after logout
    messages.success(request, "Logged out successfully.")

    # Redirect to the login page
    return redirect("login")

