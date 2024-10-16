import requests
import argparse
import urllib3
urllib3.disable_warnings()

def proxmox_connect( proxmoxhost: str, username: str, password: str, nodename: str, vmid: str):    
    
    uri = "https://" + proxmoxhost + ":8006/api2/json/access/ticket"

    ticketrequestbody = {
        "username": username,
        "password": password
    }

    headers = { "Content-Type": "application/x-www-form-urlencoded"}

    try:   
        ticketresponse = requests.post(uri, verify=False, data=ticketrequestbody,headers=headers)
    except:
        print( "Error:ticket request failed")
        exit(1)

    if ticketresponse.status_code == 200:
        try:
        # Parsing the JSON response
            ticketdata = ticketresponse.json()
        # print(ticketdata)
        except ValueError:
            print("Error: Unable to parse JSON response")
    else:
        print(f"Request failed with status code {ticketresponse.status_code}")

    ticket = ticketdata['data']['ticket']

    CSRFPreventionToken = ticketdata['data']['CSRFPreventionToken']

    #print(ticket)
    #print(CSRFPreventionToken)

    session = requests.Session()
    session.cookies.set('PVEAuthCookie', ticket)

    # Headers including the CSRF prevention token
    apiheaders = {
        'CSRFPreventionToken': CSRFPreventionToken
    }

    baseuri = "https://" + proxmoxhost + ":8006/api2/json/version"
    try:
        APIresponse = session.get(baseuri, headers=apiheaders, verify=False)
    except:
        print( "Error: API Request Failed")
        exit(1)

    # Checking if the API request was successful
    if APIresponse.status_code == 200:
        versioninfo = APIresponse.json()
        pveversion = versioninfo['data']['version']
        print(pveversion)
    else:
        print(f"API request failed with status code {APIresponse.status_code}")

    # end of connection test section

    # exit(0)

    # now get vm status
    baseuri = "https://" + proxmoxhost + ":8006/api2/json/nodes/" + nodename + "/qemu/" + vmid + "/status/current"
    try:
        APIresponse2 = session.get(baseuri, headers=apiheaders, verify=False)
    except:
        print( "Error: API Request Failed")
        exit(1)

    if APIresponse2.status_code == 200:
        vmstatusinfo = APIresponse2.json()
        vmstatus = vmstatusinfo['data']['qmpstatus']
        print(vmstatus)
    else:
        print(f"API request failed with status code {APIresponse3.status_code}")
    
    if vmstatus != "running":
        dostartup = False
        if vmstatus == "paused":
            baseuri = "https://" + proxmoxhost + ":8006/api2/json/nodes/" + nodename + "/qemu/" + vmid + "/status/resume"
            dostartup = True
        elif vmstatus == "stopped":
            baseuri = "https://" + proxmoxhost + ":8006/api2/json/nodes/" + nodename + "/qemu/" + vmid + "/status/start"
            dostartup = True
        else:
            print( "VM not detected as running but not in paused or stopped state - no action taken.")

        if dostartup == True:
            startbody = {
            "node": nodename,
            "vmid": vmid
            }
            
            try:
                APIresponse3 = session.post(baseuri, headers=apiheaders, verify=False)
            except:
                print( "Error: API Request Failed")
                exit(1)
            
            if APIresponse3.status_code == 200:
                runstateinfo = APIresponse3.json()
                runstate = runstateinfo['data']
                print(runstate)
            else:
                print(f"API request failed with status code {APIresponse3.status_code}")

    else:
        print( "VM running - no action to take.")

                    

def main( proxmoxhost ="proxmoxhost.local",username="username@pve",password="YourPassword",nodename="yournodename",vmid=100):
    proxmox_connect(proxmoxhost=proxmoxhost,username=username,password=password,nodename=nodename,vmid=vmid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple greeting script.")
    
    # Define command-line arguments with defaults
    parser.add_argument('--proxmoxhost', type=str, default="proxmoxhost.local", help='Proxmox Hostname')
    parser.add_argument('--username', type=str, default="username@pve", help='Proxmox Username')
    parser.add_argument('--password', type=str, default="YourPassword", help='Proxmox Password.')
    parser.add_argument('--nodename', type=str, default="yournodename", help='Proxmox Node.')
    parser.add_argument('--vmid', type=str, default="100", help='Proxmox VMID.')

    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    main(proxmoxhost=args.proxmoxhost, username=args.username, password=args.password, nodename=args.nodename, vmid=args.vmid)


