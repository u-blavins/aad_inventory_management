# Secret Sasquatch Society Inventory Manager
`aad_repo` contains the API definitions required for the inventory store management web application

## Workflow
Gitflow will be used to manage the project. There will be two branches within this repo; `master` and `develop`. Any features that is to be added to the repo should follow this flow:
```
master
    \develop
        \feature  # Feature branch has to be specific i.e. login-api, login-frontend
```

## Prerequisites
- Python 3.X
- Pip
- Virtualenv

## Setup
```
> virtualenv -p Python3 venv # 'venv' is just the name of the virtual environment
> source venv/bin/activate # this activates a virtual environment on linux/macos
> pip install -r requirements.txt # once virtualenv activated, run this command to install python libraries required  
```
> This setup is for local testing

## Resources
Below is a list of resources that will be useful for designing and implementing an API:
- [Virtual Environment Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/)
- [RESTful API Design Guide](https://apiguide.readthedocs.io/en/latest/build_and_publish/use_RESTful_urls.html)
- [Flask API Demo](https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask)
- [Flask Web Application](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/)
