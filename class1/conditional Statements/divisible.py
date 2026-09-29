num = (int(input("Enter your number")))
    
if((num%3==0 and num%5==0) or (num%4==0 and num%10==0)):
    print("they are divisible by the following numbers")
else:
     print("not divisible")
