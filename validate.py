class Validate:
    def __init__(self):
        

    def validate_string(val):
       if val != None:
            if type(val) is int:
                #for x in val:
                #   print(x)
                return str(val).encode('utf-8')
            else:
                return val

    def validate_int(val):
       if val != None:
            if type(val) is str:
                #for x in val:
                #   print(x)
                return int(val).encode('utf-8')
            else:
                return val