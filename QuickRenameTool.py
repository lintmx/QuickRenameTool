#!/usr/bin/env python3

# Author:https://github.com/lintmx
#
# This file is released under General Public License version 3.
# You should have received a copy of General Public License text alongside with
# this program. If not, you can obtain it at http://gnu.org/copyleft/gpl.html .
# This program comes with no warranty, the author will not be responsible for
# any damage or problems caused by this program.

import os
import re
import time

#生成 NumLength 位前面带 0 的数字字符串
def GenerateNum(Num,NumLength):
	Num = str(Num)
	
	while len(Num) < NumLength:
		Num = "0" + Num
	
	return Num

#检查文件名是否符合正则表达式
def CheckFile(Regular,File):
	MatchFile = re.search(Regular,File)
	if MatchFile is not None:
		return True
	else:
		return False

#检查文件名是否已经使用
def CheckName(Num,FileTagName,RightFileName,FileLength,FileExtensionName):
	SerialNum = GenerateNum(Num,FileLength)
	FileName = FileTagName + "-" + SerialNum + "." + FileExtensionName
	if FileName in RightFileName:
		return True
	else:
		return False

def Rename(FilePath,FileTagName,FileExtensionName,FileLength):
	FileNameList = os.listdir(FilePath)								#生成目录下文件列表
	RightFileName = []												#储存符合要求的文件名
	ErrorFileName = []												#储存不符合要求的文件名
	FileSerialNum = 0;												#文件数字编号
	
	#对文件列表进行分类
	for EachFile in FileNameList:
		if CheckFile(FileTagName + '-' + '[0-9]' * FileLength + '\.' + FileExtensionName + "$",EachFile):
			RightFileName.append(EachFile)							#符合要求文件
		elif CheckFile('[\w]+\.' + FileExtensionName + "$",EachFile):
			ErrorFileName.append(EachFile)							#不符合要求文件
		else:
			pass													#其他文件
	
	#对不符合要求文件进行重命名
	for EachFile in ErrorFileName:
		#检查文件名
		while CheckName(FileSerialNum,FileTagName,RightFileName,FileLength,FileExtensionName):
			FileSerialNum += 1
		
		SerialNum = GenerateNum(FileSerialNum,FileLength)
		NewFileName = FileTagName + "-" + SerialNum + "." + FileExtensionName
		
		os.rename(os.path.join(FilePath,EachFile),os.path.join(FilePath,NewFileName))
		FileSerialNum += 1
		
	print("OK!")
	time.sleep(2)

def main():
	#TODO:参数
	FilePath = os.getcwd()											#文件所在目录
	FileTagName = 'Wallpaper'										#文件统一前缀
	FileExtensionName = 'jpg'										#文件拓展名
	FileLength = 3													#序号长度
	
	Rename(FilePath,FileTagName,FileExtensionName,FileLength)		
	
if __name__ == '__main__':
	main()
