num = int(input("ENter a number"))
temp = num
i = 0
d = 0
sum = 0
while temp>0:
    i = i +1
    temp = temp//10
temp = num
while temp>0:
        d = temp%10
        sum = sum + d ** i
        temp = temp//10

if num == sum:
            print("armstrong")
else:
            print("not armstrong")
