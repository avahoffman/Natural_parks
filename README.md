# National Parks

Make sure to run 
	Python app.py
To start.

Killing web app dynos while troubleshooting deployment can be achieved with
	heroku ps:scale web=0
This kills the web app to allow updating
	git add .
	git commit -a -m "updated xyz"
	git push origin master
	git push web master
