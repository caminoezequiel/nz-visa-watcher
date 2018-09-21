# nz-visa-watcher
A simple script to checks if NZ Working Holiday Visa for Argentines is ready to apply and notify via email (a sendGrid's template)

## Instalation

You need to run `pipenv install` and after you should create the `config.yml` from `config-dist.yml` and set following:
```
VISA_URL: 'https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/argentina-whs'

CHECKSUM: '7b73d2b45d13f688ac0d07bac8bd0fd1' #It's the checksum of html when the button apply is disabled.

LOG_FILE: 'app.log'

EMAIL_TO: "EMAIL TO NOTIFY"
EMAIL_FROM: "noreply@example.com"
SEND_GRID_KEY: "YOUR SEND GRID KEY"
SEND_GRID_TEMPLATE: "A SEND GRID TEMPLARTE ID"
```
### Config crontab

Open crontab `crontab -e` and set to run every 15  min
```
# m   h  dom mon dow   command
 */15 *   *   *   *    pipenv run python /var/www/visa-watcher/main.py
```

### Logs
You can see all logs in `app.log`
```
tail -f /var/www/visa-watcher/app.log
```
