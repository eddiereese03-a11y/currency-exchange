import streamlit as st
import requests
from datetime import datetime
import pandas as pd

class CurrencyConverter:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.currency_symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'AUD': 'A$',
            'CAD': 'C$', 'CHF': 'CHF', 'CNY': '¥', 'INR': '₹', 'RUB': '₽',
            'BRL': 'R$', 'ZAR': 'R', 'KRW': '₩', 'MXN': '$', 'SGD': 'S$',
            'HKD': 'HK$', 'NOK': 'kr', 'SEK': 'kr', 'DKK': 'kr', 'PLN': 'zł',
            'THB': '฿', 'IDR': 'Rp', 'HUF': 'Ft', 'CZK': 'Kč', 'ILS': '₪',
            'PHP': '₱', 'AED': 'د.إ', 'COP': '$', 'SAR': '﷼', 'MYR': 'RM',
            'RON': 'lei', 'TRY': '₺', 'NZD': 'NZ$', 'VND': '₫', 'ARS': '$',
            'EGP': '£', 'PKR': '₨', 'BGN': 'лв', 'NGN': '₦', 'UAH': '₴'
        }
        self.currency_names = {
            'USD': 'US Dollar', 'EUR': 'Euro', 'GBP': 'British Pound',
            'JPY': 'Japanese Yen', 'AUD': 'Australian Dollar', 'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc', 'CNY': 'Chinese Yuan', 'INR': 'Indian Rupee',
            'RUB': 'Russian Ruble', 'BRL': 'Brazilian Real', 'ZAR': 'South African Rand',
            'KRW': 'South Korean Won', 'MXN': 'Mexican Peso', 'SGD': 'Singapore Dollar',
            'HKD': 'Hong Kong Dollar', 'NOK': 'Norwegian Krone', 'SEK': 'Swedish Krona',
            'DKK': 'Danish Krone', 'PLN': 'Polish Zloty', 'THB': 'Thai Baht',
            'IDR': 'Indonesian Rupiah', 'HUF': 'Hungarian Forint', 'CZK': 'Czech Koruna',
            'ILS': 'Israeli Shekel', 'PHP': 'Philippine Peso', 'AED': 'UAE Dirham',
            'COP': 'Colombian Peso', 'SAR': 'Saudi Riyal', 'MYR': 'Malaysian Ringgit',
            'RON': 'Romanian Leu', 'TRY': 'Turkish Lira', 'NZD': 'New Zealand Dollar',
            'VND': 'Vietnamese Dong', 'ARS': 'Argentine Peso', 'EGP': 'Egyptian Pound',
            'PKR': 'Pakistani Rupee', 'BGN': 'Bulgarian Lev', 'NGN': 'Nigerian Naira',
            'UAH': 'Ukrainian Hryvnia'
        }
        
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_exchange_rates(_self, base_currency="USD"):
        """Fetch exchange rates for a base currency"""
        try:
            response = requests.get(f"{_self.base_url}{base_currency}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching exchange rates: {e}")
            return None
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        try:
            data = self.get_exchange_rates(from_currency)
            
            if data and 'rates' in data:
                if to_currency in data['rates']:
                    rate = data['rates'][to_currency]
                    converted_amount = amount * rate
                    return converted_amount, rate, data.get('date', 'N/A')
                else:
                    return None, None, None
            else:
                return None, None, None
        except Exception as e:
            st.error(f"Error converting currency: {e}")
            return None, None, None
    
    def get_symbol(self, currency_code):
        """Get currency symbol"""
        return self.currency_symbols.get(currency_code, currency_code)
    
    def get_currency_name(self, currency_code):
        """Get full currency name"""
        return self.currency_names.get(currency_code, currency_code)
    
    def get_popular_rates(self, base_currency, currencies_list):
        """Get rates for popular currencies"""
        data = self.get_exchange_rates(base_currency)
        popular = ['EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'INR']
        rates_data = []
        
        if data and 'rates' in data:
            for curr in popular:
                if curr != base_currency and curr in data['rates']:
                    rates_data.append({
                        'Currency': f"{self.get_symbol(curr)} {curr}",
                        'Name': self.get_currency_name(curr),
                        'Rate': f"{data['rates'][curr]:.4f}",
                        f'1 {base_currency} equals': f"{data['rates'][curr]:.4f} {curr}"
                    })
        
        return pd.DataFrame(rates_data)


def main():
    # Page configuration
    st.set_page_config(
        page_title="Currency Converter",
        page_icon="💱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .big-font {
            font-size: 50px !important;
            font-weight: bold;
            color: #4CAF50;
        }
        .result-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f8ff;
            border: 2px solid #4CAF50;
            margin: 20px 0;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize converter
    converter = CurrencyConverter()
    
    # Header
    st.title("💱 Currency Exchange Rate Converter")
    st.markdown("### Real-time currency conversion with live exchange rates")
    st.markdown("---")
    
    # Get all available currencies
    initial_data = converter.get_exchange_rates("USD")
    if initial_data and 'rates' in initial_data:
        all_currencies = sorted(['USD'] + list(initial_data['rates'].keys()))
    else:
        all_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD']
    
    # Create currency display list with symbols
    currency_display = [f"{converter.get_symbol(c)} {c} - {converter.get_currency_name(c)}" 
                       if c in converter.currency_names 
                       else f"{converter.get_symbol(c)} {c}" 
                       for c in all_currencies]
    currency_dict = dict(zip(currency_display, all_currencies))
    
    # Main conversion section
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.subheader("From")
        from_display = st.selectbox(
            "Select source currency",
            currency_display,
            index=currency_display.index([d for d in currency_display if 'USD' in d][0]) if any('USD' in d for d in currency_display) else 0,
            key="from_currency"
        )
        from_currency = currency_dict[from_display]
        
        amount = st.number_input(
            "Amount",
            min_value=0.01,
            value=100.0,
            step=1.0,
            format="%.2f"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Swap"):
            # Swap currencies by updating session state
            st.session_state.swap = True
    
    with col3:
        st.subheader("To")
        to_display = st.selectbox(
            "Select target currency",
            currency_display,
            index=currency_display.index([d for d in currency_display if 'EUR' in d][0]) if any('EUR' in d for d in currency_display) else 1,
            key="to_currency"
        )
        to_currency = currency_dict[to_display]
    
    # Handle swap
    if 'swap' in st.session_state and st.session_state.swap:
        st.session_state.swap = False
        st.rerun()
    
    # Convert button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💰 Convert Currency", type="primary"):
        if from_currency and to_currency:
            with st.spinner("Converting..."):
                converted, rate, date = converter.convert_currency(
                    amount, from_currency, to_currency
                )
                
                if converted is not None:
                    # Display result
                    st.markdown("---")
                    st.success("✅ Conversion Successful!")
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        st.markdown("### Result")
                        from_symbol = converter.get_symbol(from_currency)
                        to_symbol = converter.get_symbol(to_currency)
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h2 style="color: #333;">{from_symbol}{amount:,.2f} {from_currency}</h2>
                            <h1 style="color: #4CAF50; margin: 10px 0;">⬇️</h1>
                            <h1 class="big-font">{to_symbol}{converted:,.2f} {to_currency}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with result_col2:
                        st.markdown("### Exchange Rate Info")
                        st.info(f"""
                        **Exchange Rate:**  
                        1 {from_currency} = {rate:.6f} {to_currency}
                        
                        **Inverse Rate:**  
                        1 {to_currency} = {1/rate:.6f} {from_currency}
                        
                        **Last Updated:**  
                        {date}
                        """)
                else:
                    st.error("❌ Conversion failed. Please check your internet connection.")
    
    # Sidebar with popular rates
    with st.sidebar:
        st.header("📊 Popular Exchange Rates")
        
        base_curr_display = st.selectbox(
            "Base Currency",
            currency_display,
            index=0,
            key="sidebar_base"
        )
        base_curr = currency_dict[base_curr_display]
        
        if st.button("Refresh Rates", key="refresh"):
            st.cache_data.clear()
            st.rerun()
        
        rates_df = converter.get_popular_rates(base_curr, all_currencies)
        
        if not rates_df.empty:
            st.dataframe(
                rates_df[['Currency', 'Rate']],
                hide_index=True,
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("""
        ### 💡 About
        - Real-time exchange rates
        - 160+ currencies supported
        - Updated every hour
        - Powered by ExchangeRate-API
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666;">
            <p>💱 Currency Exchange Rate Converter | Powered by ExchangeRate-API</p>
            <p><small>Rates are updated regularly and may vary slightly from actual market rates</small></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
