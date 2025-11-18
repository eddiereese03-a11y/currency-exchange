import requests
import json
from datetime import datetime

class CurrencyConverter:
    def __init__(self):
        # Using ExchangeRate-API free tier (no API key required for basic access)
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        
    def get_exchange_rates(self, base_currency="USD"):
        """Fetch exchange rates for a base currency"""
        try:
            response = requests.get(f"{self.base_url}{base_currency}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return None
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        try:
            # Get rates based on the from_currency
            data = self.get_exchange_rates(from_currency)
            
            if data and 'rates' in data:
                if to_currency in data['rates']:
                    rate = data['rates'][to_currency]
                    converted_amount = amount * rate
                    return converted_amount, rate
                else:
                    print(f"Currency {to_currency} not found")
                    return None, None
            else:
                print("Failed to fetch exchange rates")
                return None, None
        except Exception as e:
            print(f"Error converting currency: {e}")
            return None, None
    
    def display_popular_rates(self, base_currency="USD"):
        """Display exchange rates for popular currencies"""
        popular_currencies = ["EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR"]
        
        data = self.get_exchange_rates(base_currency)
        
        if data:
            print(f"\n{'='*60}")
            print(f"Exchange Rates for {base_currency}")
            print(f"Last Updated: {data.get('date', 'N/A')}")
            print(f"{'='*60}")
            
            for currency in popular_currencies:
                if currency != base_currency and currency in data['rates']:
                    rate = data['rates'][currency]
                    print(f"1 {base_currency} = {rate:.4f} {currency}")
            print(f"{'='*60}\n")
    
    def list_all_currencies(self, base_currency="USD"):
        """List all available currencies"""
        data = self.get_exchange_rates(base_currency)
        
        if data and 'rates' in data:
            print(f"\nAvailable currencies ({len(data['rates'])} total):")
            currencies = sorted(data['rates'].keys())
            
            # Print in columns
            for i in range(0, len(currencies), 6):
                print("  ".join(currencies[i:i+6]))
            print()

def main():
    converter = CurrencyConverter()
    
    print("\n" + "="*60)
    print("           CURRENCY EXCHANGE RATE APP")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Convert Currency")
        print("2. View Popular Exchange Rates")
        print("3. List All Available Currencies")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n--- Currency Conversion ---")
            amount = float(input("Enter amount: "))
            from_curr = input("From currency (e.g., USD): ").upper().strip()
            to_curr = input("To currency (e.g., EUR): ").upper().strip()
            
            converted, rate = converter.convert_currency(amount, from_curr, to_curr)
            
            if converted is not None:
                print(f"\n{amount:.2f} {from_curr} = {converted:.2f} {to_curr}")
                print(f"Exchange Rate: 1 {from_curr} = {rate:.4f} {to_curr}")
            
        elif choice == "2":
            base = input("\nEnter base currency (default USD): ").upper().strip()
            if not base:
                base = "USD"
            converter.display_popular_rates(base)
            
        elif choice == "3":
            converter.list_all_currencies()
            
        elif choice == "4":
            print("\nThank you for using Currency Exchange Rate App!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
