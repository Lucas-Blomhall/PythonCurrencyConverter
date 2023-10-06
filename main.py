import requests
import json
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv
load_dotenv()
import logging

class CurrencyConverter(tk.Tk):
    def __init__(self, balance: int):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("300x200")
        self._balance = balance

        self.convert_from_usd_ccwindow_any_to_any = None
        self.convert_from_usd_ccwindow = None
        self.text_widget = None
        self.convert_from_usd_ccwindow_any_to_any = None
        self.convert_from_usd_ccwindow = None
        self.back_button_convert_any = None

        try:
            self._allcurrenciesdata = self.load_currency_data()
        except:
            self._allcurrenciesdata = self.fetch_currency_data()
            logging.basicConfig(format='%(asctime)s %(message)s')
            logging.warning('We are updating the data in the openexchangerates.json file from the api.')

    def fetch_currency_data(self):
        logging.info('Starting: fetch_currency_data')
        api_key = os.environ.get("API_KEY")
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        headers = {"accept": "application/json"} 
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        file = open("openexchangerates.json","w")
        json.dump(data, file)
        return data
    
    def convert_from_usd(self, to_currency: str, amount: int):
        def clear_screen_convert():
            convert_from_usd_ccwindow.pack_forget()
            text_widget.pack_forget()
            convert_from_usd_ccwindow_display.pack_forget()
            convert_from_usd_ccwindow_any_to_any.pack_forget()
            convert_from_usd_ccwindow.pack_forget()
            back_button_convert.pack_forget()
            go_back_to_main()
        hide_main_menu()
        display_currency_converter()
        logging.info('Starting: convert_from_usd')  
        api_key = os.environ.get("API_KEY")
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        headers = {"accept": "application/json"} 
        response = requests.get(url, headers=headers)
        alldata = response.json()
        value = alldata["rates"][to_currency]
        valuenumber = float(value)
        convert_from_usd_ccwindow_display = tk.Label(text=f"Your choosen currency {to_currency} has a value of {valuenumber} on USD as base!")
        convert_from_usd_ccwindow_display.pack()
        newamount = amount * valuenumber
        intamount = int(newamount)
        convert_from_usd_ccwindow = tk.Label(text=f"Your new amount is {intamount}")
        convert_from_usd_ccwindow.pack()
        back_button_convert = tk.Button(root, text="Clear and go back", command=clear_screen_convert, **button_style)
        back_button_convert.pack()
    
    def list_currencies(self):
        logging.info('Starting: list_currencies')  
        with open('openexchangerates.json', 'r') as file:
            data = json.load(file)
            allcurrencies = data["rates"]
            sort_data = sorted(allcurrencies.keys())
            count = 0
            line = ""
            for currency in sort_data:
                line += currency + ", "
                count += 1
                if count % 5 == 0:
                    text_widget.insert(tk.END, line + "\n")
                    line = ""
            if line:
                text_widget.insert(tk.END, line)
            text_widget.pack(pady=10, padx=10)
        
    def convert_any_currency(self, first_to_currency, last_to_currency, amount):
        def clear_screen_convert_any():
            text_widget.pack_forget()
            convert_from_usd_ccwindow_any_to_any.pack_forget()
            convert_from_usd_ccwindow.pack_forget()
            back_button_convert_any.pack_forget()
            go_back_to_main()
        
        logging.info('Starting: convert_any_currency')  
        with open('openexchangerates.json', 'r') as file:
            data = json.load(file)
            first_value = data["rates"][first_to_currency]
            last_value = data["rates"][last_to_currency]
            first_value_number = float(first_value)
            last_value_number = float(last_value)

            print(f"Your choosen currency {first_to_currency} has a value of {first_value_number} in {first_to_currency} on as base!")
            
            try:
                usd_base_value_1_to_any = 1 / first_value
            except:
                logging.warning('Could not convert to the currency!')

            usd_base_value_to_any = amount * usd_base_value_1_to_any
            newamount = usd_base_value_to_any * last_value_number
            intamount = int(newamount)

            convert_from_usd_ccwindow_any_to_any = tk.Label(text=f"Your new amount is {intamount}")
            convert_from_usd_ccwindow_any_to_any.pack()

            back_button_convert_any = tk.Button(root, text="Clear and go back", command=clear_screen_convert_any, **button_style)
            back_button_convert_any.pack()

            
        

    def load_currency_data(self):
        logging.info('Starting: load_currency_data')
        with open('openexchangerates.json', 'r') as file:
            data = json.load(file)
        return data

    def export_to_json(self):
        with open("openexchangerates.json", "w") as file:
            json.dump(self._allcurrenciesdata, file)
        print("Exported")
  
