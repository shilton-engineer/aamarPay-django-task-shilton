# Aamar Pay Django Project

###1. Install dependencies
run the following in terminal:
pip install -r requirements.txt

###2. Apply migrations
run the following again in terminal:
python manage.py makemigrations
python manage.py migrate

###3. Create a superuser
Run the following in terminal and provide your details:
python manage.py createsuperuser

###4. Run the server
run the server from terminal using:
python manage.py runserver

###5. Docker Setup
1. Build docker image: docker build -t myproject .
2. Run containers: docker-compose up --build

###6. API usage example
Get token/Login:
curl --location 'http://127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"your_username",
    "password":"your_password"
}'


Authentication:
curl --location 'http://127.0.0.1:8000/api/authenticate/' \
--header 'Authorization: Bearer access_token from the response of the previous API'

Initiate Payment
curl --location 'http://127.0.0.1:8000/api/initiate-payment/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer access_token_from_login' \
--data '{
    "amount":100
}'

Payment Success:
curl --location 'http://127.0.0.1:8000/api/payment/success/' \
--header 'Authorization: Bearer access_token_from_login'

Upload file
curl --location 'http://localhost:8000/api/upload/' \
--header 'Authorization: Bearer access_token_from_login' \
--form 'file=@"path_to_file"'


###Web Page
Visit: http://127.0.0.1:8000/accounts/login/?next=/api/dashboard/
to go check the dashbaord.