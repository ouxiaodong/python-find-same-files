# coding: gbk
import sys
import os
import hashlib
from collections import defaultdict


TAB = '\t'
CHANCE_LINE = '\n'


def printUsage():
    message = u'''
*********************************

脚本功能：找出指定路径下是否存在内容完全一致的文件
使用方式：python tgaduplicates.py 检索路径
产出结果：当前工作路径下duplicates.txt

*********************************
    '''
    print message


# check file content for md5
def md5Checksum(filePath):
	with open(filePath, 'rb') as f_read:
		m = hashlib.md5()
		while True:
			data = f_read.read(1024 * 1024)
			if not data:
				break
			m.update(data)
		return m.hexdigest()


def duplicates(paths, hash=hashlib.sha1):
	md5_dict = defaultdict(list)

	for dirpath, dirnames, filenames in os.walk(paths):
		for filename in filenames:
			full_path = os.path.abspath(os.path.join(dirpath, filename))
			md5_dict[md5Checksum(full_path)].append(full_path)

	duplicate_files = (val for key, val in md5_dict.items() if len(val) > 1)

	with open("duplicates.txt", "w") as res:
		f_write = res
		f_write.write("文件重复数" + TAB + "文件大小" + TAB + "文件名" + CHANCE_LINE)
		for file_name in duplicate_files:
			f_write.write(str(len(file_name)) + TAB)
			f_write.write(str(float(os.path.getsize(file_name[0]) / 1024)) + 'KB' + TAB)
			f_write.write(TAB.join(file_name))
			f_write.write(CHANCE_LINE)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print u'参数有误！！！'
		printUsage()
		sys.exit(0)

	print 'working...'
	duplicates(sys.argv[1])
	print 'work finish!'
