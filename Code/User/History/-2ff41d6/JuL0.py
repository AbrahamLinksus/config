s = "race a car"
s = s.split()
string = ""
for i in s:
    if i.isalnum():
        string = string + i.lower()
    else:
        for j in i:
            if j.isalnum():
                string = string + j.lower()
length = len(string) - 1
length,counter = int(length/2),0
j = -1
for i in range(length):
    if string[i] == string[j]:
        print(string[i],print[string[j]])
        counter = 0
    else:
        print(False)
    j -= 1
print(True)