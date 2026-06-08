             
set term postscript eps enhanced color blacktext "Helvetica" 45 size 8,6
set output "Payment_exWOQ80.eps"
set xlabel 'Task Executors'
set ylabel 'Total Payment'
set key autotitle columnheader
set key font "7"
set key left
set xrange [0:60000]
set yrange [0:1500000]
set format y "%.0f"
set tics font ",35"
plot "Payment_exWOQ80.txt" using 1:2:xtic(1) with lp lc rgb "#2471A3" lt 14 lw 5.5, \
     "Payment_exWOQ80.txt" using 1:3:xtic(1) with lp lc rgb "#E32636" lt 14 lw 5.5, \
     "Payment_exWOQ80.txt" using 1:4:xtic(1) with lp lc rgb "#006400" lt 14 lw 5.5, \
     "Payment_exWOQ80.txt" using 1:5:xtic(1) with lp lc rgb "#0xc04000" lt 14 lw 5.5
 
