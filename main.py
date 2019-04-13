#!/usr/bin/env python

#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import re

template_dir= os.path.join(os.path.dirname('main.py'),'templates')                         
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
   
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)    
    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))
        
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$") 
def valid_username(username):
        return username and  USER_RE.match(username)
    
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
        return password and PASS_RE.match(password)
    
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')    
def valid_email(email):
        return email and EMAIL_RE.match(email)     
         
class MainPage(Handler):
    def get(self):
        self.render('signup.html')
    def post(self):
        have_error = False
        username = self.request.get('username') 
        password = self.request.get('password')
        vpassword = self.request.get('vpassword')
        email = self.request.get('email')
        params = dict(username = username, email = email)       
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != vpassword:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            

        if  have_error:    
            self.render('signup.html', ** params)
        else:
            self.redirect('/welcome?'+username)
          
class Welcome(Handler):
    def get(self):
             user=self.request.get("username")   
             if user:                  
                  self.render('welcome.html',username=user)     
               
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/welcome', Welcome)],                            
                            debug=True)  

