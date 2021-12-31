#!/bin/python3
import glob
import os
import subprocess

columns = 16
rows = 8
tileWidth = 16
tileHeight = 16

filepathList = list(sorted(glob.glob('./sprites/*.png')))
flairClasses = []
for filepath in filepathList:
	flairClass = os.path.splitext(os.path.basename(filepath))[0]
	# print(flairClass)
	flairClasses.append(flairClass)

# ImageMagick montage
# https://stackoverflow.com/questions/13625798/imagemagick-and-spritesheet
cmd = ['montage']
cmd += filepathList
cmd += ['-tile', '{}x{}'.format(columns, rows)]
cmd += ['-geometry', '{}x{}'.format(tileWidth, tileHeight)]
cmd += ['sprites.png']
# print(' '.join(cmd))
subprocess.run(cmd)

cssRules = []
for i, flairClass in enumerate(flairClasses):
	col = i % columns
	row = i // columns
	x = '0' if i == 0 else str(col * -tileWidth)
	y = '0' if i == 0 else str(row * -tileHeight)
	cssRule = ".flair-" + flairClass + " { "
	cssRule += "background-position: {}px {}px;".format(x, y)
	cssRule += " }"
	cssRules.append(cssRule)

cssRules = sorted(cssRules)

with open('sprites-flair.css', 'w') as fout:
	for cssRule in cssRules:
		print(cssRule)
		fout.write(cssRule + '\n')
