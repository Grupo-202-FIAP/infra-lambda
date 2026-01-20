FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./
RUN pip install -r requirements.txt --target . --no-cache-dir

COPY . ./lambda_auth

CMD ["lambda_auth.handler.handler"]
