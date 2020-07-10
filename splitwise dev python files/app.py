from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config
import pandas as pd
#clean up this code so that I don't jump around to the template pages
#I don't even need the tempalte pages
#and if possible, I don't have to initiate the body of code by going to the
#local host URL...Or maybe only if not authenticated?

app = Flask(__name__)
app.secret_key = "test_secret_key"
#i think the presence of a secret key initiates the session object,
#or the request object...


#Wiley would have another page that has a text box
#have an execute page
#use EVAL to pull python code out and run it
#do it becasue if access is incorrect, it will error line25
@app.route("/")
def home():
    if 'access_token' in session:
        print ('code 1')
        sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
        sObj.setAccessToken(session['access_token'])
        expensesObj = sObj.getExpenses(limit=30, dated_after='01/01/2020')
        
        print(session['access_token']) #this is a dict object with 2 keys
        return "<p>" + "oauth_token: " + \
            session['access_token'].get('oauth_token') +\
            "\noauth_token_secret: " + \
             session['access_token'].get('oauth_token_secret') +\
             "</p>"
        #return redirect(url_for("friends"))
    print ('code 2')
    #return session['access_token']
    return render_template("home.html")

@app.route("/login")
def login():
    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    print ('code 3')
    print (url)
    #This is where SPlitwise redirects to authorize the user
    #could return access token *wiley
    return redirect(url)#I specify this 'callback-URL' when registering the app,
                        #It can be changed. It is currently: /authorize, which
                        #redirects to the below function

@app.route("/authorize")
def authorize(): #this is actualy API_Authorize"

    if 'secret' not in session:
        print ('code 4')
        return redirect(url_for("home"))

    #this oauth is IN the 'callback-URL'. Yes, it's inside the URL.
    #http...splitwise.com/authorize?oauth_token=RTjHAra....
    #The URL's base_url is http...splitwise.com/authorize
    #But it also contains the oauth_token! after the ?...I don't know where the verifier is...
    oauth_token    = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    print (oauth_token, oauth_verifier)
    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    print ('sObj set')
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    session['access_token'] = access_token

    print ('code 5')
    return redirect(url_for("friends"))

@app.route("/friends")
def friends():
    if 'access_token' not in session:
        print ('code 6')
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()
    print ('code 7')
    return render_template("friends.html",friends=friends)


if __name__ == "__main__": #handy way to set conditions, only run if it's main
    print ('code 8')
    app.run(threaded=True,debug=True)
    