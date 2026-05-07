set terminal postscript eps enhanced color dashed font "Times-Roman,22"
set output "cluster_runtime1.eps"

set border lw 1.5
set grid
set key off
set xlabel "Number of executors"
set ylabel "Clustering time (ms)"
set xtics font "Times-Roman,24"
set ytics font "Times-Roman,24"
set xlabel font "Times-Roman,26"
set ylabel font "Times-Roman,26"

plot "cluster_runtime.dat" using 1:2 with linespoints lw 4 pt 7 lc rgb "#ff1493" title ""


   
