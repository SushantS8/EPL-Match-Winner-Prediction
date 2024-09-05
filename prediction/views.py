from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
from .forms import RegistrationForm,AuthenticationForm
# prediction/views.py
from django.shortcuts import render
import joblib
from django.contrib.auth import login, authenticate,logout


from django.contrib.auth.decorators import login_required


import joblib
import numpy as np
import pandas as pd
# Load your trained machine learning model
cls = joblib.load('logistic_regression_model.sav')# Replace 'my_model.sav' with your model file path

def make_prediction(venue_code, hour,sh,sot,pk,gls):
    # Create a dictionary to hold the input features
    input_features = {
     
        'venue_code': venue_code,
        'hour': hour,
        'sh':sh,
        'sot':sot,
        'pk':pk,
        'gls':gls,
        
    }

    # Convert the input features to a NumPy array
    input_array = np.array([list(input_features.values())])

    # Make the prediction using the loaded model
    prediction = cls.predict(input_array)

    # Convert the prediction to a human-readable result
    #result = "Te if prediction == 1 else "Team2 Wins"

    return prediction

# Load the team-specific data from a CSV file
team_data = pd.read_csv('matches.csv')

def get_team_data(team_name):
    print(team_name)
    # Find the row corresponding to the given team_name
    team_row = team_data[team_data['team'] == team_name]

    if not team_row.empty:
        sh = team_row.iloc[0]['sh']
        sot = team_row.iloc[0]['sot']
        pk = team_row.iloc[0]['pk']
        gls = team_row.iloc[0]['gls']


        print("sh:", sh)
        print("sot:", sot)
        print("pk:", pk)
        print("gls:", gls)


        return sh, sot, pk, gls
    else:
        print("Team not found in data source")
        return None, None, None, None


@login_required(login_url="prediction:login")
def home(request):
    result = ""
    if request.method == "POST":
        team_1 = request.POST.get('team1')
        team_2 = request.POST.get('team2')
        print(team_1)
        print(team_2)
        team2 = request.POST.get('team2')
        #home_team = int(request.POST.get('team1'))
        #away_team = int(request.POST.get('team2'))
        venue = request.POST.get('venue')
        print(venue)
        hour = request.POST.get('time')
        if venue == "Venue" or None or team_1 == "Team1" or team_2 == "Team2" or hour == "":
            messages.add_message(request, messages.ERROR, "Fill all the fields")
            return redirect('prediction:home')
        
        venue = int(request.POST.get('venue'))
        hour = int(hour)
        if hour < 0:
            messages.add_message(request,messages.ERROR,"Hour cannot be negative")
            return redirect('prediction:home')
        print('checked in')
        #print(away_team)
        #print(f"team1: {type(home_team)}")
       # print(f"team2: {type(away_team)}")
        print(f"venue: {type(venue)}")
        print(f"hour: {type(hour)}")

       # print(home_team)
        print(venue)
        print(hour)

        if team_1 == team_2:
            messages.add_message(request, messages.ERROR, "You cannot select same team")
            return redirect('prediction:home')
        else:
            home_team_sh, home_team_sot, home_team_pk, home_team_gls = get_team_data(team_1)
            print("Team 1: ")
            print(home_team_sh)
            print(home_team_sot)
            print(home_team_pk)
            print(home_team_gls)


            away_team_sh, away_team_sot, away_team_pk, away_team_gls = get_team_data(team2)
            print("Team 2: ")
            print(away_team_sh)
            print(away_team_sot)
            print(away_team_pk)
            print(away_team_gls)

            
            
            ans1 = make_prediction(venue,hour,home_team_sh,home_team_sot,home_team_pk,home_team_gls)
            print("Result: ")
            print(ans1)

            if ans1 == 0:
                result = f"{team_2} win"
            else:
                result = f"{team_1} win"
            
            
  



    return render(request,"index.html",{'result':result})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('prediction:home')  # Replace 'home' with your desired redirect URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.ERROR, "Registered Successfully")
            """  username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) """
            return redirect('prediction:register')  # Replace 'home' with your desired URL after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url="prediction:login")
def logout_view(request):
    logout(request)
    return redirect("prediction:login")