#!/bin/bash -xe

# Log everything to console and file for debugging
exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

# Detect package manager (Amazon Linux 2023 usa dnf, Amazon Linux 2 usa yum)
if command -v dnf >/dev/null 2>&1; then
    PKG="dnf"
else
    PKG="yum"
fi

# Actualizar sistema e instalar Apache
sudo $PKG update -y
sudo $PKG install -y httpd

# Obtener IP local
IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)

# Crear HTML personalizado
cat <<EOF > /var/www/html/index.html
<html>
<head>
    <title>Modern Web App 2025</title>
    <style>
        body {
            margin-top: 40px;
            background-color: #1e1e2f;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
        }
        h1 {
            font-size: 6vw;
            margin-bottom: 10px;
        }
        p {
            font-size: 1.5vw;
        }
        small {
            display: block;
            margin-top: 20px;
            color: #ccc;
        }
    </style>
</head>
<body>
    <h1>Modern Web App - 2025</h1>
    <p>🎉 Congratulations! Your Web Server is Online.</p>
    <small>Pages served from $IP</small>
</body>
</html>
EOF

# Iniciar y habilitar Apache
sudo systemctl enable httpd
sudo systemctl start httpd
