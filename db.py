import sys

def parseFile(arg):
    array = []
    with open(arg, 'r') as f:
        for line in f:
            array.append(line.strip('\r\n '))
    return array

if __name__ == '__main__':
    data = parseFile(sys.argv[1])
    while True:
        query = raw_input("query: ")
        print(query)
