import webbrowser

from fpdf import FPDF
#
# John = Flatmate("John", 20)
# Sarah = Flatmate("Sarah",25)
# the_bill = Bill(120, "October")
# print(John.pays(bill=the_bill))


class House:

    def __init__(self):
        self.flatmates = []
        self.size = len(self.flatmates) #constructors are only run once so size attr must be updated elsewhere
        print(self.flatmates)


class Bill:
    """
        Doc String:
        Object that contains data about a bill, such as
        total amount and period of the bill
        """
    def __init__(self, amount, period):
        self.amount = amount
        self.period = period



class FlatMate:
    """
        Creates a flatmate that lives in the house and
        the time they've lived, name, and pays a share of bill
        """
    house = House()
    def __init__(self, name, daysInHouse):
        self.name = name
        self.daysInHouse = daysInHouse
        self.house.flatmates.append(self)

    def pays(self, bill):
        #implement the calculations of the payment for the flatmate
        #amount total = bill.amount
        amount_total = bill.amount
        total_days = 0
        for people in self.house.flatmates:
            total_days += people.daysInHouse

        rate = amount_total / total_days
        personal_amount = rate * self.daysInHouse

        print(personal_amount)
        return personal_amount

class PdfReport:
    """
        Creates a pdf file that contains the names, payments,
        and the period of the bills.
        """
    def __init__(self, filename):
        self.filename = filename

    def generate(self, house_info, bill):
        pdf = FPDF(orientation='P', unit='pt', format='A4')

        pdf.add_page()

        pdf.image("house.png", w=30, h=30)
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt='Billing', border=1, align='C', ln=1)

        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=100, h=40, txt="Period:", border=1)
        pdf.cell(w=150, h=40, txt=bill.period, border=1, ln=1)
        #print("people :", house_info.flatmates[0])

        pdf.set_font(family='Times', size=12, style='B')
        for personal_info in [person for person in house_info.flatmates]:
            print("personal info: ", personal_info.name, personal_info.pays(bill))
            pdf.cell(w=100, h=40, txt=str(personal_info.name), border=1)
            pdf.cell(w=150, h=40, txt=str(round(personal_info.pays(bill), 2)), border=1, ln=1)

        pdf.output(name=self.filename)
        webbrowser.open(self.filename)


bill = Bill(120, "January 2023")

print(bill.amount)

Tim = FlatMate("Timothy", 20)
Sam = FlatMate("Samantha", 25)
Susan = FlatMate("Susan", 10)
# for x in [flatmates for flatmates in apt.flatmates]:
#     print(x.name)

Susan.pays(bill)
Sam.pays(bill)
Tim.pays(bill)

#new declaration of house would not have the same information as the one used for each person
#house_info = House()

print("number of people in the house: ", len(Tim.house.flatmates))

pdf = PdfReport("Report1.pdf")
pdf.generate(Tim.house, bill)