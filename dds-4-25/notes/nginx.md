<link rel='stylesheet' href='markdown9.css'/>

The old static website has been mirrored to /srv/www/datadrivenshipping.com/

nginx sites-enabled
-------------------

    https-dev.datadrivenshipping.com -> ../sites-available/https-dev.datadrivenshipping.com
    http-www.datadrivenshipping.com -> ../sites-available/http-www.datadrivenshipping.com

https (backend)
---------------

    (pending transition to final www subdomain)

http (static site)
------------------

    server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        root /srv/www/datadrivenshipping.com;
        index index.html index.htm;
        default_type text/html;
        server_name www.datadrivenshipping.com;

        location / {
            try_files $uri $uri/ $uri.html /index.html;
        }
    }

SSL
---

SSL files live in /etc/nginx/ssl/

Private key: server.key

CA certificate: DigiCertCA.crt

Bundled signed certificates: bundle.crt

CSR: server.csr

Private key readable only by root, but no passphrase