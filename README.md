# graphql_alchemy

Библиотека для типобезопасного построения GraphQL запросов из Python-моделей. Поддерживает преобразование dataclasses/ Pydantic/dict в GraphQL схемы.

## Возможности

- ✅ **Типобезопасное построение GraphQL запросов**
- ✅ **Поддержка трех типов моделей**: dataclasses, Pydantic, словари
- ✅ **Сложные вложенные структуры**
- ✅ **Автоматическая генерация схемы**
- ✅ **Входные параметры и переменные**
- ✅ **Валидация типов данных**

## Структура библиотеки
```
├── src/                           # Исходный код библиотеки
│   ├── __init__.py
│   ├── const.py                  # Константы и настройки
│   ├── converter/                # Модули конвертации моделей в GraphQL
│   │   ├── __init__.py
│   │   ├── base.py               # Базовый класс конвертера
│   │   ├── dataclass_.py         # Конвертер для dataclasses
│   │   ├── dict_.py              # Конвертер для словарей
│   │   └── pydantic_.py          # Конвертер для Pydantic моделей
│   ├── types/                    # Типы данных и классы GraphQL
│   │   ├── __init__.py
│   │   ├── base.py               # Базовые классы типов
│   │   ├── enums.py              # Перечисления (GraphQL методы и т.д.)
│   │   └── query.py              # Классы для построения GraphQL запросов
│   └── utils.py                  # Вспомогательные функции
├── tests/                        # Тесты библиотеки
│   ├── __init__.py
│   ├── fixtures/                 # Фикстуры и тестовые данные
│   │   ├── __init__.py
│   │   ├── fuctions.py
│   │   └── queries.py            # Примеры GraphQL запросов для проверки
│   ├── test_converter/           # Тесты конвертеров
│   │   ├── __init__.py
│   │   ├── test_base.py          # Тесты базового конвертера
│   │   ├── test_dataclass.py     # Тесты конвертера dataclasses
│   │   └── test_pydantic.py      # Тесты конвертера Pydantic
│   ├── test_method.py            # Тесты GraphQL методов
│   ├── test_query/               # Тесты построения запросов
│   │   ├── __init__.py
│   │   ├── test_dataclass.py     # Тесты запросов из dataclasses
│   │   ├── test_dict.py          # Тесты запросов из словарей
│   │   └── test_pydantic.py      # Тесты запросов из Pydantic моделей
│   ├── test_query_generator.py   # Тесты генератора запросов
│   └── test_utils.py             # Тесты вспомогательных функций
├── README.md                     # Документация проекта
├── pyproject.toml                # Конфигурация проекта и зависимости
└── uv.lock                       # Файл блокировки версий зависимостей (uv)
```

## Быстрый старт

### 1. Использование с Dataclasses

```python
from dataclasses import dataclass
from graphql_query import GraphQlQuery, GraphQlMethodType
from graphql_query.converter import dataclass_ as dataclass_converter

@dataclass
class User:
    typename: str = "User"
    id: int
    name: str
    email: str

@dataclass
class ReturnError:
    typename: str = "ReturnError"
    message: str

# Создание GraphQL запроса
query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetUser",
    name_method="getUser",
    inputs={"user_id": 123},
    models=dataclass_converter.build_graph_ql_models([User, ReturnError]),
)

print(str(query))
```

**Результат GraphQL:**
```graphql
query GetUser($user_id: Int!) {
  getUser(user_id: $user_id) {
    ... on User {
      id
      name
      email
    }
    ... on ReturnError {
      message
    }
  }
}
```

### 2. Использование с Pydantic

```python
from pydantic import BaseModel, Field
from graphql_query import GraphQlQuery, GraphQlMethodType
from graphql_query.converter import pydantic_ as pydantic_converter

class User(BaseModel):
    typename: str = Field(default="User", alias="__typename")
    id: int
    name: str
    email: str

class UserInput(BaseModel):
    user_id: int

# Создание запроса
query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetUser",
    name_method="getUser",
    inputs=UserInput(user_id=123).model_dump(),
    models=pydantic_converter.build_graph_ql_models([User]),
)

print(str(query))
```

**Результат GraphQL:**
```graphql
query GetUser($user_id: Int!) {
  getUser(user_id: $user_id) {
    id
    name
    email
  }
}
```

### 3. Использование со словарями

```python
from graphql_query import GraphQlQuery, GraphQlMethodType
from graphql_query.converter.dict_ import build_graph_ql_models

user_schema = {
    "__typename": "User",
    "id": 1,
    "name": "John",
    "email": "john@example.com"
}

query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetUser",
    name_method="getUser",
    inputs={"user_id": 123},
    models=build_graph_ql_models([user_schema]),
)

print(str(query))
```

## Расширенные примеры

### Сложные вложенные модели

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Address:
    city: str
    street: str
    zip_code: str

@dataclass
class Company:
    name: str
    address: Address

@dataclass
class User:
    typename: str = "User"
    name: str
    email: str
    company: Company
    friends: List["User"]

# Автоматически генерирует вложенные GraphQL поля
query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetUserWithFriends",
    name_method="getUser",
    inputs={"user_id": 123},
    models=dataclass_converter.build_graph_ql_models([User]),
)
print(str(query))
```

**Результат GraphQL:**
```graphql
query GetUserWithFriends($user_id: Int!) {
  getUser(user_id: $user_id) {
    name
    email
    company {
      name
      address {
        city
        street
        zip_code
      }
    }
    friends {
      name
      email
      company {
        name
        address {
          city
          street
          zip_code
        }
      }
    }
  }
}
```

### Пагинация и фильтрация

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Research:
    title: str
    description: str
    status: str

@dataclass
class ResearchPagination:
    typename: str = "ResearchPagination"
    researches: List[Research]
    pages: int
    current_page: int

@dataclass  
class FilterInput:
    status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


@dataclass
class ResearchFilterInput:
    pass


# Запрос с пагинацией и фильтрацией
query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetResearches",
    name_method="researches",
    inputs={
        "filter": ResearchFilterInput(),
        "page": 1,
        "limit": 10
    },
    models=dataclass_converter.build_graph_ql_models([ResearchPagination]),
)
print(str(query))
```

