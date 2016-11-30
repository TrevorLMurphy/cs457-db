import sys

def parseFile(arg):
    array = []
    with open(arg, 'r') as f:
        for line in f:
            array.append(line.strip('\r\n '))
    return array

def processData(data):
    temp = data[0]
    print(data[0][:5])

def processQuery(query):
    while query != "exit":
        if not query.startswith("db.final.", 0, 9):
            print("\nThere was an error with your syntax...\n")
            print("Your query: " + query)
            print("Queries must begin with: db.final\n")
        else:
            operation = query[9:]
            if operation.startswith("find", 0, 4):
                # Do the find operation
                print("You're trying to do find!")
            elif operation.startswith("avg", 0, 3):
                # Do the avg operation
                print("You're trying to do average!")
            else:
                print("That operation is not supported by this program!")
        query = raw_input("query: ")

if __name__ == '__main__':
    data = parseFile(sys.argv[1])
    processData(data)
    # query = raw_input("query: ")
    # processQuery(query)
    # print("Exiting...")
