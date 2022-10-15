from modules.database.database_functions import get_database_table_name

QUERY_TRANSLATE = [
    {
        "columns": ["colors"],
        "type": "array",
        "query_command": ["color", "c"]
    },

    {
        "columns": ["color_identity"],
        "type": "array",
        "query_command": ["id", "identity"]
    },

    {
        "columns": ["type_line"],
        "type": "string",
        "query_command": ["t", "type"]
    },

    {
        "columns": ["set", "set_name"],
        "type": "string",
        "query_command": ["e", "edition", "s", "set"]
    },

    {
        #TODO: needs to have 3 operator: :/=, >=, < xd
        "columns": ["rarity"],
        "type": "string",
        "query_command": ["r", "rarity"]
    },

    {
        "columns": ["cmc"],
        "type": "float",
        "query_command": ["cmc", "mv", "manavalue"]
    },

    {
        "columns": ["oracle_text"],
        "type": "string",
        "query_command": ["o", "oracle"]
    },

    {
        "columns": ["prices"],
        "type": "object",
        "query_command": ["eur", "usd", "tix"]
    },

    {
        "columns": ["games"],
        "type": "array",
        "query_command": ["game", "games"]
    },

    {
        "columns": ["keywords"],
        "type": "array",
        "query_command": ["keyword"]
    },

    {
        "columns": ["released_at"],
        "type": "datetime",
        "query_command": ["date", "year"]
    },

]


def decide_operator(query_string:str) -> str:
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
    elif "=" in query_string:
        operator = "="

    return operator


def split_query(query_string:str) -> list:
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


def handle_query_when_number(table:str, operator:str, column:str, value:str, value_type:str) -> str:
    if value_type == "float":
        correct_value = float(value)
    elif value_type == "int":
        correct_value = int(value)
    
    correct_operator = operator if operator != ":" else "="
    query = f"{table}.{column} {correct_operator} {str(correct_value)}"
    return query


def handle_query_when_string(table:str, column:str, value:str, command:str, operator:str) -> str:
    value = value.replace('"',"")
    query = f"{table}.{column} {'LIKE' if command.find('-') == -1 else 'NOT LIKE'} '%{value}%'"
    return query


def handle_query_when_string_multiple_columns(table:str, columns:str, value:str, command:str) -> str:
    # "set" LIKE 'dom' OR set_name LIKE 'dom'
    value = value.replace('"',"")
    query = " OR ".join([f"{table}.{column} {'LIKE' if command.find('-') == -1 else 'NOT LIKE'} '{value}'" for column in columns])
    return query


def handle_query_when_string_array(table:str, column:str, value:str, command:str, operator:str) -> str:
    values = value.replace('"',"").split(",")
    query = " AND ".join([f"{table}.{column} {'LIKE' if command.find('-') == -1 else 'NOT LIKE'} '%{value}%'" for value in values])
    return query


def handle_query_when_color_array(table:str, column:str, value:str, command:str, operator: str):
    query = ""
    value = value.replace('"',"")
    elements_included = " AND ".join([f"{table}.{column} LIKE '%{char}%'" for char in value])
    length = f"""json_array_length(json(replace({table}.{column}, "'", '"')))"""
    match operator:
        case ">=" | ":":
            query = f"""{elements_included}"""
        case ">" | "=":
            query = f"""{length} {operator} {len(value)} AND {elements_included}"""
        case "<":
            query = f"""{length} < {len(value)} AND ({" OR ".join([f"{table}.{column} LIKE '%{char}%'" for char in value])} OR {length} = 0)"""
        case "<=":
            extract = f"""json_extract(json(replace({table}.{column}, "'", '"')), '$[0]')"""
            query = f"""{" OR ".join([f"({length} = 1 and {extract} = '{char.upper()}')" for char in value])} OR ({length} = 0) OR ({length} = {len(value)} AND {elements_included})"""

    return f"NOT ({query})" if command.find('-') > -1 else query


