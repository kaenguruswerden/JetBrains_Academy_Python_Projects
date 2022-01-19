import math
import argparse


# user inputs
loan_principal = 0  # int
monthly_payment = 0.0  # float
number_of_payments = 0  # int
loan_interest = 0.0  # float

nominal_interest = 0.0
overpayment = 0


def check_arguments() -> int:
    """ Returns the number of arguments that are not None.
    If a negative value has been entered, return -1."""
    counter = 0
    arguments = [args.type, args.payment, args.principal, args.periods, args.interest]
    for argument in arguments:
        if type(argument) == int and argument < 0:
            return -1
        if argument is not None:
            counter += 1
    return counter


def calculate_number_of_payments(a: float, p: int, i: float) -> int:
    return math.ceil(math.log(a / (a - i * p), 1 + i))


def calculate_annuity_payment(p: int, i: float, n: int) -> int:
    return math.ceil(p * i * pow(1 + i, n) / (pow(1 + i, n) - 1))


def calculate_loan_principal(a: float, i: float, n: int) -> int:
    return a / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1))


def calculate_differentiated_payment(p: int, i: float, n: int) -> list:
    payment_list = []
    for m in range(1, n+1):
        d = p / n + i * (p - (p * (m - 1)) / n)
        payment_list.append(math.ceil(d))
    return payment_list


# Create parser and it's arguments
parser = argparse.ArgumentParser(description="This program calculates the \
                                value based of the provided arguments.")

parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()

# Check for invalid arguments or argument combinations.
# Exit script if parameters incorrect.
if (args.type != "annuity" and args.type != "diff") or \
        (args.type == "diff" and args.payment is not None) or \
        args.interest is None or \
        check_arguments() < 4:
    print("Incorrect parameters")
    exit()

loan_interest = float(args.interest)
nominal_interest = loan_interest / (12 * 100)

if args.type == "annuity":
    if args.principal is None:
        monthly_payment = float(args.payment)
        number_of_payments = int(args.periods)
        loan_principal = calculate_loan_principal(monthly_payment, nominal_interest,
                                                  number_of_payments)
        print(f"Your loan principle = {loan_principal}!")

    elif args.payment is None:
        loan_principal = int(args.principal)
        number_of_payments = int(args.periods)
        monthly_payment = calculate_annuity_payment(loan_principal, nominal_interest,
                                                    number_of_payments)
        print(f"Your monthly payment = {monthly_payment}!")

    elif args.periods is None:
        loan_principal = int(args.principal)
        monthly_payment = float(args.payment)
        number_of_payments = calculate_number_of_payments(monthly_payment,
                                                          loan_principal,
                                                          nominal_interest)
        years = math.floor(number_of_payments / 12)
        months = number_of_payments % 12
        if number_of_payments == 1:
            print("It will take 1 month to repay this loan!")
        elif number_of_payments < 12:
            print(f"It will take {months} months to repay this loan!")
        elif number_of_payments == 12:
            print("It will take 1 year to repay this loan!")
        elif number_of_payments == 13:
            print("It will take 1 year and 1 month to repay this loan!")
        elif number_of_payments < 24:
            print(f"It will take 1 year and {months} months to repay this loan!")
        elif number_of_payments % 12 == 0:
            print(f"It will take {years} years to repay this loan!")
        elif number_of_payments % 12 == 1:
            print(f"It will take {years} years"
                  f" and 1 month to repay this loan!")
        else:
            print(f"It will take {years} years"
                  f" and {months} months to repay this loan!")

    overpayment = monthly_payment * number_of_payments - loan_principal

elif args.type == "diff":
    loan_principal = int(args.principal)
    number_of_payments = int(args.periods)
    list_of_payments = calculate_differentiated_payment(loan_principal,
                                                        nominal_interest,
                                                        number_of_payments)
    for count in range(len(list_of_payments)):
        print(f"Month {count + 1}: payment is {list_of_payments[count]}")
    overpayment = sum(list_of_payments) - loan_principal
    print("")

print(f"Overpayment = {overpayment}")
