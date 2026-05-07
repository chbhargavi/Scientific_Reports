set term postscript eps enhanced color blacktext "Helvetica" 45
set xlabel 'Number of Agents'
set key autotitle columnheader
set key font "20"
set key left
set xrange [15000:97000]
set yrange [0:16000]
set ytics 2000
set tics font ", 35"
set term post size 8,6
#set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#E5E7E9" behind
set output "running_time3.eps" 
set ylabel 'running time (in millisecond)'
plot "running_time.txt" using 1:2:xtic(1) with lp lc rgb "#2471A3" lt 14 lw 11, \
      "running_time.txt" using 1:3:xtic(1) with lp lc rgb "#E32636" lt 14 lw 11, \
      "running_time.txt" using 1:4:xtic(1) with lp lc rgb "#006400" lt 14 lw 11, \
       "running_time.txt" using 1:5:xtic(1) with lp lc rgb "#0xc04000" lt 14 lw 11, \
    
      
      

