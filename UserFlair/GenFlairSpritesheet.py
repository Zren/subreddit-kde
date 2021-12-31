#!/bin/python3
import glob
import os
import subprocess

columns = 1
rows = 128
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

def genTileBgPos(i):
	col = i % columns
	row = i // columns
	x = '0' if i == 0 else str(col * -tileWidth)
	y = '0' if i == 0 else str(row * -tileHeight)
	return "background-position: {}px {}px;".format(x, y)

cssRules = []
for i, flairClass in enumerate(flairClasses):
	cssRule = ".flair-" + flairClass + " { "
	cssRule += genTileBgPos(i)
	cssRule += " }"
	cssRules.append(cssRule)

stylesheet = ''
cssRules = sorted(cssRules)
for cssRule in cssRules:
	stylesheet += cssRule + '\n'
stylesheet += '\n'

kdedevClasses = [
	{ 'name': 'kdedev', 'sprite': 'kde', 'bg': '#3daee9', },
	{ 'name': 'kdedevchakra', 'sprite': 'chakra', 'bg': '#6b5e9c', },
	{ 'name': 'kdedevsuse', 'sprite': 'opensuse', 'bg': '#007373', },
	{ 'name': 'kdedevkubuntu', 'sprite': 'kubuntu', 'bg': '#4042be', },
	{ 'name': 'kdedevfedora', 'sprite': 'fedora', 'bg': '#014980', },
	{ 'name': 'kdedevredhat', 'sprite': 'redhat', 'bg': '#800016', },
	{ 'name': 'kdedevarch', 'sprite': 'arch', 'bg': '#000a8f', },
	{ 'name': 'kdedevkrita', 'sprite': 'krita', 'bg': '#b02564', },
	{ 'name': 'kdedevkdenlive', 'sprite': 'kdenlive', 'bg': '#004444', },
	{ 'name': 'kdedevkate', 'sprite': 'kate', 'bg': '#196181', },
	{ 'name': 'kdedevkwin', 'sprite': 'kwin', 'bg': '#445560', },
	{ 'name': 'kdedevvdg', 'sprite': 'vdg', 'bg': '#701db5', },
	{ 'name': 'kdedevneochat', 'sprite': 'neochat', 'bg': '#397249', },
]
for kdedev in kdedevClasses:
	flairName = kdedev['name']
	flairSprite = kdedev['sprite']
	flairIndex = flairClasses.index(flairSprite)
	if flairIndex < 0:
		raise Exception("Could not find sprite '{}' for '{}'".format(flairSprite, flairName))

	print(flairName, flairIndex, flairSprite, genTileBgPos(flairIndex))
	cssRule = '.flair-' + flairName + ' {\n'
	cssRule += '    ' + genTileBgPos(flairIndex) + '\n'
	cssRule += '    background-color: {};\n'.format(kdedev['bg'])
	cssRule += '    color: {};\n'.format(kdedev['fg'] if 'border' in kdedev else '#ffffff')
	cssRule += '    border-color: {};\n'.format(kdedev['border'] if 'border' in kdedev else kdedev['bg'])
	cssRule += '}\n'
	stylesheet += cssRule


# print(stylesheet)

with open('sprites-flair.css', 'w') as fout:
	fout.write(stylesheet)
