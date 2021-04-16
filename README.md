# crud-api-test
1

```linux
  docker-compose -f docker-compose.yml up -d --build
  docker-compose -f docker-compose.yml exec web python manage.py crontab add
  docker-compose -f docker-compose.yml exec web python manage.py migrate
  docker-compose -f docker-compose.yml exec web python manage.py collectstatic
```

[localhost](http://localhost/api/) <br/>
[heroku](https://django-crud-ostapenko.herokuapp.com/api/) <br/>
[Postman Doc](https://documenter.getpostman.com/view/12567904/TzJrDKbf)
