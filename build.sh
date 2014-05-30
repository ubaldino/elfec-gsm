#!/bin/bash

BUILD_TARGET=win32

export BUILD_NAME=1.0

#Elfec-1.0-win32
TARGET_DIR=Elfec-${BUILD_NAME}-${BUILD_TARGET}

##Which versions of external programs to use
WIN_PORTABLE_PY_VERSION=2.7.2.1

#############################
# Funcion que verifica las herramientas
# en el sistema
#############################
function checkTool
{
	if [ -z `which $1` ]; then
		echo "The $1 command must be somewhere in your \$PATH."
		echo "Fix your \$PATH or install $2"
		exit 1
	fi
}

function downloadURL
{
	filename=`basename "$1"`
	echo "Checking for $filename"
	if [ ! -f "$filename" ]; then
		echo "Downloading $1"
		curl -L -O "$1"
		if [ $? != 0 ]; then
			echo "Failed to download $1"
			exit 1
		fi
	fi
}

function extract
{
	echo "Extracting $*"
	echo "7z x -y $*" >> log.txt
	7z x -y $* >> log.txt
}


# Change working directory to the directory the script is in
# http://stackoverflow.com/a/246128
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPT_DIR

#checkTool git "git: http://git-scm.com/"
checkTool curl "curl: http://curl.haxx.se/"
checkTool 7z "7zip: http://www.7-zip.org/"
#checkTool mingw32-make "mingw: http://www.mingw.org/"

#############################
# Download all needed files.
#############################

if [ $BUILD_TARGET = "win32" ]; then
	#Get portable python for windows and extract it. (Linux and Mac need to install python themselfs)
	downloadURL http://ftp.nluug.nl/languages/python/portablepython/v2.7/PortablePython_${WIN_PORTABLE_PY_VERSION}.exe
	#downloadURL http://sourceforge.net/projects/pyserial/files/pyserial/2.5/pyserial-2.5.win32.exe
	downloadURL http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.win32.exe
	#downloadURL http://sourceforge.net/projects/pyopengl/files/PyOpenGL/3.0.1/PyOpenGL-3.0.1.win32.exe
	#downloadURL http://sourceforge.net/projects/numpy/files/NumPy/1.6.2/numpy-1.6.2-win32-superpack-python2.7.exe
	#downloadURL http://videocapture.sourceforge.net/VideoCapture-0.9-5.zip
	#downloadURL http://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20120927-git-13f0cd6-win32-static.7z
	downloadURL http://sourceforge.net/projects/comtypes/files/comtypes/0.6.2/comtypes-0.6.2.win32.exe
	#downloadURL http://www.uwe-sieber.de/files/ejectmedia.zip
fi

#############################
# Build the packages
#############################
rm -rf ${TARGET_DIR}
mkdir -p ${TARGET_DIR}

rm -f log.txt
if [ $BUILD_TARGET = "win32" ]; then
	#For windows extract portable python to include it.
	extract PortablePython_${WIN_PORTABLE_PY_VERSION}.exe \$_OUTDIR/App
	extract PortablePython_${WIN_PORTABLE_PY_VERSION}.exe \$_OUTDIR/Lib/site-packages
	extract pyserial-2.7.win32.exe PURELIB
	#extract PyOpenGL-3.0.1.win32.exe PURELIB
	#extract numpy-1.6.2-win32-superpack-python2.7.exe numpy-1.6.2-sse2.exe
	#extract numpy-1.6.2-sse2.exe PLATLIB
	#extract VideoCapture-0.9-5.zip VideoCapture-0.9-5/Python27/DLLs/vidcap.pyd
	#extract ffmpeg-20120927-git-13f0cd6-win32-static.7z ffmpeg-20120927-git-13f0cd6-win32-static/bin/ffmpeg.exe
	#extract ffmpeg-20120927-git-13f0cd6-win32-static.7z ffmpeg-20120927-git-13f0cd6-win32-static/licenses
	#extract comtypes-0.6.2.win32.exe
	#extract ejectmedia.zip Win32

	# -----------------
	mkdir -p ${TARGET_DIR}/python
	mkdir -p ${TARGET_DIR}/Elfec/
	mv \$_OUTDIR/App/* ${TARGET_DIR}/python
	mv \$_OUTDIR/Lib/site-packages/wx* ${TARGET_DIR}/python/Lib/site-packages/
	mv PURELIB/serial ${TARGET_DIR}/python/Lib
	#mv PURELIB/OpenGL ${TARGET_DIR}/python/Lib
	#mv PURELIB/comtypes ${TARGET_DIR}/python/Lib
	#mv PLATLIB/numpy ${TARGET_DIR}/python/Lib
	#cp -r Power/power ${TARGET_DIR}/python/Lib
	#mv VideoCapture-0.9-5/Python27/DLLs/vidcap.pyd ${TARGET_DIR}/python/DLLs
	#mv ffmpeg-20120927-git-13f0cd6-win32-static/bin/ffmpeg.exe ${TARGET_DIR}/Elfec/
	#mv ffmpeg-20120927-git-13f0cd6-win32-static/licenses ${TARGET_DIR}/Elfec/ffmpeg-licenses/
	#mv Win32/EjectMedia.exe ${TARGET_DIR}/Elfec/
	
	#rm -rf Power/
	rm -rf \$_OUTDIR
	rm -rf PURELIB
	rm -rf PLATLIB
	rm -rf VideoCapture-0.9-5
	rm -rf numpy-1.6.2-sse2.exe
	rm -rf ffmpeg-20120927-git-13f0cd6-win32-static

	#Clean up portable python a bit, to keep the package size down.
	rm -rf ${TARGET_DIR}/python/PyScripter.*
	rm -rf ${TARGET_DIR}/python/Doc
	rm -rf ${TARGET_DIR}/python/locale
	rm -rf ${TARGET_DIR}/python/tcl
	rm -rf ${TARGET_DIR}/python/Lib/test
	rm -rf ${TARGET_DIR}/python/Lib/distutils
	rm -rf ${TARGET_DIR}/python/Lib/site-packages/wx-2.8-msw-unicode/wx/tools
	rm -rf ${TARGET_DIR}/python/Lib/site-packages/wx-2.8-msw-unicode/wx/locale
	#Remove the gle files because they require MSVCR71.dll, which is not included. We also don't need gle, so it's safe to remove it.
	rm -rf ${TARGET_DIR}/python/Lib/OpenGL/DLLS/gle*
fi

#add Cura
mkdir -p ${TARGET_DIR}/Elfec
cp -a Elfec/* ${TARGET_DIR}/Elfec
cp -a Elfec/* ${TARGET_DIR}/Elfec
#Add Elfec version file
echo $BUILD_NAME > ${TARGET_DIR}/Elfec/version

#add script files
cp -a scripts/${BUILD_TARGET}/*.bat $TARGET_DIR/
cp -a scripts/${BUILD_TARGET}/drivers/ $TARGET_DIR/

# ---- agregando printrun ----

rm -rf scripts/win32/dist
mv `pwd`/${TARGET_DIR} scripts/win32/dist

#package the result
if [ "$1" = "exe" ]; then
	if [ $BUILD_TARGET = "win32" ]; then
		if [ -f '/c/Program Files (x86)/NSIS/makensis.exe' ]; then
			echo "generando Elfec.exe"
			'/c/Program Files (x86)/NSIS/makensis.exe' 'scripts/win32/installer.nsi' >> log.txt
			echo "Elfec.exe  generado"
		fi
	fi
else
	echo "Elfec compilado"
fi