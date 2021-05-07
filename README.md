# Image Portfolio API

see all conditions in [Test_task_Python.pdf](./Test_task_Python.pdf)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

Create the project directory (for example 'portfolio')
```
mkdir portfolio
cd portfolio
```

Clone the repository to this folder

```
git clone https://github.com/Vitamal/lanars_portfolio
```
## Run local server with docker

Use [docker-compose](https://docs.docker.com/compose/) when working on this project. 

To build a container, run
```
$> docker-compose build
```

To get server started, run
```
$> docker-compose up
```

To run management commands, run bash in the docker environment with:

```
$> docker exec -it web sh
```

In the prompt that appears, you should be able to run e.g

```
$> python manage.py migrate
# or
$> python manage.py createsuperuser
```
or for creating new migrations
```
$> python manage.py makemigrations api
$> python manage.py makemigrations auth
```