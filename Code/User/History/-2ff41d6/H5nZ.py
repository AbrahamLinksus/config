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
        length = len(string) - 1
        length,counter = length/2,0
        j = -1
        for i in range(length):
            if string[i] == string[j]:
                counter = 0
            else:
                return False
            j -= 1
        return True