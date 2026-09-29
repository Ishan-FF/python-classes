
age = int(input("Enter age: "))
student = input("Are you a student? (yes/no): ").lower()

price = 200.0

# Age-based discount
if age < 12:
  price = price * 0.50  # 50% discount


if student == "yes":
  price = price * 0.80  # 20% discount

print(f"Final ticket amount: ₹{price}")