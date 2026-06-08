set terminal postscript eps enhanced color dashed font "Times-Roman,22"
set output "Quality_Executors2.eps"

set style data histograms
set style histogram cluster gap 2   
set style fill solid 0.9 border -1 
set boxwidth 0.8

set size ratio 0.8
         

set xlabel "Tasks"
set ylabel "Number of Voters"

set key autotitle columnhead
set key font ",30"
set key right

set xrange [-0.5:4.5]
set yrange [2500:60000]

set xtics rotate by 0
set tics font ",25"

set grid ytics lw 1 lc rgb "black"

plot "Quality_Executors.txt" using 2:xtic(1) lc rgb "#000080", \
     "" using 3 lc rgb "#8b0000"
