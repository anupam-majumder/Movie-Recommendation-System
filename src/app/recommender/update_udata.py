import os
def ratings_match(line_list,line_split):
    if(line_list[0]==line_split[0] and line_list[1]==line_split[1]):
        return True
    return False

def remove_duplicate_ratings(towrite):
    str_return = ""
    lines = towrite.split('\n')
    size = len(lines) -1
    for i in range(size):
        match = False
        for j in range(i+1,size):
            if ratings_match(lines[i].split('\t'),lines[j].split('\t')):
                match = True
                break
        if match == False:
            str_return = str_return+lines[i]+'\n'
    return str_return

#edit filepath
filepath = ''
data_file = open(filepath +'u.data','r')
data_file_write = open(filepath +'temp.data','w')
temp_data = open(filepath + 'temp.txt','r')
towrite = temp_data.read()
towrite = remove_duplicate_ratings(towrite)
temp_lines = towrite.split('\n')
data_lines = data_file.readlines() 
data_file_write.write(towrite)
for line1 in data_lines:
    match = False
    for line2 in temp_lines:
        if ratings_match(line1.split('\t'),line2.split('\t')) == True :
            match = True
            break
    if match== False:
        data_file_write.write(line1)
data_file.close()
data_file_write.close()
temp_data.close()

os.remove(filepath+'u.data')
os.remove(filepath+'temp.txt')
f = open(filepath+'temp.txt','a')
f.close()
os.rename(filepath+'temp.data',filepath+'u.data')

