

summ = int(input("Сумма чека?"))
pr_tia = int(input("Процент чая?"))

def num(summ, pr_tia):
    res = summ * (pr_tia / 100)
    return res

print(f"чек = {num(summ, pr_tia)}")
