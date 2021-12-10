from flask import redirect, g, flash, request
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user
import jwt


class CustomAuthDBView(AuthDBView):
    login_template = 'appbuilder/general/security/login_db.html'

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
	    #This is to decode the JWT (ath_un). The below key needs to match the athletedataapp's secret key.
        athletedata_secret_key = '<YOUR ATHLETE DATA APP SECRET KEY>'
        redirect_url = self.appbuilder.get_url_for_index
        if request.args.get('redirect') is not None:
            redirect_url = request.args.get('redirect') 

        if request.args.get('username') is not None:
            try:
                #Decode and retrieve ath_un from the link
                ath_un = jwt.decode(request.args.get('username'), key=athletedata_secret_key, algorithms="HS256")['ath_un']
                if not ath_un:
                    flash('  Something went wrong. Please log-in','danger')
                    return super(CustomAuthDBView,self).login()
            except:
                #Token expired
                jwt.exceptions.ExpiredSignatureError
                flash('  You used an expired token. Please log-in.','danger')
                return super(CustomAuthDBView,self).login()

            user = self.appbuilder.sm.find_user(ath_un)
            login_user(user, remember=False)
            return redirect(redirect_url)
        #elif g.user is not None and g.user.is_authenticated():
            #return redirect(redirect_url)
        else:
            flash('Unable to auto login', 'warning')
            return super(CustomAuthDBView,self).login()

class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)