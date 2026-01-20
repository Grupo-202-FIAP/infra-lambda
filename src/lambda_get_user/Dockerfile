FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt  ./
RUN python -m pip install -r requirements.txt -t .

COPY . ./lambda_get_user

CMD ["lambda_get_user.handler.handler"]
