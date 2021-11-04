import requests
import json


def login(username: str, password: str, otp_code: str):
    url = "https://api.nobitex.ir/auth/login/"

    payload = {'username': username,
               'password': password,
               'remember': 'yes',
               'captcha': 'api'}
    files = [

    ]
    headers = {
        'x-totp': otp_code,
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def order_book(symbol: str):
    url = "https://api.nobitex.ir/v2/orderbook"

    payload = {'symbol': symbol}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def trades(symbol: str):
    url = "https://api.nobitex.ir/v2/trades"

    payload = {'symbol': symbol}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def stats(src: str, dst: str):
    url = "https://api.nobitex.ir/market/stats"


    payload = {
        'srcCurrency' : src,
        'dstCurrency': dst
    }
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def OHL(symbol: str, resolution: str, fist_date: str, last_date: str):
    url = "https://api.nobitex.ir/market/udf/history?symbol=" + symbol + "&resolution=" + resolution + "&from=" \
          + fist_date + "&to=" + last_date
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def global_stats():
    url = "https://api.nobitex.ir/market/global-stats"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def profile(token: str):
    url = "https://api.nobitex.ir/users/profile"

    payload = {}
    headers = {
        'Authorization': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def login_attemp(token: str):
    url = "https://api.nobitex.ir/users/login-attempts"

    payload = {}
    headers = {
        'Authorization': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def card_add(card_number: str, bank_name: str, token: str):
    url = "https://api.nobitex.ir/users/cards-add"

    payload = json.dumps({
        "number": card_number,
        "bank": bank_name
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def account_add(card_number: str, shaba: str, bank_name: str, token: str):
    url = "https://api.nobitex.ir/users/accounts-add"

    payload = json.dumps({
        "number": card_number,
        "shaba": shaba,
        "bank": bank_name
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def limitations(token: str):
    url = "https://api.nobitex.ir/users/limitations"

    payload = {}
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def wallets_list(token: str):
    url = "https://api.nobitex.ir/users/wallets/list"

    payload = {}
    headers = {
        'Authorization': token
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def balance(currency: str, token: str):
    url = "https://api.nobitex.ir/users/wallets/balance"

    payload = {'currency': currency}
    files = [

    ]
    headers = {
        'Authorization': token
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def transactions_list(token: str, wallet: str):
    import requests

    url = "https://api.nobitex.ir/users/wallets/transactions/list"

    payload = {'wallet': wallet}
    files = [

    ]
    headers = {
        'Authorization': token,
        'Cookie': '__cfduid=d727d4fbddc828884f2a793143332d5aa1613231485; csrftoken=6iEk9yjmgJFbNCXSELduTVeTTEJZBSNu7H0QbN7ZrRbqRLQS8s1oz3nTOIDj1EBH'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def deposits_and_withdraws(token: str, wallet: str):
    url = "https://api.nobitex.ir/users/wallets/deposits/list"

    payload = {'wallet': wallet}
    files = [

    ]
    headers = {
        'Authorization': token,
        'Cookie': '__cfduid=d727d4fbddc828884f2a793143332d5aa1613231485; csrftoken=6iEk9yjmgJFbNCXSELduTVeTTEJZBSNu7H0QbN7ZrRbqRLQS8s1oz3nTOIDj1EBH; sessionid=208gbekbzl74ea5bz5zyy3iq5x082pfd'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    return response


def generate_wallet_address(token: str, wallet: str):
    url = "https://api.nobitex.ir/users/wallets/generate-address"

    payload = {'wallet': wallet}
    files = [

    ]
    headers = {
        'Authorization': token,
        'Cookie': '__cfduid=d727d4fbddc828884f2a793143332d5aa1613231485; csrftoken=6iEk9yjmgJFbNCXSELduTVeTTEJZBSNu7H0QbN7ZrRbqRLQS8s1oz3nTOIDj1EBH'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def add_order(type: str, src: str, dst: str, amount: str, price: int, token: str):
    url = "https://api.nobitex.ir/market/orders/add"

    payload = json.dumps({
        "type": type,
        "srcCurrency": src,
        "dstCurrency": dst,
        "amount": amount,
        "price": price
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def order_status(token: str, status_id: int):
    url = "https://api.nobitex.ir/market/orders/status"

    payload = json.dumps({
        "id": status_id
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def order_list(token: str, src: str, dst: str, details: int):
    url = "https://api.nobitex.ir/market/orders/list"

    payload = json.dumps({
        "srcCurrency": src,
        "dstCurrency": dst,
        "details": details
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def update_order_status(token: str, order_number: int, status: str):
    url = "https://api.nobitex.ir/market/orders/update-status"

    payload = json.dumps({
        "order": order_number,
        "status": status
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def cancel_order(token: str, src: str, dst: str, hours: float, executation: str):
    url = "https://api.nobitex.ir/market/orders/cancel-old"

    payload = json.dumps({
        "execution": executation,
        "srcCurrency": src,
        "dstCurrency": dst,
        "hours": hours
    })
    headers = {
        'Authorization': token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
