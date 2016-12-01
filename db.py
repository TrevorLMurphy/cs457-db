"""
CS 457 Mongo Clone
"""

import sys
import operator

def parse_file(arg):
    """
    Read the file
    """
    array = []
    with open(arg, 'r') as f:
        id_count = 0
        for line in f:
            line_array = line.strip('\r\n ').replace(":", "").split(" ")
            d = {'id': id_count}
            keys = line_array[0::2]
            vals = line_array[1::2]
            for i in range(0, len(keys)):
                d[keys[i]] = vals[i]
            array.append(d)
            id_count += 1
    return array

def get_condition_and_field(string):
    """
    Retrieve the condition and the fields
    """
    condition = ""
    field = ""
    i = 1
    while string[i] != ",":
        condition += string[i]
        i += 1

    if string[i + 1] == " ": # Skip a space if needed
        i += 1

    while i < len(string):
        field += string[i]
        i += 1
    return (condition, field[1:].replace(")", ""))

def process_cond(cond):
    key = ""
    val = ""
    key_vals = []
    i = 1
    while i < len(cond):
        if key == 'and' or key == 'or':
            key_vals.append(key)
            key = ""
            i += 1
        elif cond[i] == '=' or cond[i] == '<' or cond[i] == '>' or cond[i] == '!':
            oper = cond[i]
            if cond[i+1] == '=':
                oper += cond[i + 1]
                i += 2
            else:
                i += 1
            while cond[i] != " " and cond[i] != ')':
                val += cond[i]
                i += 1
            key_vals.append((key, oper, val))
            key = ""
            val = ""
            i += 1
        else:
            key += cond[i]
            i += 1
    return key_vals

def get_operator(op):
    return {
        '=' : operator.eq,
        '!=' : operator.ne,
        '<' : operator.lt,
        '<=' : operator.le,
        '>' : operator.gt,
        '>=' : operator.ge
        }[op]

def perform_cond(cond, doc):
    return cond[0] in doc and get_operator(cond[1])(doc[cond[0]], cond[2])

def get_response(cond, fields, data):
    """
    Query response
    """
    conditions = process_cond(cond)
    result = []
    is_and = False
    is_or = False
    for elem in conditions:
        if elem == 'and':
            is_and = True
            is_or = False
        elif elem == 'or':
            is_and = False
            is_or = True
        else:
            if is_and:
                result = [doc for doc in result if perform_cond(elem, doc)]
            else:
                for doc in data:
                    if perform_cond(elem, doc) and doc not in result:
                        result.append(doc)

    for doc in result:
        print doc

def process_query(query, data):
    """
    Make sense of the query
    """
    while query != "exit":
        if not query.startswith("db.final.", 0, 9):
            print "\nThere was an error with your syntax...\n"
            print "Your query: " + query
            print "Queries must begin with: db.final\n"
        else:
            operation = query[9:]
            if operation.startswith("find", 0, 4):
                condition = get_condition_and_field(query[13:])[0]
                fields = get_condition_and_field(query[13:])[1]
                get_response(condition, fields, data)
                print "You're trying to do find!"
            elif operation.startswith("avg", 0, 3):
                # Do the avg operation
                print query[12:]
                print "You're trying to do average!"
            else:
                print "That operation is not supported by this program!"
        query = raw_input("query: ")

if __name__ == '__main__':
    DATA = parse_file(sys.argv[1])
    # process_data(DATA)
    QUERY = raw_input("query: ")
    process_query(QUERY, DATA)
    print "Exiting..."
