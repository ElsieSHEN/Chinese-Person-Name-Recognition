import os
import re
import xlrd
import thulac

def isChinese(str):
	for char in str:
		if (char < '\u4e00' or  char > '\u9fa5'):
			return False
	return True

# step 1
def clean_np(path):
	thu = thulac.thulac()
	np_list = []

	# construct a dictionary with surnames
	workbook = xlrd.open_workbook('Chinese_Family_Name(1k).xlsx') # surname
	table = workbook.sheet_by_index(0)
	surname = {}

	for i in range(1, 1000):
		surname[table.row_values(i)[0]] = table.row_values(i)[1]


	# fpathe: path
	# dirs: a list of directories it has
	# fs: files in path
	for fpathe, dirs, fs in os.walk(path):		
		for f in fs:
			np_list.append('\n' + f)
			with open(os.path.join(fpathe, f), encoding='utf-8') as record:
				for line in record.readlines():
					text = thu.cut(line, text = True)
					print(text)
					text = text.split(' ')
					print(text)
					for word in text:
						if word != '':
							if word.split('_')[1] == 'np':
								name = word.split('_')[0]
								name = name.strip()
								if isChinese(name) and ((name[0] in surname and len(name) < 4) or ((name[0]+name[1]) in surname)):
									np_list.append(name)
									line = line.replace(name, 'X'*len(name))
									with open(os.path.join(fpathe, f), "w", encoding='utf-8') as new:
										new.write(line)
				record.close()


	# these steps can be ignored for just cleaning purpose
	f = open('np_naive.txt', 'w', encoding='utf-8')

	for name in np_list:	
		f.write(name + '\n') # write the name of patients into file

	f.close()

root = input("Input your directory path: ")
root = root.encode("utf-8")
print("The program is processing your files in ", root)
clean_np(root)
print("Name recognition and cleaning finish.")