FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt  ./
RUN python -m pip install -r requirements.txt -t .

COPY . ./lambda_list_users

CMD ["lambda_list_users.handler.handler"]
