
readcol,'testchisq.T1.data',x,y,yerr,ymod,format='D,D,D,D',delimiter='|'

chisq = total(( (y-ymod)/yerr)^2)

print, chisq, N_ELEMENTS(y)

plot, x,y, psym=3, ysty=1
oplot, x,ymod

; plot, x, abs(y-ymod),psym=3
; plot, (y-ymod)^2, yerr^2, psym=4

