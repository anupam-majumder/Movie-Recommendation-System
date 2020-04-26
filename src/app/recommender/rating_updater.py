def txt_dump(list_of_tuples):

	delimiter = '\t'
	with open('temp.txt', mode='a') as file_handler:
		for _tuple in list_of_tuples:
			user = str(_tuple[0])
			movie = str(_tuple[1])
			rating = str(_tuple[2])
			timestamp = str(_tuple[3])

			file_handler.write(user+delimiter+movie+delimiter+rating+delimiter+timestamp+'\n')
		file_handler.close()

if __name__=="__main__":
	sample_list = [('a', 'b', 'c', 'd'), (1, 2, 3, 4), ('a', 1, 'b', '2')]
	txt_dump(sample_list)

