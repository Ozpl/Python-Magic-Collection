#!/usr/bin/env python
# coding: utf-8

# In[1]:


QUERY_TRANSLATE = [
    {
        "table_name": "colors",
        "table_type": "array",
        "query_command": ["color", "c"]
    },

    {
        "table_name": "color_identity",
        "table_type": "array",
        "query_command": ["id", "identity"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'type_line', 'type': 'string'}],
        "query_command": ["t", "type"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': '"set"', 'type': 'string'}, {'name':'set_name', 'type': 'string'}],
        "query_command": ["e", "edition", "s", "set"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'rarity', 'type': 'string'}],
        "query_command": ["r", "rarity"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'cmc', 'type': 'float'}],
        "query_command": ["cmc", "mv", "manavalue"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'oracle_text', 'type': 'string'}],
        "query_command": ["o", "oracle"]
    },

    {
        "table_name": "prices",
        "table_type": "object",
        "columns": [{'name': 'usd', 'type': 'float'}, {'name':'eur', 'type': 'float'}, {'name':'tix', 'type': 'float'}],
        "query_command": ["eur", "usd", "tix"]
    },

    {
        "table_name": "games",
        "table_type": "array",
        "query_command": ["game"]
    },

    {
        "table_name": "keywords",
        "table_type": "array",
        "query_command": ["keyword"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'released_at', 'type': 'datetime'}],
        "query_command": ["date", "year"]
    },

    {
        "table_name": "main",
        "table_type": "main",
        "columns": [{'name': 'name', 'type': 'string'}],
        "query_command": ["n", "name"]
    }

]


# In[2]:


def decide_operator(query_string):
    operator = ""
    if ">=" in query_string:
        operator = ">="
    elif "<=" in query_string:
        operator = "<="
    elif ">" in query_string:
        operator = ">"
    elif "<" in query_string:
        operator = "<"
    elif ":" in query_string:
        operator = ":"

    return operator


# In[11]:


def split_query(query_string):
    result = []
    separators = [" ", ";"]
    flag = False
    last_idx = 0
    for idx, char in enumerate(query_string):
        if char == '"':
            flag = True if not flag else False

        if not flag:
            if char in separators:
                result.append(query_string[last_idx:idx])
                last_idx = idx+1
    
    result.append(query_string[last_idx:])
    result = [element for element in result if len(element) > 0]
    return result


# In[4]:


def handle_query_when_array(table, column, value, command, operator):
    query = ""
    value = value.replace('"',"")
    elements_included = " AND ".join([f"{table}.{column} LIKE '%{char}%'" for char in value])
    match operator:
        case ">=" | ":":
            length = ""
            query = f"""{elements_included}"""
        case ">":
            length = f'length({table}.{column}) > {len(value) + (len(value)-1)}'
            query = f"""{length} AND {elements_included}"""
        case "=":
            length = f'length({table}.{column}) = {len(value) + (len(value)-1)}'
            query = f"""{length} AND {elements_included}"""
        case "<":
            length = f'length({table}.{column}) < {len(value) + (len(value)-1)}'
            query = f"""{length} AND ({" OR ".join([f"{table}.{column} LIKE '%{char}%'" for char in value])} OR length({table}.{column}) = 0)"""
        case "<=":
            length = f'length({table}.{column}) = {len(value) + (len(value)-1)}'
            query = f"""{" OR ".join([f"(length({table}.{column}) = 1 and instr({table}.{column}, '{char.upper()}') = 1)" for char in value])} OR (length({table}.{column}) = 0) OR ({length} AND {elements_included}"""[:-5]+") AND "

    return f"NOT ({query})" if command.find('-') > -1 else query


# In[3]:


def handle_query_when_number(table, operator, column, value, value_type):
    if value_type == "float":
        correct_value = float(value)
    elif value_type == "int":
        correct_value = int(value)
    
    correct_operator = operator if operator != ":" else "="
    query = f"{table}.{column} {operator} {str(correct_value)}"
    return query


# In[5]:


def handle_query_when_string(table, column, value, command, operator):
    value = value.replace('"',"")
    query = f"{table}.{column} {'LIKE' if command.find('-') == -1 else 'NOT LIKE'} '%{value}%'"
    return query


