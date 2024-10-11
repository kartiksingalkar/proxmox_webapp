from proxmoxer import ProxmoxAPI

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)


proxmox = ProxmoxAPI('<host_ip_or_domain>', user='<username>@<realm>', password='<password>', verify_ssl=False)




