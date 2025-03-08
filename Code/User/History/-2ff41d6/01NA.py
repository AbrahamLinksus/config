s = "A man, a plan, a canal: Panama"
s = s.split()
string = ""
for i in s:
    if i.isalnum():
        string = string + i.lower()
    else:
        for j in i:
            if j.isalnum():
                string = string + j.lower()
print(string)