"""
CS 457 Mongo Clone
"""

import sys

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
    while i < len(string):
        field += string[i]
        i += 1
    return (condition, field[2:].replace(")", ""))

def get_response(cond, fields, data):
    """
    Query response
    """
    for doc in data:
        if 'Age' in doc and doc['Age'] == 20:
            print doc
    print cond, fields

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
