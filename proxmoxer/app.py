from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load environment variables
load_dotenv()
PROXMOX_API_URL = os.getenv('PROXMOX_API_URL')
TOKEN_ID = os.getenv('TOKEN_ID')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')

HEADERS = {
    'Authorization': f'PVEAPIToken={TOKEN_ID}={TOKEN_SECRET}'
}

@app.route('/home', methods=['GET'])
def home():
    """ Confirm connection and display Proxmox version information. """
    try:
        response = requests.get(f'{PROXMOX_API_URL}/version', headers=HEADERS, verify=False)
        data = response.json()
        return render_template('home.html', version=data.get('data'))
    except Exception as e:
        flash(f'Error: {str(e)}')
        return render_template('home.html')

@app.route('/firewall-create', methods=['GET', 'POST'])
def firewall_create():
    """ Create a firewall rule for a specific VM. """
    if request.method == 'POST':
        node = request.form['node']
        vmid = request.form['vmid']
        rule_data = {
            'action': request.form['action'],
            'type': request.form['type'],
            'macro': request.form['macro'],
        }
        try:
            response = requests.post(f'{PROXMOX_API_URL}/nodes/{node}/qemu/{vmid}/firewall/rules', headers=HEADERS, json=rule_data, verify=False)
            if response.status_code == 200:
                flash('Firewall rule created successfully.')
            else:
                flash('Failed to create firewall rule.')
            return redirect(url_for('firewall_create'))
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('firewall_create.html')

@app.route('/firewall-delete', methods=['GET', 'POST'])
def firewall_delete():
    """ Delete a firewall rule for a specific VM. """
    if request.method == 'POST':
        node = request.form['node']
        vmid = request.form['vmid']
        pos = request.form['pos']
        try:
            response = requests.delete(f'{PROXMOX_API_URL}/nodes/{node}/qemu/{vmid}/firewall/rules/{pos}', headers=HEADERS, verify=False)
            if response.status_code == 200:
                flash('Firewall rule deleted successfully.')
            else:
                flash('Failed to delete firewall rule.')
            return redirect(url_for('firewall_delete'))
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('firewall_delete.html')

@app.route('/firewall-update', methods=['GET', 'POST'])
def firewall_update():
    """ Update an existing firewall rule. """
    if request.method == 'POST':
        node = request.form['node']
        vmid = request.form['vmid']
        pos = request.form['pos']
        rule_data = {
            'action': request.form['action'],
            'type': request.form['type'],
            'macro': request.form['macro'],
        }
        try:
            response = requests.put(f'{PROXMOX_API_URL}/nodes/{node}/qemu/{vmid}/firewall/rules/{pos}', headers=HEADERS, json=rule_data, verify=False)
            if response.status_code == 200:
                flash('Firewall rule updated successfully.')
            else:
                flash('Failed to update firewall rule.')
            return redirect(url_for('firewall_update'))
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('firewall_update.html')

@app.route('/firewall-show', methods=['GET', 'POST'])
def firewall_show():
    """ Show firewall rules for a specific VM. """
    rules = []
    if request.method == 'POST':
        node = request.form['node']
        vmid = request.form['vmid']
        try:
            response = requests.get(f'{PROXMOX_API_URL}/nodes/{node}/qemu/{vmid}/firewall/rules', headers=HEADERS, verify=False)
            if response.status_code == 200:
                rules = response.json().get('data', [])
                print(rules)
            else:
                flash('Failed to retrieve firewall rules.')
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('firewall_show.html', rules=rules)

if __name__ == '__main__':
    app.run(debug=True)
