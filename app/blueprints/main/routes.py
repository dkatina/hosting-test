from . import  main
from flask import request, render_template, redirect, url_for
from app.models import User, db
from flask_login import current_user, login_required
import requests

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/user/<name>')
def user(name):
    return f"Hello {name}"

#helper function to get driver data
    
def getDriverInfo(driver):
    driver_info = {
        'position': driver['position'],
        'first_name': driver['Driver']['givenName'],
        'last_name': driver['Driver']['familyName'],
        'DOB': driver['Driver']['dateOfBirth'],
        'wins': driver['wins'],
        'team': driver['Constructors'][0]['name']
    }
    return driver_info
    
def driver_info_year_rnd(year, rnd):
    url = f'https://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
    response = requests.get(url)
    drivers = []
    if response.ok:
        data = response.json()
        driver_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for driver in driver_standings:
            driver_dict = getDriverInfo(driver)
            drivers.append(driver_dict)
    return drivers
    
@main.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('round')
        drivers = driver_info_year_rnd(year,rnd)
        return render_template('ergast.html', drivers=drivers)
    else:
        return render_template('ergast.html')
    
@main.route('/users')
def users():
    users = User.query.filter(User.id != current_user.id)
    return render_template('users.html', users=users)
    

@main.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.following.append(user)
    db.session.commit()
    return redirect(url_for('main.users'))

@main.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    current_user.following.remove(user)
    db.session.commit()
    return redirect(url_for('main.users'))

    