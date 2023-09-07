from decimal import ROUND_HALF_UP, Decimal, ROUND_HALF_DOWN
import math

def redondear(num,digitos=2):
    if digitos==0:
        a=num-int(num)
        a=round(a,1)
        a=int(num)+a
        a=round(a)
    else:
        pr=round(num,digitos)
        num_=Decimal(num)
        snum=str(num_)
        if snum.count('9')>10:
            num=round(num_,digitos+1)
        
        a=Decimal(num).quantize(Decimal(str(pr)),rounding=ROUND_HALF_UP)
        
    return float(a)



def reddataframe(df,digitos=0):
    for i in range(0,len(df.columns)):
        for j in range(0,len(df.index)):
            df.iloc[j,i]=redondear(df.iloc[j,i],digitos)
    return df