import requests
import json
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv

class CurrencyConverter(tk.Tk):
    def __init__(self, balance: int):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("300x200")
        self._balance = balance
        
        try:
            self._allcurrenciesdata = self.load_currency_data()
        except:
            self._allcurrenciesdata = self.fetch_currency_data()

    def fetch_currency_data(self):
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
        headers = {"accept": "application/json"} 
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        file = open("openexchangerates.json","w")
        json.dump(data, file)
        return data
    
    def convert_from_usd(self, to_currency: str, amount: int):
        load_dotenv()
        api_key = os.environ.get("API_KEY")
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        headers = {"accept": "application/json"} 
        response = requests.get(url, headers=headers)
        alldata = response.json()
        value = alldata["rates"][to_currency]
        valuenumber = int(value)
        print(f"Your choosen currency {to_currency} has a value of {valuenumber} on USD as base!")
        newamount = amount * valuenumber
        convert_from_usd_ccwindow = tk.Label(text=f"Your new amount is {newamount}")
        convert_from_usd_ccwindow.pack()
    
    def list_currencies(self):
        with open('openexchangerates.json', 'r') as file:
            data = json.load(file)
            allcurrencies = data["rates"]
            sort_data = sorted(allcurrencies.keys())
            text_widget = tk.Text(height=5, wrap=tk.WORD)
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
    
    def load_currency_data(self):
        with open('openexchangerates.json', 'r') as file:
            data = json.load(file)
        return data

    def export_to_json(self):
        print("Hello?")
        with open("openexchangerates.json", "w") as file:
            json.dump(self._allcurrenciesdata, file)

def process_input():
    def currency_amount():
        to_currency_value = input_for_currency.get()
        try:
            amount_value = int(input_amount.get())
            User1.convert_from_usd(to_currency=to_currency_value, amount=amount_value)
            result_var.set(f"Converted {amount_value} USD to {to_currency_value}.")
        except ValueError:
            result_var.set("Invalid amount!")

    inputCCstring = entry.get()
    User1 = CurrencyConverter(balance=800000)
    if inputCCstring == "10":
        root.quit()
    elif inputCCstring == "0":
        result_var.set(f"All currencies: " + ", ".join(User1.list_currencies()))
    elif inputCCstring == "1":
        input_for_currencywindow0 = tk.Label(text="What currency do you want to use? Use for example three letter as USD or SEK: ")
        input_for_currency = tk.Entry()
        input_for_currencywindow1 = tk.Label(text="How much USD Do you want to convert to? ")
        input_amount = tk.Entry()
        button_convert = tk.Button(text="Submit", command=currency_amount)

        input_for_currencywindow0.pack()
        input_for_currency.pack()
        input_for_currencywindow1.pack()
        input_amount.pack()
        button_convert.pack()

        try:
            int_amount = int(input_amount)
        except ValueError:
            result_var.set("Invalid amount!")
            return
        User1.convert_from_usd(to_currency=input_for_currency, amount=int_amount)
        result_var.set(f"Converted {input_amount} USD to {input_for_currency}.")
    elif inputCCstring == "2":
        User1.fetch_currency_data()
        result_var.set("Data refreshed!")
    elif inputCCstring == "3":
        User1.export_to_json()
        result_var.set("Data exported!")
    else:
        result_var.set("Please try again. Type 0, 1, 2, 3, 4 or 10.")

root = tk.Tk()
root.title("Python Currency Converter")

entry1 = tk.Entry(fg="yellow", bg="blue", width=50)
CCwindow0 = tk.Label(text="[0] - List all currencies")
CCwindow1 = tk.Label(text="[1] - Convert USD to a currency of choice")
CCwindow2 = tk.Label(text="[2] - Refresh the data (fetch new currency data)")
CCwindow3 = tk.Label(text="[3] - Export the data to JSON")
CCwindow4 = tk.Label(text="[4] - Convert from any currency to another")

CCwindow5 = tk.Label(text="[3] - Export the data to JSON")
CCwindow6 = tk.Label(text="[4] - Convert from any currency to another")
entry = tk.Entry()
entry2 = tk.Entry(fg="yellow", bg="blue", width=50)
button = tk.Button(text="Submit", command=process_input)
result_var = tk.StringVar()
result_label = tk.Label(textvariable=result_var)

def main():
    CCwindow0.pack()
    CCwindow1.pack()
    CCwindow2.pack()
    CCwindow3.pack()
    CCwindow4.pack()
    entry1.pack()
    entry.pack()
    entry2.pack()
    button.pack()
    result_label.pack()
    root.mainloop()

if __name__ == "__main__":
    main()