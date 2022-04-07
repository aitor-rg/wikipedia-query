#!/bin/bash

p=2
input=""

bold=$(tput bold)
normal=$(tput sgr0)

usage()
{
	echo "Usage: ${bold}search${normal} SEARCH WORDS"
	echo "or:    ${bold}search${normal} SEARCH WORDS [OPTIONS..]"
	echo
	echo "Optional parameters:"
	echo " -p, --parag=2          number of paragraphs to be shown"
}

contains()
{
	seek=$1
	array=("${@:2:${#@}-1}")
	c=0
	for arg in "${array[@]}"
        do
	        if [ "$seek" == "$arg" ]
                then
			c=1
                fi
        done
	echo $c
}

options=("-p" "--parag" "-h" "--help")

#if no arguments given, suggest to use help
if [ "$1" == "" ]; then	echo "Type [search -h] to see usage"; exit 1; fi

#take the input arguments
while [ "$1" != "" ]
do
	#check if some option has been introduced first
	contained=$(contains "$1" "${options[@]}")

	#if no option given first, then $1 refers to a search word
	if [ $contained == 0 ]
	then
		input=${input}"${1,,}"_
	fi

	#check option introduced, if any
	case $1 in
		-p | --parag )
			shift
			p=$((${1}))
			;;
		-h | --help )
			usage
			exit
	esac
	shift
done

input=${input^}
input=${input:0:${#input}-1}

page="https://en.wikipedia.org/wiki/$input"

echo
echo "${bold}Wikipedia search for${normal} $input $page"
echo

content="$(curl -s $page)"

echo $content >> /tmp/search.txt
python3 ./process_search_request.py -f /tmp/search.txt -p $p
rm /tmp/search.txt
