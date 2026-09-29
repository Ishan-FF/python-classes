num = int(input("Enter a number"))
rev = 0
temp = num
d = 0

while temp>0:
        d = temp % 10
        rev = rev*10 + d
        temp = temp//10


if(rev == num):
        print("is palindrome")
else:
        print("not palindrome")
