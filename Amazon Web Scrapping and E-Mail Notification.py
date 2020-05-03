import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = "https://www.amazon.co.uk/Logitech-Ultrafast-Scrolling-Ergonomic-" \
      "Customisation/dp/B07W6JG6Z7/ref=sxbs_sxwds-stvp?cv_ct_cx=logitech+" \
      "mx+master+3&dchild=1&keywords=logitech+mx+master+3&pd_rd_i=" \
      "B07W6JG6Z7&pd_rd_r=4ee66124-2cf9-449e-afe4-0f640f276b65&pd_rd_w" \
      "=rb5Ix&pd_rd_wg=gpATp&pf_rd_p=d9b87ec0-c7c2-464c-b8a6-2e7b5576127a" \
      "&pf_rd_r=9R9MNSHWBYBDV6X7P4VR&psc=1&qid=1588489791&sr=1-1-718396d" \
      "e-69ac-46a0-9195-9669ab0086b2"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/81.0.4044.129 Safari/537.36"}

def check_price():
    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text()


    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:])


    if(converted_price<90):
        send_mail()

    print(title.strip())
    print(converted_price)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("jeffsabarman@gmail.com", "lyhpjllfvnqubwbn")

    subject = "Price fell down! How cool is this!"
    body = "Check the amazon link below!, The logitech MX Master 3 price" \
           "below 90 pound!\n" \
           "https://www.amazon.co.uk/Logitech-Ultrafast-Scrolling-Ergonomic-Customisation/dp/B07W6JG6Z7/ref=sxbs_sxwds-stvp?cv_ct_cx=logitech+mx+master+3&dchild=1&keywords=logitech+mx+master+3&pd_rd_i=B07W6JG6Z7&pd_rd_r=4ee66124-2cf9-449e-afe4-0f640f276b65&pd_rd_w=rb5Ix&pd_rd_wg=gpATp&pf_rd_p=d9b87ec0-c7c2-464c-b8a6-2e7b5576127a&pf_rd_r=9R9MNSHWBYBDV6X7P4VR&psc=1&qid=1588489791&sr=1-1-718396de-69ac-46a0-9195-9669ab0086b2"
    msg=f'Subject : {subject}\n\n{body}'

    server.sendmail(
        'jeffsabarman@gmail.com',
        'jeffsabarman@gmail.com',
        msg
    )
    print("Hey email has been sent!")

    server.quit()

while True:
    check_price()
    time.sleep(60 * 60)
