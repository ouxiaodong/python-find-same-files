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

�ű����ܣ��ҳ�ָ��·�����Ƿ����������ȫһ�µ��ļ�
ʹ�÷�ʽ��python tgaduplicates.py ����·��
�����������ǰ����·����duplicates.txt

*********************************
    '''
    print message


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
		f_write.write("�ļ��ظ���" + TAB + "�ļ���С" + TAB + "�ļ���" + CHANCE_LINE)
		for file_name in duplicate_files:
			f_write.write(str(len(file_name)) + TAB)
			f_write.write(str(float(os.path.getsize(file_name[0]) / 1024)) + 'KB' + TAB)
			f_write.write(TAB.join(file_name))
			f_write.write(CHANCE_LINE)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print u'�������󣡣���'
		printUsage()
		sys.exit(0)

	print 'working...'
	duplicates(sys.argv[1])
	print 'work finish!'
