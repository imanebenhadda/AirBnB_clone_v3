#!/usr/bin/env bash
#  a Bash script that sets up your web servers for the deployment of web_static
apt-get -y update
apt-get install -y nginx
ufw allow 'Nginx HTTP'
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
for directory in "${directories[@]}"; do
	if [ ! -d "$directory" ]; then
	    mkdir -p "$directory"
	else
		continue
	fi
done
sudo tee /data/web_static/releases/test/index.html <<EOT
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple HTML Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
    </style>
</head>
<body>

    <h1>Welcome to My test HTML Page</h1>

    <p>This is a basic HTML page.</p>
    <h2>My favorite programming languages are:</h2>
    <ul>
        <li>C</li>
        <li>Python</li>
        <li>HTML (for web markup)</li>
        <li>CSS (for web styling)</li>
        <li>SQL</li>
        <li>JavaScript (js)</li>
    </ul>

</body>
</html>
EOT
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
echo "Ceci n'est pas une page" | sudo tee /data/web_static/releases/test/404.html
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOT
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /data/web_static/releases/test/;
    index index.html;

    location /redirect_me {
        return 301 http://localhost/new_page;
    }
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
    location /hbnb_static/ {
      alias /data/web_static/releases/test/;
   }
	location / {
      add_header X-Served-By "$(hostname)";
   }
}
EOT
sudo service nginx restart