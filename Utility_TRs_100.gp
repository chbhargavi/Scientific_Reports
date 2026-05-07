#set term postscript eps enhanced color blacktext "Helvetica" 35
set term pngcairo enhanced size 1200,800 font "Helvetica,35"
set output "Utility_TRs2.png"
set style data histograms
set style histogram cluster gap 1
set xlabel 'Number of TRs'
set ylabel 'Utility of TRs'
set key autotitle columnheader
set key font ",20"
set key left
#set xrange [-0:*] # Allow Gnuplot to automatically set the range
set yrange [0:160000]
set style fill solid
set boxwidth 0.9 # Set boxwidth to less than 1 to ensure no overlap
#set xtics rotate by -45
set tics font ",30"
#set xrange [-0.5:*] # Adjust to ensure the first bar is fully visible
plot "Utility_TRs.txt" using 2:xtic(1) title "McAfee" lc rgb "#2471A3", \
     "Utility_TRs.txt" using 3 title "MUDA" lc rgb "#E32636", \
     "Utility_TRs.txt" using 4 title "TRUST-SC" lc rgb "#006400",\
     "Utility_TRs.txt" using 5 title "PPM" lc rgb "#0xc04000",\
      #"Utility_TRs.txt" using 6 title "PPM-D" lc rgb "#c8c800",\
