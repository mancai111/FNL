echo -e "\n$*\n"

if [ "$1" == "--o" ] && [ "$3" == "--in_mics" ] && [ "$5" == "--param1" ]; then
    python3 bgal_sam2.py $2 $4 $6

else
    echo "FIX INPUTS"
fi

