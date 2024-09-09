echo -e "\n$*\n"
echo -e "\n$1 $3 $5 $7 $9\n"
echo -e "\n$2 $4 $6 $8 ${10}\n"
if [ "$1" == "--o" ] && [ "$3" == "--in_mics" ] && [ "$5" == "--in_coords" ] && [ "$7" == "--param1" ] && [ "$9" == "--param2" ]; then
    python3 curate_picks.py $2 $4 $6 $8 ${10}
else
    echo "Only inputs should be micrographs, coordinates, params1, param2"
fi

