# DDNS Cloudflare

## Install

Clone this repository
```bash
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
```txt
        ╔╦╗╔╦╗╔╗╔╔═╗          
         ║║ ║║║║║╚═╗          
        ═╩╝═╩╝╝╚╝╚═╝          
╔═╗┬  ┌─┐┬ ┬┌┬┐┌─┐┬  ┌─┐┬─┐┌─┐
║  │  │ ││ │ ││├┤ │  ├─┤├┬┘├┤ 
╚═╝┴─┘└─┘└─┘─┴┘└  ┴─┘┴ ┴┴└─└─┘
Unable to read config at config/config.json...
<><><><><><><><><><><><><><><><><><><><><><><><><>
Please type in the cloudflare access token: Y0urAccessT0ken
Unable to read zones config at config/zones.json...
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
`crontab -e`
```bash
@reboot bash /path/ddns-cloudflare/ddns-cloudflare.sh
0 * * * * bash /path/ddns-cloudflare/ddns-cloudflare.sh
```
Replacing the `/path/` with your installation folder, this lines will check and update the DNS records configured  hourly

## Make binary

If you want to compile by yourself the binary that is also included in the root of this repository, you first need to create and install the proper conda environment

```bash
conda create -n ddns-cf python==3.10.* -y
conda activate ddns-cf
pip install -r requirements.txt
```

Then just run the `make.sh` script
```bash
bash make.sh
```
