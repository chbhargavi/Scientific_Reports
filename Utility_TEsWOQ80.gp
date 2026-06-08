#set term postscript eps enhanced color blacktext "Helvetica" 35
set term pngcairo enhanced size 1200,800 font "Helvetica,35"
set output "Utility_TEsWOQ80.png"
set style data histograms
set style histogram cluster gap 1
set xlabel 'Number of TEs'
set ylabel 'Utility of TEs'
set key autotitle columnheader
set key font ",20"
set key left
#set xrange [-0:*] # Allow Gnuplot to automatically set the range
set yrange [0:1200000]
set format y "%.0f"
set style fill solid
set boxwidth 0.9 # Set boxwidth to less than 1 to ensure no overlap
#set xtics rotate by -45
set tics font ",30"
#set xrange [10000:50000] # Adjust to ensure the first bar is fully visible
plot "Utility_TEsWOQ80.txt" using 2:xtic(1) title "McAfee" lc rgb "#2471A3", \
     "Utility_TEsWOQ80.txt" using 3 title "MUDA" lc rgb "#E32636", \
     "Utility_TEsWOQ80.txt" using 4 title "TRUST-SC" lc rgb "#006400",\
       "Utility_TEsWOQ80.txt" using 5 title "PPM" lc rgb "#0xc04000",\
          #"Utility_TEsWOQ80.txt" using 6 title "PPM-D" lc rgb "#c8c800",\
