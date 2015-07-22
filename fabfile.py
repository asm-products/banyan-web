from fabric.api import local

def deploy():
   local('pip freeze > requirements.txt')
   local('git add .')
   print("enter your git commit comment: ")
   comment = raw_input()
   local('git commit -m "%s"' % comment)
   local('git push -u origin master')
   local('heroku maintenance:on')
   local('git push heroku master')
   local('heroku run python manage.py migrate')
   local('heroku maintenance:off')
