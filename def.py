from fontTools.varLib.mutator import percents

sum = int(input("Сколько сумма чека?"))



def perc(sum):
    perc20 = sum / 1.20
    perc22 = sum / 1.22
    return perc22, perc20
per20, per22 = perc(sum)
print(f"""сумма = {sum}, 
Процент если 20% НДС {per20}, 
Процент если 22% НДС {per22}""")
