# public toilets

## database + pgadmin4

to start database and pgadmin4 run in main folder `docker-compose up`  
you should be able to visit pgadmin4 at **localhost:5050**

## backend

to start backend run in main folder `source env/bin/activate` then `uvicorn app.main:app --reload`  
backend should be available at **http://127.0.0.1:8000**

### tests

to run tests db must be running, then run `pytest`

### lint

`black app/`

### helpers

to find runing port type `sudo lsof -t -i:5432` and then u can kill it with `sudo kill -9 {id}` where **id** is returned from first command

to add database in **pgadmin4 web** use `docker inspect CONTAINER_ID | grep IPAddress.` it will return database host
