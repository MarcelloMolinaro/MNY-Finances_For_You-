from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config

app = Flask(__name__)
app.secret_key = "test_secret_key"
#i think the presence of a secret key initiates the session object,
#or the request object...

@app.route("/")
def home():
    if 'access_token' in session:
        print ('code 1')
        #this is where the export data code should be
        sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
        sObj.setAccessToken(session['access_token'])
        expensesObj = sObj.getExpenses(limit=1000, dated_after='01/01/2019')
        print ('Length of expensesObj = ', len(expensesObj))
        for x in expensesObj:
            print (x.getDescription(), x.getCost(), x.getCategory(), x.getDate())


        return redirect(url_for("friends"))
    print ('code 2')
    return render_template("home.html")

@app.route("/login")
def login(): #formerly" login" user_authorize
    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    print ('code 3')
    print (url) #for testing
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
    print('oauth_token sucessful')
    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    print('sObj sucessful')
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
    #test printingfriend objects
    for friend in friends:
        print (friend.getId())
    print (session)
    return render_template("friends.html",friends=friends)


#sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
#sObj.setAccessToken(session['access_token'])

#friendList = sObj.getFriends()
#groupList = sObj.getGroups()

#for x in friendList:
#    print (x.getFirstName())



if __name__ == "__main__":
    print ('code 8')
    app.run(threaded=True,debug=True)

print (session)
