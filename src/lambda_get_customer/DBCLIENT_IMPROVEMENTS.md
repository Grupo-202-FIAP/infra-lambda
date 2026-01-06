# Melhorias no DBClient

## Contexto

O `DBClient` original em `lambda_registration` só possuía o método `execute()` para operações de escrita (INSERT, UPDATE, DELETE).

Para o `lambda_get_customer`, foi necessário adicionar métodos de leitura para consultar o RDS.

## Métodos Adicionados

### 1. `fetch_one(query, params=None)`

Executa uma query SELECT e retorna **um único resultado** como dicionário.

**Uso:**
```python
db = DBClient()
customer = db.fetch_one(
    "SELECT * FROM customers WHERE id = %s",
    (customer_id,)
)
# Retorna: {'id': '123', 'name': 'John Doe', ...} ou None
```

**Características:**
- Retorna `dict` se encontrar resultado
- Retorna `None` se não encontrar
- Usa `RealDictCursor` para retornar dicionários ao invés de tuplas
- Ideal para buscas por ID ou chave única

### 2. `fetch_all(query, params=None)`

Executa uma query SELECT e retorna **múltiplos resultados** como lista de dicionários.

**Uso:**
```python
db = DBClient()
customers = db.fetch_all(
    "SELECT * FROM customers WHERE name LIKE %s",
    ('%John%',)
)
# Retorna: [{'id': '1', 'name': 'John'}, {'id': '2', 'name': 'Johnny'}]
```

**Características:**
- Retorna `list[dict]` com todos os resultados
- Retorna `[]` (lista vazia) se não encontrar
- Usa `RealDictCursor` para retornar dicionários
- Ideal para listagens e buscas que retornam múltiplos registros

## Vantagens

1. **Tipo de retorno consistente**: Sempre retorna dicionários, facilitando o acesso aos dados
2. **Segurança**: Continua usando prepared statements (parametrização)
3. **Logging**: Mantém o padrão de logging do projeto
4. **Tratamento de erros**: Exceptions são logadas e propagadas corretamente

## Comparação com o DBClient Original

### Original (lambda_registration)
```python
class DBClient:
    def execute(self, query, params=None):
        """Apenas INSERT/UPDATE/DELETE"""
        with self._conn.cursor() as cursor:
            cursor.execute(query, params)
        self._conn.commit()
```

### Melhorado (lambda_get_customer)
```python
class DBClient:
    def execute(self, query, params=None):
        """INSERT/UPDATE/DELETE"""
        # ... mesmo código
    
    def fetch_one(self, query, params=None):
        """SELECT retornando 1 registro"""
        with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def fetch_all(self, query, params=None):
        """SELECT retornando N registros"""
        with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return [dict(row) for row in results] if results else []
```

## Recomendação

É recomendado **atualizar o DBClient do lambda_registration** para incluir esses métodos, tornando-o mais completo e reutilizável em todos os Lambdas do projeto.

## Retrocompatibilidade

Os métodos adicionados **não quebram** o código existente. O método `execute()` continua funcionando exatamente como antes.

## Exemplo de Uso no Projeto

```python
# lambda_registration (existente) - continua funcionando
db = DBClient()
db.execute(
    "INSERT INTO customers (name, email) VALUES (%s, %s)",
    (name, email)
)

# lambda_get_customer (novo) - agora funciona também
db = DBClient()
customer = db.fetch_one(
    "SELECT * FROM customers WHERE email = %s",
    (email,)
)
```