**Результат GraphQL:**
```graphql
query GetResearches($filter: ResearchFilterInput, $page: Int, $limit: Int) {
  researches(filter: $filter, page: $page, limit: $limit) {
    researches {
      title
      description
      status
    }
    pages
    current_page
  }
}
```

### Мутации с входными параметрами

```python
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class CreateUserInput:
    name: str
    email: str
    password: str

@dataclass
class User:
    id: UUID
    name: str
    email: str

@dataclass
class CreateUserResponse:
    user: User
    success: bool
    message: str


@dataclass
class CreateUserInput:
    typename: str = "CreateUserInput"


mutation = GraphQlQuery(
    type_method=GraphQlMethodType.mutation,
    name="CreateUser",
    name_method="createUser",
    inputs={"input": CreateUserInput()},
    models=dataclass_converter.build_graph_ql_models([CreateUserResponse]),
)
print(str(mutation))
```

**Результат GraphQL:**
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
    success
    message
  }
}
```

### Union типы и обработка ошибок

```python
from dataclasses import dataclass
from typing import Union

@dataclass
class User:
    typename: str = "User"
    id: int
    name: str
    email: str

@dataclass
class NotFoundError:
    typename: str = "NotFoundError"
    message: str
    resource: str

@dataclass
class ValidationError:
    typename: str = "ValidationError" 
    message: str
    field: str

# Union тип для разных возможных ответов
UserResult = Union[User, NotFoundError, ValidationError]

query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetUserWithErrors",
    name_method="getUser",
    inputs={"user_id": 123},
    models=dataclass_converter.build_graph_ql_models([User, NotFoundError, ValidationError]),
)
print(str(query))
```

**Результат GraphQL:**
```graphql
query GetUserWithErrors($user_id: Int!) {
  getUser(user_id: $user_id) {
    ... on User {
      id
      name
      email
    }
    ... on NotFoundError {
      message
      resource
    }
    ... on ValidationError {
      message
      field
    }
  }
}
```

### Сложные исследовательские модели (из тестов)

```python
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Optional

@dataclass
class Duration:
    duration: int
    duration_cost: float
    duration_id: int

@dataclass
class ResearchCalc:
    age_max: int
    age_min: int
    count_respondent: int
    duration: Duration
    research_calc_uid: UUID

@dataclass
class Research:
    research_name: str
    research_cost: float
    research_count_respondent: int
    research_calc: ResearchCalc
    research_uid: UUID = field(default_factory=uuid4)

query = GraphQlQuery(
    type_method=GraphQlMethodType.query,
    name="GetResearch",
    name_method="research",
    inputs={"research_uid": UUID("12345678-1234-1234-1234-123456789012")},
    models=dataclass_converter.build_graph_ql_models([Research]),
)
print(str(query))
```

**Результат GraphQL:**
```graphql
query GetResearch($research_uid: UUID!) {
  research(research_uid: $research_uid) {
    research_name
    research_cost
    research_count_respondent
    research_calc {
      age_max
      age_min
      count_respondent
      duration {
        duration
        duration_cost
        duration_id
      }
      research_calc_uid
    }
    research_uid
  }
}
```

## DataConverter - Универсальный конвертер

```python
from graphql_query.converter import DataConverter

# Автоматическое определение типа модели
converter = DataConverter(User, ReturnError, input_data={"user_id": 123})

# Конвертация данных
result = converter(user_data)
variables = converter.variables
models = converter.models
```

### Поддерживаемые преобразования

| Входной тип | Выходной тип | Использование |
|-------------|--------------|---------------|
| Dataclass | Dataclass | `DataConverter(DataclassModel)` |
| Pydantic | Pydantic | `DataConverter(PydanticModel)` |
| Dict | Dict | `DataConverter(dict_schema)` |
| Mixed | TypeError | ❌ Не поддерживается |

## Типы данных

Библиотека поддерживает все основные типы GraphQL:

- **Скалярные типы**: `String`, `Int`, `Float`, `Boolean`, `ID`
- **Сложные типы**: объекты, списки, не-nullable типы
- **Специальные типы**: `UUID`, `DateTime` (через кастомные скаляры)
- **Union типы**: `Union[TypeA, TypeB]`
- **Optional типы**: `Optional[str]` → `String`

## Установка

```bash
pip install qraphql-alchemy
```

## Тестирование

```bash
# Запуск всех тестов
pytest tests/

# Тесты конкретного модуля
pytest tests/test_query.py -v
pytest tests/test_converter.py -v
```

## Особенности
### 🔄 **Мульти-формат**
Одинаковая функциональность для dataclasses, Pydantic и словарей

### 🏗️ **Автоматическая генерация**
Рекурсивное построение GraphQL схем из сложных моделей

### 🛡️ **Валидация**
Проверка совместимости типов и структуры данных

## Ограничения

- ❌ Смешивание разных типов моделей в одном конвертере
- ❌ Кастомные директивы GraphQL
- ❌ Фрагменты и inline fragments
- ❌ Подписки (subscriptions)

## Совместимость

- Python 3.11+
- GraphQL стандарт
- Совместимо с большинством GraphQL клиентов и серверов
