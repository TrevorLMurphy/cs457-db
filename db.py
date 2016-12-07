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
            d = {'ID': str(id_count)}
            keys = line_array[0::2]
            vals = line_array[1::2]
            for i in range(0, len(keys)):
                d[keys[i]] = vals[i]
            array.append(d)
            id_count += 1
    return array

def process_find(string):
    """
    Retrieve the condition and the fields of a find expression
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

    return (condition, field[1:-1])

def process_avg(field):
    """
    Just returns the average argument
    """
    return field[1:-1]

def process_cond(cond):
    """
    A list of conditional statements that have elements that
    are lists that contain the conditional tuples...ugh
    """
    key = ""
    val = ""
    full_cond = []
    key_vals = []
    i = 1
    while i < len(cond):
        if cond[i] == '(':
            if key_vals[-1] == 'or' or key_vals[-1] == 'and':
                full_cond.append(key_vals[0:-1])
                full_cond.append(key_vals[-1])
            key_vals = []
            i += 1
        elif key == 'and' or key == 'or':
            if key_vals:
                key_vals.append(key)
            else:
                full_cond.append(key)
            key = ""
        elif cond[i] == '=' or cond[i] == '<' or cond[i] == '>':
            oper = cond[i]
            if cond[i + 1] == '>':
                oper += cond[i + 1]
                i += 2
            else:
                i += 1
            while cond[i] != ' ' and cond[i] != ')':
                val += cond[i]
                i += 1
            key_vals.append((key, oper, val))
            key = ""
            val = ""
            if cond[i] == ')':
                full_cond.append(key_vals)
                key_vals = []
            i += 1
        else:
            key += cond[i]
            i += 1

    return full_cond

def process_fields(fields):
    """
    Get a list of fields
    """
    field_list = []
    if fields == '[]': # No fields
        return field_list
    else:
        field_list = [s.strip() for s in fields[1:-1].split(',')]
    return field_list

def get_operator(op):
    # This is awesome
    return {
        '=' : operator.eq,
        '<>' : operator.ne,
        '<' : operator.lt,
        '>' : operator.gt
        }[op]

def cast(s):
    try:
        return int(s)
    except ValueError:
        return s

def perform_cond(cond, doc):
    """
    Conditional tuple is in the form:
    (field, conditional_operator, value)
    This function isn't very readable but it's cool
    """
    return cond[0] in doc and get_operator(cond[1])(cast(doc[cond[0]]), cast(cond[2]))

def eval_cond(cond, data):
    """
    Evaluate the inner conditionals
    """
    result = []
    is_and = False
    for elem in cond:
        if elem == 'and':
            is_and = True
        elif elem == 'or':
            is_and = False
        else:
            if is_and:
                result = [doc for doc in result if perform_cond(elem, doc)]
            else:
                for doc in data:
                    if perform_cond(elem, doc) and doc not in result:
                        result.append(doc)
    return result

def outer_join(result1, result2):
    """
    Outer join for OR statements
    """
    for doc in result2:
        if doc not in result1:
            result1.append(doc)
    return result1

def inner_join(result1, result2):
    """
    Inner join for AND statements
    """
    return [doc for doc in result1 if doc in result2]

def find_result(cond, fields, data):
    """
    Query response
    """
    result = []
    i = 0

    while i < len(cond):
        if isinstance(cond[i], list):
            result = eval_cond(cond[i], data)
            i += 1
        else:
            if cond[i] == 'or':
                if result:
                    result = outer_join(result, eval_cond(cond[i + 1], data))
                else:
                    result = outer_join([], eval_cond(cond[i + 1], data))
                i += 2
            else:
                if result:
                    result = inner_join(result, eval_cond(cond[i + 1], data))
                else:
                    result = inner_join([], eval_cond(cond[i + 1], data))
                i += 2

    if not cond:
        # No conditional? Then get ALL the documents
        result = data

    print
    if not fields:
        # Output all the fields
        for doc in result:
            for k, v in doc.items():
                print(k + ": " + str(v)),
            print
    else:
        for doc in result:
            output = ""
            for field in fields:
                if field in doc:
                    output += field + ": " + str(doc[field])
            if output: # Sometimes nothing is returned
                print output
    print

def avg_result(field, data):
    """
    Get the result from average
    """
    count = 0
    my_sum = 0
    for doc in data:
        if field in doc:
            count += 1
            my_sum += int(doc[field])
    print
    if count != 0:
        print my_sum / float(count)
    print

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
                conditions = process_find(query[13:])[0]
                fields = process_find(query[13:])[1]
                cond_list = process_cond(conditions)
                field_list = process_fields(fields)
                find_result(cond_list, field_list, data)
            elif operation.startswith("avg", 0, 3):
                # Do the avg operation
                field = process_avg(query[12:])
                avg_result(field, data)
            else:
                print "\nThat operation is not supported by this program!\n"
        query = raw_input("query: ")

if __name__ == '__main__':
    DATA = parse_file(sys.argv[1])
    QUERY = raw_input("query: ")
    process_query(QUERY, DATA)
    print "Exiting..."
