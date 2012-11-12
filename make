#!/usr/bin/env bash

echo -e "\E[31m        !!!! Warning this is custom make script !!!\033[0m"

sleep 1

. ~/.remoterunrc

REL=${PWD#$SYNCROOT}

# check_prefix <prefix> <string>
function check_prefix()
{
	case "$2" in
	$1*) true ;;
	*) false ;;
	esac
}


if check_prefix "/" "$REL"
then	
	echo Running local make
	/usr/bin/make "$@"
else
    rr make -j8  "$@"
fi

