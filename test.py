import re

pattern = r'^89\d{9}$'
string = '89202145699'

match = re.match(pattern, string)
if match:
    print("good")
else:
    print("error")
