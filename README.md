# DDNS Cloudflare
Dynamic update of DNS records (A and AAAA) for Cloudflare domains. This app retrieve the PUBLIC IP of the server and then updates the selected DNS records.
## Install

Install dependencies and clone this repository:
```bash
sudo apt install dnsutils
git clone https://github.com/Eric106/ddns-cloudflare
```
Go into the folder `ddns-cloudflare` and execute the `ddns-cloudflare.sh` script.
```bash
cd ddns-cloudflare/
bash ddns-cloudflare.sh
```
The first time it will create the configuration file at `config/`
```bash
config/
└── config.json
```
Just follow the console prompts to configure the access token, zones and records to update.

> `NOTE ✅` :
At selection of zones and records to update, you can use range (5-8 -8 5-) or list of items to select ( 5,6,7,8 )

```txt
        ╔╦╗╔╦╗╔╗╔╔═╗          
         ║║ ║║║║║╚═╗          
        ═╩╝═╩╝╝╚╝╚═╝          
╔═╗┬  ┌─┐┬ ┬┌┬┐┌─┐┬  ┌─┐┬─┐┌─┐
║  │  │ ││ │ ││├┤ │  ├─┤├┬┘├┤ 
╚═╝┴─┘└─┘└─┘─┴┘└  ┴─┘┴ ┴┴└─└─┘
by Eric106
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
Unable to read config at config/config.json...
<><><><><><><><><><><><><><><><><><><><><><><><><>
Please type in the cloudflare access token: Y0urAccessT0ken
        🌐 0. domain.com        id: dfg23f1ef12f1.....
Select the zones to update: 0
        🌐 domain.com :
                📝 0. web.domain.com -> type:A -> ttl:60
Select the records to update: 0
<><><><><><><><><><><><><><><><><><><><><><><><><>
Do you want to add other account (y/n)?: n
All records updated... ['web.domain.com']
```

Then just add the following lines to your crontab jobs:
`crontab -e`, replacing the `/path/` with your installation folder
```bash
@reboot bash /path/ddns-cloudflare/ddns-cloudflare.sh
0 * * * * bash /path/ddns-cloudflare/ddns-cloudflare.sh
```
This lines will check and update the DNS records every hour and on system reboot.

## Make binary

If you want to compile by yourself the binary that is also included in the `bin/` folder, you first need to create and install the proper conda environment

```bash
conda create -n ddns-cf python==3.10.* -y
conda activate ddns-cf
pip install -r requirements.txt
```

Then just run the `make.sh` script
```bash
bash make.sh
```
