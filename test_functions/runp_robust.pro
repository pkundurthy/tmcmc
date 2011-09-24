readcol,'data4mean.txt',x,format='D'
p_robustmm, x, 5, 'median', mm, errmm, sdv, ngood, nrej, goodvec, badvec, /silent
print, 'IDL> 5sig', mm, sdv, ngood, nrej
p_robustmm, x, 3, 'median', mm, errmm, sdv, ngood, nrej, goodvec, badvec, /silent
print, 'IDL> 3sig', mm, sdv, ngood, nrej
p_robustmm, x, 0.9, 'median', mm, errmm, sdv, ngood, nrej, goodvec, badvec, /silent
print, 'IDL> 0.9sig', mm, sdv, ngood, nrej

