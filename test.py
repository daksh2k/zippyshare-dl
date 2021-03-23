# import sys
# print(f"length of sys arg:  {len(sys.argv) }")
file_list=[]
# for i in range(1,len(sys.argv)):
	# print(f"argument {i}"+sys.argv[i])
	# file_list.append(sys.argv[i])
	# fl+str(i)= arg
# for file in file_list:
# print(file_list)
# for fl in file_list:
 # print("rr")	
file_inputs=input("Enter the name of the file or path(if multiple separete by commas):")
for file in file_inputs.strip().split(','):
	# file_e = file.strip()
	file_list.append(file.strip())
print(file_list)			