# In[6]:


def handle_query_when_date(table, operator, column, value, command):
    value = value.replace('"',"")
    query = ""
    correct_operator = operator if operator != ":" else "="
    if command == "year":
        query = f"CAST(STRFTIME('%Y',{table}.{column}) AS INT) {correct_operator} {str(int(value))}"
    else:
        query = f"{table}.{column} {correct_operator} '{str(value)}'"
    return query


# In[7]:


def handle_query_when_prices(operator, column, value):
    value = float(value)
    correct_operator = operator if operator != ":" else "="
    query = f"cast(prices.{column} as float) {correct_operator} {str(value)}"
    return query


# In[8]:


def handle_query_when_multiple_columns(table, columns, value):
    # "set" LIKE 'dom' OR set_name LIKE 'dom'
    query = " OR ".join([f"{table}.{column} LIKE '{value}'" for column in columns])
    return query


# In[9]:


def handle_query_when_format(operator, column, value):
    correct_operator = operator if operator != ":" else "="
    query = f""
    return query


# In[49]:


def construct_like_value(table_name, column_name, words):
    like_value = " AND ".join([f"{table_name}.{column_name} LIKE '%{word}%'" for word in words])
    return like_value


# In[57]:


def handle_query_when_no_operator(value):
    words = value.split(" ")
    query = f"({construct_like_value('main', 'name', words)}) OR ({construct_like_value('main', 'type_line', words)}) OR ({construct_like_value('main', 'oracle_text', words)})"
    return query


# In[20]:


def construct_query_when(query_string):
    query_array = []
    query_elements = split_query(query_string)

    for element in query_elements:
        operator = decide_operator(element)
        try:
            element_array = element.split(operator)
        except ValueError:
            query = handle_query_when_no_operator(query_string)
            return f"WHERE {query}"
            
        argument = element_array[0]
        value = element_array[1]
     
        for translation in QUERY_TRANSLATE:
            translation_commands = translation["query_command"]
            translation_commands_negative = [f"-{element}" for element in translation_commands]
            if argument in translation_commands or argument in translation_commands_negative:
                table_name = translation["table_name"]
                if translation["table_type"] == "main":
                    if len(translation["columns"]) == 1:
                        column = translation["columns"][0]
                        column_name = column["name"]
                        column_type = column["type"]
                        
                        if column_type in ['float', 'int']:
                            query = handle_query_when_number(table_name, operator, column_name, value, column_type)
                            query_array.append(query)
                        elif column_type in ['datetime']:
                            query = handle_query_when_date(table_name, operator, column_name, value, argument)
                            query_array.append(query)
                        else:
                            query = handle_query_when_string(table_name, column_name, value, argument, operator)
                            query_array.append(query)
                    else:
                        column_list = list(map(lambda ele: ele['name'], translation["columns"]))
                        query = handle_query_when_multiple_columns(table_name, column_list, value)
                        query_array.append(query)

                elif translation["table_type"] == "array":
                    query = handle_query_when_array(table_name,'array_value', value, argument, operator)
                    query_array.append(query)

                elif translation["table_type"] == "object":
                    match table_name:
                        case "prices":
                            query = handle_query_when_prices(operator, argument, value)
                            query_array.append(query)

    return f"WHERE {' AND '.join(query_array)}"


# In[10]:


def construct_query_join(table_name):
    join_query = f"""INNER JOIN {table_name}_table as {table_name} ON main.id = {table_name}.card_id """
    return join_query


# In[72]:


def construct_query(query_string=None):
    query = 'SELECT id FROM main_table main '
    if not query_string:
        return query
    try:
        query_commands = list(set([element.split(decide_operator(element))[0] for element in split_query(query_string)]))
    except ValueError:
        query_commands = []

    tables_to_include = []
    if query_commands: # default case will be empty array
        for element in query_commands:
            for record in QUERY_TRANSLATE:
                if element in record['query_command'] and record['table_type'] != "main":
                    tables_to_include.append(record['table_name'])

        for table in tables_to_include:
            join_query = construct_query_join(table)
            query += join_query

    query += construct_query_when(query_string)

    return query


# In[73]:


query_string = 'year>2010 c>gw cmc>5 eur>=10'
construct_query(query_string)