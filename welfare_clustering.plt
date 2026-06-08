set terminal postscript eps enhanced color dashed font "Times-Roman,22"
set output "welfare_clustering1.eps"

set border lw 1.5
set grid
set key top left
set xlabel "Number of Voters"
set ylabel "Social welfare"
set yrange [500:1200]  
set xtics font "Times-Roman,24"
set ytics font "Times-Roman,24"
set xlabel font "Times-Roman,26"
set ylabel font "Times-Roman,26"

     plot "welfare_clustering.dat" using 1:2 with linespoints lw 4 pt 5 lc rgb "#ff1493" title "Without clustering", \
     "welfare_clustering.dat" using 1:3 with linespoints lw 4 pt 7 lc rgb "#1a1a1a" title "With clustering"
     
   
