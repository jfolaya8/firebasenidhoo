import requests
from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
import ssl
import pyppeteer

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

initialize_app()
@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    body = req.get_json()
    if body.get('method') == 'POST':
        url = body.get('url')
        data = body.get('data')
        if body.get('type') == "JSON":
            response = requests.post(url, json=data, verify=False)
        else:
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'content-Length': str(len(data))
            }
            response = requests.post(url, data=data, headers=headers)
    
    if body.get('method') == 'GET':
        get_data()
        response = requests.get(url, verify=False)
    return https_fn.Response(response.text)


async def get_data():
    # Launch Chromium in headless mode
    browser = await pyppeteer.launch(headless=True)
    page = await browser.newPage()

    # Navigate to the page
    await page.goto('https://nube.celsia.com:4443/clientes/paga-tus-facturas?special=%7B%22codigoCuenta%22:%22314053%22%7D')
    title = await page.title()
    print("Page title:", title)

    # Close the browser
    await browser.close()