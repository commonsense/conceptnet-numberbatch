#!/bin/bash

# ----------------------------------------------------------------------
# This shell script produces the latex source-package of a paper
# as required by AAAI, in preparation for printed proceedings.
# Copyright (C) 2009 Christian Fritz "fritz at cs dot toronto dot
# edu" For the latest version of this script go to: 
# https://gist.github.com/chfritz/5447483
# ----------------------------------------------------------------------
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# function for recursive processing of style files
recurseStyles() {
    echo "..recursively processing required packages of $1"
    PACKAGES=`grep RequirePackage $1 | sed 's/RequirePackage\[[^]]*\]/RequirePackage/g' | sed 's/.*RequirePackage{\([^}]*\)}.*/\1/' | sed -e 's/, */\n/g'`
    for name in $PACKAGES; do
	if [ ! -e sources/$name.sty ]; then 
	    echo "..locating and copying: $name"
	    FILE=`locate /$name.sty | head -n 1`
	    if [ -e $FILE ]; then
		cp $FILE sources
	    else
		echo "..cannot locate $name.sty"
	    fi
	    if [ -e sources/$name.sty ]; then
		recurseStyles sources/$name.sty
	    fi
	fi
    done
}

#            -------------------------------              

# give a tex file as parameter
if (( $# < 1 )); then
    echo "Error: Please give a tex-file as parameter, e.g., ./aaai_script.sh main.tex";
    exit;
fi;

mkdir sources

echo "locating and copying all used packages"
PACKAGES=`grep ^.usepackage $1 | sed -e 's/.*usepackage{\(.*.\)}.*/\1/' | sed -e 's/, /\n/g'`
for name in $PACKAGES; do
    echo "locating and copying: $name"
    if [ -e $name.sty ]; then
	cp $name.sty sources
    else
	FILE=`locate /$name.sty | head -n 1`
	if [ -e $FILE ]; then
	    cp $FILE sources
	else
	    echo "cannot locate $name.sty"
	fi
    fi
    if [ -e sources/$name.sty ]; then
	recurseStyles sources/$name.sty
    fi
done


echo "inlining all included files"
cp $1 __tmp1
while ( grep ^.input __tmp1 ); do
#     INPUTS=`grep ^.input __tmp1 | sed 's/.*input *{*\([^.}]*\).*/\1/'`
#     cat __tmp1 | sed '/^%.*$/d' >  __tmp2
#     for name in $INPUTS; do
# 	echo "inlining $name"
# 	awk -v filename=$name '{ if ($0 ~ ".input.*"filename) { system("cat "filename".tex | sed  '/^%.*\$/d'"); } else { print $0; } }' < __tmp2 > __tmp1
#     done
    awk '{ if ( $0 ~ /\\input( |{)/ ) { sub(/\\input( |{)/,""); sub(/}/, ""); sub(/\.tex/, ""); system("cat "$0".tex | sed  '/^%.*\$/d'") } else { print $0; } }' __tmp1 > __tmp2
    cp __tmp2 __tmp1
done

echo "inlining bibitems"
BIBFILE=`echo $1 | sed 's/.tex/.bbl/'`
awk -v filename=$BIBFILE '{ if ($0 ~ ".bibliography{") { system("cat "filename); } else { print $0; } }' < __tmp1 > __tmp2
cp __tmp2 sources/full.tex


echo "getting figures"
FIGURES=`grep includegraphics __tmp2 | grep -v ^% | sed 's/.*{\([^}]*\)}*/\1/'`
for name in $FIGURES; do
    echo "getting figure $name"
    mkdir -p sources/`echo "$name" | sed 's/\(.*\)\/.*/\1/'`
    cp $name.*ps sources/`echo "$name" | sed 's/\(.*\)\/.*/\1/'`
done

#            -------------------------------              

cd sources
echo "latexing source"
latex full.tex
echo "latexing source once more"
latex full.tex

echo "creating the PDF using"
dvips -Ppdf -G0 -tletter full -o full.ps
ps2pdf -sPAPERSIZE=letter -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=false -dEmbedAllFonts=true full.ps
cd ..

echo "DONE"
