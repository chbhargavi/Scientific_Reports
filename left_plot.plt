set terminal postscript eps enhanced color dashed font "Times-Roman,22"
set output "left_plot.eps"

set style data histograms
set style histogram cluster gap 2
set style fill solid 0.9 border -1
set boxwidth 0.8

set size ratio 0.8

set xlabel "Number of voters"
set ylabel "Task Success Rate (%)"

set xtics font "Times-Roman,24"
set ytics font "Times-Roman,24"
set xlabel font "Times-Roman,26"
set ylabel font "Times-Roman,26"

set yrange [50:100]
set grid ytics

set key top left
set key font ",22"

plot "left_plot.dat" using 2:xtic(1) title "Without Quality" lc rgb "#306080", \
     "" using 3 title "With Quality" lc rgb "#556b2f"
