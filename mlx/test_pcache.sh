date

for i in {1..10}; do
    echo "nop $i"
    ./x_mlx_nopromsaved_censtr.sh    
done

date

for i in {1..10}; do
    echo "p $i"
    ./x_mlx_promsaved_censtr.sh
done

date
