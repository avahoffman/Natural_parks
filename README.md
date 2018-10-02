# National Parks  
Well, I named the repository Natural Parks, oops.



# Helpful tips / notes  
Helpful to me anyway.   

To start your app, make sure to run

	Python app.py  
 
log in to heroku

    heroku login

Check heroku apps running with    

    heroku ps 
    
Killing web app dynos while troubleshooting deployment can be achieved with the commands below. Make sure to scale back to 1 before attempting to load the web version!  

    heroku ps:scale web=0
    heroku ps:restart web.1
    heroku ps:kill web.1
    heroku ps:stop run.

Check logs  
    
    heroku logs --tail
    
Push to origin and web
    
      git add .
	git commit -a -m "logs"
	git push origin master
	git push web master OR git push heroku master


Helpful TUTORIALS:  
https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50  
https://stackoverflow.com/questions/35247347/point-heroku-application-to-aws-rds-database