def hide_main_menu():
    entry.pack_forget()
    CCwindow0.pack_forget()
    CCwindow1.pack_forget()
    CCwindow2.pack_forget()
    CCwindow3.pack_forget()
    CCwindow4.pack_forget()
    button.pack_forget()
    result_label.pack_forget()
    
def clear_screen():
    convert_from_usd_ccwindow.pack_forget()
    text_widget.pack_forget()
    convert_from_usd_ccwindow_any_to_any.pack_forget()
    convert_from_usd_ccwindow.pack_forget()

def display_main_menu():
    entry.pack(pady=10)
    CCwindow0.pack(pady=5)
    CCwindow1.pack(pady=5)
    CCwindow2.pack(pady=5)
    CCwindow3.pack(pady=5)
    CCwindow4.pack(pady=5)
    button.pack(pady=10)
    result_label.pack(pady=10)

def hide_currency_converter():
    input_for_currencywindow0.pack_forget()
    input_for_currency.pack_forget()
    input_for_currencywindow1.pack_forget()
    input_amount.pack_forget()
    button_convert.pack_forget()

def go_back_to_main():
    hide_currency_converter()
    hide_currency_converter_any_to_any()
    display_main_menu()

def currency_amount_any_to_any():
    first_to_currency_value = first_convert_any_currency.get()
    last_to_currency_value = last_convert_any_currency.get()
    try:
        amount_value = int(input_amount_any_to_any.get())
        User1.convert_any_currency(first_to_currency=first_to_currency_value, last_to_currency = last_to_currency_value, amount=amount_value)
        result_var.set(f"Converted {amount_value} {first_to_currency_value} to {last_to_currency_value}.")
    except ValueError:
        result_var.set("Invalid amount!")
    go_back_to_main()

def currency_amount():
    logging.info('Starting: currency_amount')
    to_currency_value = input_for_currency.get()
    try:
        amount_value = int(input_amount.get())
        User1.convert_from_usd(to_currency=to_currency_value, amount=amount_value)
        result_var.set(f"Converted {amount_value} USD to {to_currency_value}.")
    except ValueError:
        result_var.set("Invalid amount!")
    
def display_currency_converter():
    input_for_currencywindow0.pack()
    input_for_currency.pack()
    input_for_currencywindow1.pack()
    input_amount.pack()
    button_convert.pack()

def display_currency_converter_any_to_any():
    first_convert_any_currencywindow0.pack()
    first_convert_any_currency.pack()
    last_convert_any_currencywindow1.pack()
    last_convert_any_currency.pack()
    input_for_currencywindow1_any_to_any.pack()
    input_amount_any_to_any.pack()
    convert_any_currency_button.pack()
    User1.convert_any_currency(first_to_currency=first_convert_any_currency, last_to_currency=last_convert_any_currency, amount=input_amount_any_to_any)

def hide_currency_converter_any_to_any():
    first_convert_any_currencywindow0.pack_forget()
    first_convert_any_currency.pack_forget()
    last_convert_any_currencywindow1.pack_forget()
    last_convert_any_currency.pack_forget()
    input_for_currencywindow1_any_to_any.pack_forget()
    input_amount_any_to_any.pack_forget()
    convert_any_currency_button.pack_forget()

