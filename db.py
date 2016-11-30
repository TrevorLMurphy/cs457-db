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
            id_count+=1
    return array

def process_data(data):
    """
    Create array of dictionaries from data
    """
    print data

def process_query(query):
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
                # Do the find operation
                print "You're trying to do find!"
            elif operation.startswith("avg", 0, 3):
                # Do the avg operation
                print "You're trying to do average!"
            else:
                print "That operation is not supported by this program!"
        query = raw_input("query: ")

if __name__ == '__main__':
    DATA = parse_file(sys.argv[1])
    process_data(DATA)
    # query = raw_input("query: ")
    # processQuery(query)
    # print("Exiting...")
