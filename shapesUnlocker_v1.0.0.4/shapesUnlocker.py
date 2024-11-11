# 1.0.0.4:
# - added support for fs25
# - fixed `SyntaxWarning: invalid escape sequence '\s'`


import os

os.system('color 0E')

print("===========================")
print("I3D.Shapes Unlocker 1.0.0.4")
print("===========================")

baseDirectory = os.path.dirname(os.path.realpath(__file__)) + '\\shapes\\'

if not os.path.exists(baseDirectory):
	os.makedirs(baseDirectory, exist_ok=True)

count = 0
errorCount = 0

def scanFile(src):
	file = open(src, "r+b")
	array = bytearray(file.read())

	shortPath = src.split(baseDirectory)[1]

	unknownFormat = False

	global count
	global errorCount

	if array[0] == 0x05 or array[0] == 0x07 or array[0] == 0x0A:
		if array[1] == 0x20:
			array[1] = 0x00
			array[2] = changeBytes(array[2])
			array[3] = 0x00

			file.seek(0)
			file.write(array)

			count +=1

			if array[0] == 0x05:
				print('FS17/FS19 .i3d.shapes: "{0}" unlocked!'.format(shortPath))
			elif array[0] == 0x07:
				print('FS22 .i3d.shapes: "{0}" unlocked!'.format(shortPath))
			elif array[0] == 0x0A:
				print('FS25 .i3d.shapes: "{0}" unlocked!'.format(shortPath))
		elif array[1] == 0x00:
			errorCount +=1

			if array[0] == 0x05:
				print('FS17/FS19 .i3d.shapes: "{0}" already unlocked!'.format(shortPath))
			elif array[0] == 0x07:
				print('FS22 .i3d.shapes: "{0}" already unlocked!'.format(shortPath))
			elif array[0] == 0x0A:
				print('FS25 .i3d.shapes: "{0}" already unlocked!'.format(shortPath))
		else:
			unknownFormat = True
	elif array[0] == 0x00 or array[0] == 0x01:
		if array[2] == 0x80:
			array[0] = 0x00
			array[1] = changeBytes(array[1])
			array[2] = 0x00

			file.seek(0)
			file.write(array)

			count +=1

			print('FS15 .i3d.shapes: "{0}" unlocked!'.format(shortPath))
		elif array[2] == 0x00:
			errorCount +=1
			print('FS15 .i3d.shapes: "{0}" already unlocked!'.format(shortPath))
		else:
			unknownFormat = True
	else:
		unknownFormat = True

	if unknownFormat:
		errorCount +=1
		print('Unknown .i3d.shapes format: "{0}"'.format(shortPath))

def changeBytes(num):
	num = num - 0x0D

	if num < 0:
		num = num + 256

	return num

def scanDir(src, subpath):
	srcDir = os.path.join(src, subpath)

	with os.scandir(srcDir) as it:
		for path in it:
			if path.name.endswith('.i3d.shapes'):
				scanFile(os.path.join(srcDir, path.name))
			elif path.is_dir():
				scanDir(src, os.path.join(subpath, path.name))

scanDir(baseDirectory, '')

if count > 0:
	print('Successfully unlocked {0} files.'.format(count))

if errorCount > 0:
	print('Failed to unlock {0} files.'.format(errorCount))

os.system('pause')