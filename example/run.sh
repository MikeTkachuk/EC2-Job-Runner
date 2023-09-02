python example/script.py --bucket_name "$1" --run_prefix "$2" || :
cd ~
rm -r "$2"
echo "Removed run dir"
