import math
import os.path



# print(os.path.exists("../Data/File23.txt"))
#
# file = open("../Data/File.txt","rb")
# print(file)
# file.close()



if __name__ == '__main__':
    dict = {5:'f',3:'s',43:'a',1:'b'}
    newdict = {}
    for key in sorted(dict):
        newdict[key] =dict[key]
    print(newdict)







