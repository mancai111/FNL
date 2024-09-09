echo -e "\n$*\n"

if [ "$1" == "--o" ] && [ "$3" == "--in_mics" ] && [ "$5" == "--param1" ]; then
    python3 new_copy.py $2 $4 $6

else
    echo "FIX INPUTS"
fi

