set terminal postscript eps enhanced color dashed font "Times-Roman,22"
set output "right_plot.eps"

#set multiplot layout 1,2 title ""
set xlabel "Number of Voters"
set ylabel "Quality Determination Runtime (ms)"
#set xtics font "Times-Roman,14" rotate by 360
#set ytics font "Times-Roman,14"
set xtics font "Times-Roman,24"
set ytics font "Times-Roman,24"
set xlabel font "Times-Roman,26"
set ylabel font "Times-Roman,26"
set xrange [100:1000]
set yrange [0:350]
set grid
#set xtics 100,200,1000
plot "right_plot.dat" using 1:2 with linespoints lt 1 lw 4 pt 5 lc rgb "#556b2f" title ""

#"right_plot.dat" using 1:2 with linespoints lt 1 lw 4 pt 7 lc rgb "#306080" title "Without Quality", \
