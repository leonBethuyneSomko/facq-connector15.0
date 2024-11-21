# Project template

Dit project bevat de huidige template voor een project van het type:
git/docker-compose.

## Initiatie van de template

1. Verwijder `readme.md`
2. Vul de naam van de klant en de domeinen in op `/docker/.env` (Hidden file).
3. Verwijder .git

## Gebruik template in production

Deze template gaat er van uit dat ieder project een somko domain heeft.
Namelijk:

- __klant__.somko.be
- test.__klant__.somko.be

Voor correcte werking moeten deze domainen adressen dus verwijzen naar de
product server. (Bij het schrijven van deze readme gebruikt somko cloudflare)

1. Stel bovenstaande domain adresen in en zorgt dat de klant naam en
extra domainen correct is ingesteld in `docker/.env`.

2. Documenteer de inlog gegevens van de gegeven productie server op onedrive of
Odoo.

3. login op de server.

4. geneer een ssh key met `ssh-keygen` (spam enter tot commando sluit).
Kopieer de public key (`cat .ssh/id_rsa.pub`) en voeg deze toe bij access keys
op bitbucket (of huidig git systeem).

5. Maak een folder `odoo` aan (`mkdir odoo`). Ga in deze folder `cd odoo` en clone de git repo 2 keer als
`prod` en `test`. Je kan dit in een keer uitvoeren als `git clone git@bitbucket.org:somko-consulting/project.git prod && cp -r prod test`.
(Note: Test en Prod staan standaard op branch master)

6. Maak de links aan in `~/odoo`. Je doet dit door: `ln -s prod/docker/{.??,}* .`
uit te voeren.

7. Installeer docker en docker-compose. Je kan dit doen door
`sudo ./install_docker.sh` uit te voeren. Als dit scriptje faalt,
bekijk documentatie voor docker en docker-compose. Als je gebruiker niet root is
voer je dit commando uit `sudo adduser $USER docker` en log je in en uit.

8. Valideer of `docker` en `docker-compose` correct werken. Je kan dit doen met:
`docker run --rm hello-world` en `docker-compose -h`.

9. Voeg de somko docker repo toe. Je doet dit met: `docker login docker.somko.be`.
Login gegevens voor deze server vind je in: `Technical/docker.somko.be.txt`

10. Voer `docker-compose up -d` uit. En spam de domain adressen tot dat het
certificaat valid is.
