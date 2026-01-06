FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./
RUN pip install -r requirements.txt --target . --no-cache-dir

COPY . ./lambda_get_customer

CMD ["lambda_get_customer.handler.handler"]
