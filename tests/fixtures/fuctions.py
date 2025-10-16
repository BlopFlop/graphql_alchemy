import re


def normalize_graphql_query(query):
    """
    Нормализует GraphQL запрос для сравнения, удаляя все пробелы и табы
    """
    # Удаляем все пробелы, табы и переносы строк
    query = re.sub(r'\s+', '', query)

    return query
