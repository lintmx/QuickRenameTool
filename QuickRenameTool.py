#!/usr/bin/env python3
#coding:utf-8

# Author:https://github.com/lintmx
#
# This file is released under General Public License version 3.
# You should have received a copy of General Public License text alongside with
# this program. If not, you can obtain it at http://gnu.org/copyleft/gpl.html .
# This program comes with no warranty, the author will not be responsible for
# any damage or problems caused by this program.

import os
import re
import sys
import random
import argparse

def CheckFile(FileName,FileType,Regular = ''):
	FileName,FileExt = os.path.splitext(FileName)
	
	if FileExt[1:].lower() not in FileType:
		return False
		
	if Regular != '':
		MatchFile = re.match(Regular,FileName)
		if MatchFile is not None:
			return False
		
	return True

def GenSeqStr(Num,Length):
	Num = str(Num)
	
	while len(Num) < Length:
		Num = '0' + Num
		
	return Num

def returnStaticNode(duration,FilePath):
	return '\t<static>\n\t\t<duration>' + str(duration) + '</duration>\n\t\t<file>' + str(FilePath) + '</file>\n\t</static>\n'
    
def returnTransitionNode(duration,FromFile,ToFile):
	return '\t<transition>\n\t\t<duration>' + str(duration) + '</duration>\n\t\t<from>' + str(FromFile) + '</from>\n\t\t<to>' + str(ToFile) + '</to>\n\t</transition>\n'
    
def QuickRename(FilePath,FileTagName,FileType,SeqLength,isRandom,isXml):
	FileList = os.listdir(FilePath)
	WorkList = []
	CheckList = []
	
	if isRandom:
		RandomNumList = random.sample(range(len(FileList)),len(FileList))
		
		for EachFile,RandomNum in zip(FileList,RandomNumList):
			if CheckFile(EachFile,FileType):
				RandomFileName = 'This-is-a-meanningless-string-' + str(RandomNum) + os.path.splitext(EachFile)[1]
				WorkList.append(RandomFileName)
				os.rename(os.path.join(FilePath,EachFile),os.path.join(FilePath,RandomFileName))
	else:
		for EachFile in FileList:
			if CheckFile(EachFile,FileType,'^' + FileTagName + '-[0-9]{' + str(SeqLength) + '}$'):
				WorkList.append(EachFile)
			else:
				CheckList.append(os.path.splitext(EachFile)[0])
				
	SeqNum = 0
	
	for EachFile in WorkList:
		while True:
			NewName = FileTagName + '-' + GenSeqStr(SeqNum,SeqLength)
			SeqNum += 1
			if NewName not in CheckList:
				break
		
		os.rename(os.path.join(FilePath,EachFile),os.path.join(FilePath,NewName + os.path.splitext(EachFile)[1].lower()))	
        
	if isXml:
		FileList = os.listdir(FilePath)
		WorkList = []
		KeepTime = 60
		ChangeTime = 0
		XmlFileContent = '''<background>
	<starttime>
		<year>1995</year>
		<month>11</month>
		<day>07</day>
		<hour>00</hour>
		<minute>00</minute>
		<second>00</second>
	</starttime>\n'''
		for EachFile in FileList:
			if CheckFile(EachFile,FileType):
				WorkList.append(EachFile)

		if (len(WorkList) > 1):
			for i in range(len(WorkList) - 1):
				XmlFileContent += returnStaticNode(KeepTime,os.path.join(FilePath,WorkList[i])) + returnTransitionNode(ChangeTime,os.path.join(FilePath,WorkList[i]),os.path.join(FilePath,WorkList[i + 1]))

			XmlFileContent += returnStaticNode(KeepTime,os.path.join(FilePath,WorkList[len(WorkList) - 1])) + returnTransitionNode(ChangeTime,os.path.join(FilePath,WorkList[len(WorkList) - 1]),os.path.join(FilePath,WorkList[0])) + '</background>'

			XmlF = open(os.path.join(FilePath,FileTagName + '.xml'),'w')
			XmlF.write(XmlFileContent)
			XmlF.close

def main():
	parser = argparse.ArgumentParser(description = 'A tool to quickly rename.')
	parser.add_argument('-p','--path',help = 'File Directory.',default = os.getcwd())
	parser.add_argument('-t','--tag',help = 'Filename Identifier.',default = 'Wallpapers')
	parser.add_argument('-f','--filetype',help = 'Filename Extension.',nargs = '*',default = ['jpg','png'])
	parser.add_argument('-l','--length',help = 'The length of Sequence.',type = int,default = '3')
	parser.add_argument('-r','--random',help = 'Whether random file.',action = 'store_true')
	parser.add_argument('-x','--xml',help = 'Create Ubuntu Wallpaper XML file.',action = 'store_true')
	args = parser.parse_args()
	
	# Check Directory
	if not os.path.exists(args.path):
		raise ValueError('Directory does not exist.')
	
	# Check Sequence
	if args.length <= 0:
		raise ValueError('The length of sequence must greater than zero.')
	elif args.length < len(str(len(os.listdir(args.path)))):
		raise ValueError('The length of sequence must greater than file.')
		
	QuickRename(args.path,args.tag,args.filetype,args.length,args.random,args.xml)

if __name__ == '__main__':
	main()
