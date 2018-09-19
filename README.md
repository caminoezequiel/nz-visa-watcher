# nz-visa-watcher
A simple script to checks if NZ Working Holiday Visa for Argentines is ready to apply

## Instalation
```
pipenv install
```
### Config crontab

Open crontab `crontab -e` and set to run every 15  min
```
# m h  dom mon dow   command
*/15 * * * *    pipenv run python /var/www/visa-watcher/main.py >> /var/log/visa_watcher.log
```

