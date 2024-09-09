echo -e "\n$*\n"

if [ "$1" == "--o" ] && [ "$3" == "--in_mics" ] && [ "$5" == "--param1" ] && [ "$7" == "--param2" ] && [ "$9" == "--param3" ]; then
    python3 new.py $2 $4 $6 $8 ${10}

else
    echo "FIX INPUTS"
fi

