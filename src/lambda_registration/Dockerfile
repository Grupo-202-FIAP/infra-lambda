FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./
RUN pip install -r requirements.txt --target . --no-cache-dir

# 👇 Copia o diretório completo mantendo o nome 'lambda_registration'
COPY . ./lambda_registration

# Ajuste o CMD para apontar para o handler dentro do pacote
CMD ["lambda_registration.handler.handler"]
