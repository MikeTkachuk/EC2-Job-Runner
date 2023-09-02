cd ~
conda activate foo_env
cd foo
python  || :
cd ~
rm -r checkpoints
rm -r Brawl_iris
echo "Removed repo dir and chkpt"