def process_input():
    logging.info('Starting: process_input')
    inputCCstring = entry.get()
    input_amount_content = input_amount.get()
    if inputCCstring == "q":
        root.quit()
    elif inputCCstring == "0":
        result_var.set(f"All currencies: " + ", ".join(User1.list_currencies()))
    elif inputCCstring == "1":
        print("it is working")
        hide_main_menu()
        display_currency_converter()
        try:
            int_amount = int(input_amount_content)
        except ValueError:
            result_var.set("Invalid amount!")
            return
        User1.convert_from_usd(to_currency=input_for_currency, amount=int_amount)
        result_var.set(f"Converted {input_amount_content} USD to {input_for_currency}.")
        clear_screen()
    elif inputCCstring == "2":
        User1.fetch_currency_data()
        result_var.set("Data refreshed!")
    elif inputCCstring == "3":
        User1.export_to_json()
        result_var.set("Data exported!")
    elif inputCCstring == "4":
        hide_main_menu()
        display_currency_converter_any_to_any()
        result_var.set(f"Converted {input_amount_any_to_any} {first_convert_any_currency} to {last_convert_any_currency}.")
    else:
        result_var.set("Please try again. Type 0, 1, 2, 3, 4 or q for exit.")
  
root = tk.Tk()
root.title("Python Currency Converter")

root.geometry("500x600")
root.configure(bg='#1a1a1a')  


#style
label_style = {
    "bg": "#1a1a1a",  
    "fg": "#e6e6e6",  
    "padx": 5,  
    "pady": 5
}

button_style = {
    "bg": "#33aaff",
    "fg": "white",
    "padx": 10,
    "pady": 5,
    "relief": "ridge",
    "borderwidth": 2
}

User1 = CurrencyConverter(balance=800000)
entry = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")

#Extra 
text_widget = tk.Text(root, height=5, wrap=tk.WORD)
convert_from_usd_ccwindow = tk.Label()
convert_from_usd_ccwindow_any_to_any = tk.Label()

#window with everything
CCwindow0 = tk.Label(root, text="[0] - List all currencies", **label_style)
CCwindow1 = tk.Label(root, text="[1] - Convert USD to a currency of choice", **label_style)
CCwindow2 = tk.Label(root, text="[2] - Refresh the data (fetch new currency data)", **label_style)
CCwindow3 = tk.Label(root, text="[3] - Export the data to JSON", **label_style)
CCwindow4 = tk.Label(root, text="[4] - Convert from any currency to another", **label_style)

back_button = tk.Button(root, text="Back", command=go_back_to_main, **button_style)

#step if == 1
input_for_currencywindow0 = tk.Label(root, text="What currency do you want to use? Use for example three letter as USD or SEK: ", **label_style)
input_for_currency = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")
input_for_currencywindow1 = tk.Label(root, text="How much USD Do you want to convert to? ", **label_style)
input_amount = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")
button_convert = tk.Button(root, text="Submit", command=currency_amount, **button_style)

# Step if == 4
first_convert_any_currencywindow0 = tk.Label(root, text="What currency do you want to use as base? Use for example three letter as USD or SEK: ")
first_convert_any_currency = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")
last_convert_any_currencywindow1 = tk.Label(root, text="What currency do you want to convert to? Use for example three letter as USD or SEK: ")
last_convert_any_currency = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")
input_for_currencywindow1_any_to_any = tk.Label(root, text="How much USD Do you want to convert to? ")
input_amount_any_to_any = tk.Entry(root, fg="black", bg="white", width=50, borderwidth=2, relief="ridge")
convert_any_currency_button = tk.Button(root, text="Submit", command=currency_amount_any_to_any)

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, **label_style)
button = tk.Button(root, text="Submit", command=process_input, **button_style)

def main():
    display_main_menu()
    root.mainloop()

if __name__ == "__main__":
    main()