```
        ╔╦╗╔╦╗╔╗╔╔═╗          
         ║║ ║║║║║╚═╗          
        ═╩╝═╩╝╝╚╝╚═╝          
╔═╗┬  ┌─┐┬ ┬┌┬┐┌─┐┬  ┌─┐┬─┐┌─┐
║  │  │ ││ │ ││├┤ │  ├─┤├┬┘├┤ 
╚═╝┴─┘└─┘└─┘─┴┘└  ┴─┘┴ ┴┴└─└─┘
```
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
The first time it will create the configuration files at `config/`
```bash
config/
├── config.json
└── zones.json
```
Just follow the console prompts to configure the access token, zones and records to update.
```txt
Unable to read config at config/config.json...
Please type in the cloudflare access token: YOURaccessTOKEN
Unable to read zones config at config/zones.json...
        🌐 0. domain.com        id: dfg23f1ef12f1.....
Select the zones to update: 0
        🌐 domain.com :
                📝 0. web.domain.com -> type:A -> ttl:60
Select the records to update: 0
All records updated... ['web.domain.com']
```

Then just add the following lines to your crontab jobs:
`crontab -e`
```bash
@reboot bash /path/ddns-cloudflare/ddns-cloudflare.sh
0 * * * * bash /path/ddns-cloudflare/ddns-cloudflare.sh
```
Replacing the `/path/` with your installation folder, this lines will check and update the DNS records configured  hourly