def handle_query_when_object_prices(table:str, column:str, value:str, command:str, operator:str) -> str:
    value = value.replace('"',"")
    correct_operator = operator if operator != ":" else "="
    query = f"""IIF(cast(json_extract(json(replace(replace(prices, "'", '"'), "None", "null")), '$.{command}') as float) is not null, cast(json_extract(json(replace(replace(prices, "'", '"'), "None", "null")), '$.{command}') as float) {correct_operator} {value}, iif(cast(json_extract(json(replace(replace(prices, "'", '"'), "None", "null")), '$.{command}_foil') as float) is not null, cast(json_extract(json(replace(replace(prices, "'", '"'), "None", "null")), '$.{command}_foil') as float) {correct_operator} {value}, cast(json_extract(json(replace(replace(prices, "'", '"'), "None", "null")), '$.{command}_etched') as float) {correct_operator} {value}))"""
    return query


def handle_query_when_date(table:str, operator:str, column:str, value:str, command:str) -> str:
    value = value.replace('"',"")
    query = ""
    correct_operator = operator if operator != ":" else "="
    if command == "year":
        query = f"CAST(STRFTIME('%Y',{table}.{column}) AS INT) {correct_operator} {str(int(value))}"
    else:
        query = f"{table}.{column} {correct_operator} '{str(value)}'"
    return query


def construct_like_value(table_name:str, column_name:str, words:str) -> str:
    like_value = " AND ".join([f"{table_name}.{column_name} LIKE '%{word}%'" for word in words])
    return like_value


def handle_query_when_no_operator(table_name:str, default_columns:list, value:str) -> str:
    words = value.split(" ")
    query = " OR ".join([f"({construct_like_value(table_name, column, words)})" for column in default_columns])
    return query


def construct_query_when(query_string:str) -> str:
    table_name = get_database_table_name()
    #FIXME: add below to globals
    default_columns = ['name', 'type_line', 'oracle_text'] # columns that will be searched when there was no argument provided
    query_array = []
    query_elements = split_query(query_string)

    for element in query_elements:
        operator = decide_operator(element)
        try:
            element_array = element.split(operator)
        except ValueError:
            query = handle_query_when_no_operator(table_name, default_columns, query_string)
            return f"WHERE {query}"
            
        argument = element_array[0]
        value = element_array[1]
     
        for translation in QUERY_TRANSLATE:
            translation_commands = translation["query_command"]
            translation_commands_negative = [f"-{element}" for element in translation_commands] #commands found in translation dictionary, but negated
            if argument in translation_commands or argument in translation_commands_negative:
                column_type = translation["type"]

                if column_type not in ["array", "object"]:
                    if len(translation["columns"]) == 1:
                        column_name = translation["columns"][0]
                        if column_type in ["float", "int"]:
                            query = handle_query_when_number(table_name, operator, column_name, value, column_type)
                            query_array.append(query)
                        elif column_type in ["datetime"]:
                            query = handle_query_when_date(table_name, operator, column_name, value, argument)
                            query_array.append(query)
                        else:
                            query = handle_query_when_string(table_name, column_name, value, argument, operator)
                            query_array.append(query)
                    else:
                        if column_type in ["float", "int"]:
                            #TODO: there is no use case right now; might be added later in the development
                            pass
                        elif column_type in ["datetime"]:
                            #TODO: there is no use case right now; might be added later in the development
                            pass
                        else:
                            query = handle_query_when_string_multiple_columns(table_name, translation["columns"], value, argument)
                            query_array.append(query)

                else:
                    column_name = translation["columns"][0]
                    if column_type == "array":
                        if "color" in ",".join(translation["columns"]):
                            query = handle_query_when_color_array(table_name, column_name, value, argument, operator)
                            query_array.append(query)
                        else:
                            query = handle_query_when_string_array(table_name, column_name, value, argument, operator)
                            query_array.append(query)
                    elif column_type == "object":
                        if "prices" in translation["columns"]:
                            query = handle_query_when_object_prices(table_name, column_name, value, argument, operator)
                            query_array.append(query)   

    return f"WHERE {' AND '.join(query_array)}" if query_array else ""


def construct_query(query_string=None):
    table_name = get_database_table_name()
    query = f'SELECT id FROM {table_name} '

    query += construct_query_when(query_string)
    return query