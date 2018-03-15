import os
import sys
import re


def findindex(words):
	for i in range(len(words)):
		temp = words[len(words)-i-1]
		if(len(temp)>0):
			# print(temp)
			if(temp[0].islower() and str(temp) != 'empty'):
				return len(words)-i-1

	return -1


def converttostr(word1):
	string = ''
	for i in range(len(word1)):
		string += str(word1[i]) + '		'

	return string	


if __name__ == "__main__":
	htmlCode = """
		<!DOCTYPE html>
		<html>
		<head>
		<title> cs335 asgn3 </title>
		<style>
			*{
				margin: 0;
				padding: 0;
			}
			div.rule{
				margin: 10px auto;
				padding: 10px;
				background-color: pink;
				width: 80%;
				word-wrap: break-word;
			}
			div.main{
				background-color: rgba(200,200,200,0.8);
				padding: 10px;
			}
			div.tab{
				margin-left: 10px;
			}
		</style>
		</head>
		<body>
			<div class="main">
			<font color="red">module</font>
			</div>
	"""

	filename = sys.argv[1]
	if os.path.exists(filename):
		file = open(filename, 'r')
		pat1 = re.compile('^Action : Reduce rule \[([^]]+)\] with \[(([^]]|\'\]\')+)\] .*')
		pat2 = re.compile('^Stack  : .*')
		flag = 0
		counter = 0
		for line in file:
			if(flag == 0):
				var1 = pat1.search(line)
				if var1 != None:
					flag = 1
					# print(line)
					# print("found")

			if(flag == 1):
				# print("comes here")
				var2 = pat2.search(line)
				# print("comes here as well")
				if var2 != None:
					# print("found")
					flag = 2
					# print(var2)
					lhs, rhs = line.split(':')
					lhs, rhs = rhs.split('.')
					# print(lhs)
					words = lhs.split(' ')
					# print(words)
					# print(words[6][0])
					kindex = findindex(words)
					# print(kindex)
					# for i in range(len(words)):
						# print(words[len(words)-i-1])
						# temp = words[len(words)-i-1]
						# temp = words[1]
						# print(temp[0])
						# if(len(temp) > 0):
							# print(temp)
							# if(temp[0].islower()):
								# print(temp)
								# kindex = len(words)-i-1
							# else:
								# kindex = -1
					word1 = words[:kindex]
					word2 = words[kindex+1:]
					# print(word2)
					code = '<br></br><div class = "rule"><font>' + var1.group(1) + '</font></div>'
					htmlCode += code
					code = '<br></br><div class = "tab"><font>' + converttostr(word1) + '</font><font color="red">' + converttostr(words[kindex]) + '</font><font>' + converttostr(word2) + '</font></div>'
					htmlCode += code
					counter = 1

			if(flag == 2):
				var3 = pat1.search(line)
				if var3 != None:
					lhs, rhs = var3.group(1).split(' -> ')
					# print(rhs)
					# print(var3.group(1))
					rhs = rhs.split(' ')
					if(str(words[kindex]) == str(lhs)):
						words = word1 + rhs + word2
						# print(words)
						counter += 1
						kindex = findindex(words)
						code = '<br></br><div class = "rule"><font>' + var3.group(1) + '</font></div>'
						htmlCode += code
						if(kindex != -1):
							word1 = words[:kindex]
							word2 = words[kindex+1:]
							if(counter%2 == 0):
								code = '<br></br><div class="main"><font>' + converttostr(word1) + '</font><font color="red">' + converttostr(words[kindex]) + '</font><font>' + converttostr(word2) + '</font></div>'
							else:
								code = '<br></br><div class="tab"><font>' + converttostr(word1) + '</font><font color="red">' + converttostr(words[kindex]) + '</font><font>' + converttostr(word2) + '</font></div>'
							htmlCode += code

						else:
							if(counter%2 == 0):
								code = '<br></br><div class="main"><font>' + converttostr(words) + '</font></div>'
							else:
								code = '<br></br><div class="tab"><font>' + converttostr(words) + '</font></div>'
							htmlCode += code
							break	
						# print(words[kindex])
					# flag = 3				

		htmlCode += '</body></html>'
		file.close()
		try:
			directory = "./"
			with open(directory + "htmlCode.html", 'w') as fs:
				fs.write(htmlCode)
		except:
			print("Cannot write to file!")
			exit(EXIT_FAILURE)				

	else:
		print("no file")	