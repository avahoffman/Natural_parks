# National Parks

Make sure to run 
	Python app.py
To start.

Killing web app dynos while troubleshooting deployment can be achieved with
	heroku ps:scale web=0
This kills the web app to allow updating
	
    git add .
	git commit -a -m "updated sql"
	git push origin master
	git push web master OR git push heroku master


SEE TUTORIAL:  
https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50  
