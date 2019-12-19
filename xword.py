import copy,time
import multiprocessing as mp
import random

words = ["isle","barra","jura","mull","harris","benbecula","north","uist","south","uist","cullins","islay","eigg","lewis","muck","caledonian","macbrayne","iona","staffa","coll","tiree","canna","south","uist","colonsay","scalpay","raasay","rona"]

#words = ["isle","barra","jura","mull","harris","benbecula","north","uist","south","uist","cullins"]

#words = {"LIGHTMEAL","UNRAVEL","CREW","COERCED","CLOUDCUC","AGGRIEVE","STOVE","REPLACED"}
#words = {"LIGHTMEAL","UNRAVEL","CREW","COERCED","CLOUDCUC","AGGRIEVE"}

puzzle = {}

maxcache = 1E6

def fitfunc(puzzle,words,quality,level,checksum):
	global bestquality
	global csumcache
	#Try all remaining words
	for w,word in enumerate(words):
		fitmask = [False]*len(word)
		if level < 17:
			print("{}Placing word {} at level {} with checksum {} at {}".format(' '*level,w,level,checksum,time.strftime("%a, %d %b %Y %H:%M:%S")))
		#Try every letter of word
		for i,letteri in enumerate(word):
			#Try fitting at every existing place
			for loc,place in puzzle.items():
				#Skip if letter doesn't match existing
				if place[0] != letteri:
					continue
				#Skip if already words crossing here
				if place[1] and place[2]:
					continue
				#Try word vertically
				elif place[1]:
					#Check space before word is clear
					if (loc[0],loc[1]-i-1) in puzzle:
						continue
					#Check space after word is clear
					if (loc[0],loc[1]+len(word)-i) in puzzle:
						continue
					#Check every letter can be placed
					newchecksum = checksum
					wordOK = True
					for j,letterj in enumerate(word):
						testloc = (loc[0],loc[1]-i+j)
						newchecksum += testloc[0] + testloc[1]*1000 + ord(letterj)*1000000
						#Is there already a letter here?
						if testloc in puzzle:
							#Does the letter match and is it not from a vertical word?
							if puzzle[testloc][0] != letterj or puzzle[testloc][2]:
								wordOK = False
								break
							fitmask[j] = True
						#No letter already here
						else:
							fitmask[j] = False
							#Is there any letter either side?
							if (loc[0]+1,loc[1]-i+j) in puzzle or (loc[0]-1,loc[1]-i+j) in puzzle:
								wordOK = False
								break
				
					#Did the word fit and was it a new solution?
					if wordOK and newchecksum not in csumcache[level]:
						if len(csumcache[level]) > maxcache:
							csumcache[level] = {newchecksum}
						else:
							csumcache[level].add(newchecksum)
						#Copy the puzzle
						newpuzzle = copy.copy(puzzle)
						newquality = list(quality)
						#Add the word
						for j,letterj in enumerate(word):
							newloc = (loc[0],loc[1]-i+j)
							if newloc in newpuzzle:
								newquality[0] += 1
								newpuzzle[newloc] = (letterj,True,True)
							else:
								newpuzzle[newloc] = (letterj,False,True)
						#Update vertical dimensions
						newquality[4] = min(newquality[4],loc[1]-i)
						newquality[5] = max(newquality[5],loc[1]-i+len(word)-1)
						newquality[1] = newquality[2]-newquality[3]+newquality[4]-newquality[5]
						newquality = tuple(newquality)
						#Copy the words
						newwords = copy.copy(words)
						newwords.remove(word)
						#Recurse!
						if len(newwords):
							fitfunc(newpuzzle,newwords,newquality,level+1,newchecksum)
						elif newquality > bestquality:
							print("Solution with quality {} at {}".format(newquality,time.strftime("%a, %d %b %Y %H:%M:%S")))
							bestquality = newquality
							printpuzzle(newpuzzle)
							
				#Try the word horizontally
				else:
					#Check space before word is clear
					if (loc[0]-i-1,loc[1]) in puzzle:
						continue
					#Check space after word is clear
					if (loc[0]+len(word)-i,loc[1]) in puzzle:
						continue
					#Check every letter can be placed
					newchecksum = checksum
					wordOK = True
					for j,letterj in enumerate(word):
						testloc = (loc[0]-i+j,loc[1])
						newchecksum += testloc[0] + testloc[1]*1000 + ord(letterj)*1000000
						#Is there already a letter here?
						if testloc in puzzle:
							#Does the letter match and is it not from a vertical word?
							if puzzle[testloc][0] != letterj or puzzle[testloc][1]:
								wordOK = False
								break
							fitmask[j] = True
						#No letter already here
						else:
							fitmask[j] = False
							#Is there any letter either side?
							if (loc[0]-i+j,loc[1]+1) in puzzle or (loc[0]-i+j,loc[1]-1) in puzzle:
								wordOK = False
								break
				
					#Did the word fit and was it a new solution?
					if wordOK and newchecksum not in csumcache[level]:
						if len(csumcache[level]) > maxcache:
							csumcache[level] = {newchecksum}
						else:
							csumcache[level].add(newchecksum)
						#Copy the puzzle
						newpuzzle = copy.copy(puzzle)
						newquality = list(quality)
						#Add the word
						for j,letterj in enumerate(word):
							newloc = (loc[0]-i+j,loc[1])
							if newloc in newpuzzle:
								newquality[0] += 1
								newpuzzle[newloc] = (letterj,True,True)
							else:
								newpuzzle[newloc] = (letterj,True,False)
						#Update horizontal dimensions
						newquality[2] = min(newquality[2],loc[0]-i)
						newquality[3] = max(newquality[3],loc[0]-i+len(word)-1)
						newquality[1] = newquality[2]-newquality[3]+newquality[4]-newquality[5]
						newquality = tuple(newquality)
						#Copy the words
						newwords = copy.copy(words)
						newwords.remove(word)
						#Recurse!
						if len(newwords):
							fitfunc(newpuzzle,newwords,newquality,level+1,newchecksum)
						elif newquality > bestquality:
							print("Solution with quality {} at {}".format(newquality,time.strftime("%a, %d %b %Y %H:%M:%S")))
							bestquality = newquality
							printpuzzle(newpuzzle)
							
def printpuzzle(puzzle):
	minx = min([x[0] for x in puzzle.keys()])
	maxx = max([x[0] for x in puzzle.keys()]) + 1
	miny = min([x[1] for x in puzzle.keys()])
	maxy = max([x[1] for x in puzzle.keys()]) + 1
	
	for i in range(miny,maxy):
		print(''.join([puzzle[(j,i)][0] if (j,i) in puzzle else ' ' for j in range(minx,maxx)]))
	print('')
	
csumcache = [set()]*len(words)

random.shuffle(words)
	
#Place first word
starttime = time.time()
word = words.pop()
bestquality = (0,-(len(word)-1),0,len(word)-1,0,0)
for i,letter in enumerate(word):
	puzzle[(i,0)] = (letter,True,False)
if len(words):
	fitfunc(puzzle,words,bestquality,0,0)
else:
	printpuzzle(puzzle)
print(time.time()-starttime)
	
