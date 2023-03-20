import qrcode

if __name__ == "__main__":

    site_link = "https://t.me/ksyprbot"
    qr_link = "qr-link/qr_link.png"

    img = qrcode.make(site_link)
    img.save(qr_link)