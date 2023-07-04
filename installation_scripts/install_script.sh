#!/bin/bash

# Specify the folder name
folder_name="../database"

if [ -d "$folder_name" ]; then
    echo "Folder '$folder_name' already exists."
else
    # Create the folder
    if mkdir "$folder_name"; then
        echo "Folder '$folder_name' created successfully."
    else
        echo "Failed to create folder '$folder_name'."
        exit 1
    fi
fi

echo "Installing project prerequisites..."
if pip install -r project_prerequisiter.txt; then
    echo "Prerequisites installed successfully."
else
    echo "Failed to install prerequisites."
    exit 1
fi

echo "Installing Nginx..."
if apt-get install nginx; then
    echo "Nginx installed successfully."
else
    echo "Failed to install Nginx."
    exit 1
fi

echo "Starting Nginx..."
if systemctl start nginx; then
    echo "Nginx started successfully."
else
    echo "Failed to start Nginx."
    exit 1
fi

echo "Enabling Nginx..."
if systemctl enable nginx; then
    echo "Nginx enabled successfully."
else
    echo "Failed to enable Nginx."
    exit 1
fi

echo "Copying stock_data_collector.service..."
if cp -r /home/ubuntu/StockMarket/ /etc/systemd/system/stock_data_collector.service; then
    echo "stock_data_collector.service copied successfully."
else
    echo "Failed to copy stock_data_collector.service."
    exit 1
fi

echo "Copying stock_data_collector.timer..."
if cp -r /home/ubuntu/StockMarket/ /etc/systemd/system/stock_data_collector.timer; then
    echo "stock_data_collector.timer copied successfully."
else
    echo "Failed to copy stock_data_collector.timer."
    exit 1
fi

echo "Copying stock_market_flask.service..."
if cp -r /home/ubuntu/StockMarket/ /etc/systemd/system/stock_market_flask.service; then
    echo "stock_market_flask.service copied successfully."
else
    echo "Failed to copy stock_market_flask.service."
    exit 1
fi

echo "Setting ownership and permissions..."
if chown -R root:www-data /home/ubuntu/StockMarket && chmod -R 775 /home/ubuntu/StockMarket; then
    echo "Ownership and permissions set successfully."
else
    echo "Failed to set ownership and permissions."
    exit 1
fi

echo "Reloading systemd daemon..."
if systemctl daemon-reload; then
    echo "Systemd daemon reloaded successfully."
else
    echo "Failed to reload systemd daemon."
    exit 1
fi

echo "Enabling stock_data_collector.service..."
if systemctl enable stock_data_collector.service; then
    echo "stock_data_collector.service enabled successfully."
else
    echo "Failed to enable stock_data_collector.service."
    exit 1
fi

echo "Enabling stock_data_collector.timer..."
if systemctl enable stock_data_collector.timer; then
    echo "stock_data_collector.timer enabled successfully."
else
    echo "Failed to enable stock_data_collector.timer."
    exit 1
fi

echo "Enabling stock_market_flask.service..."
if systemctl enable stock_market_flask.service; then
    echo "stock_market_flask.service enabled successfully."
else
    echo "Failed to enable stock_market_flask.service."
    exit 1
fi

echo "Starting stock_data_collector.service..."
if systemctl start stock_data_collector.service; then
    echo "stock_data_collector.service started successfully."
else
    echo "Failed to start stock_data_collector.service."
    exit 1
fi

echo "Starting stock_data_collector.timer..."
if systemctl start stock_data_collector.timer; then
    echo "stock_data_collector.timer started successfully."
else
    echo "Failed to start stock_data_collector.timer."
    exit 1
fi

echo "Starting stock_market_flask.service..."
if systemctl start stock_market_flask.service; then
    echo "stock_market_flask.service started successfully."
else
    echo "Failed to start stock_market_flask.service."
    exit 1
fi

echo "Copying nginx_flask.conf to /etc/nginx/conf.d/nginx_flask.conf..."
if cp nginx_flask.conf /etc/nginx/conf.d/nginx_flask.conf; then
    echo "nginx_flask.conf copied successfully."
else
    echo "Failed to copy nginx_flask.conf."
    exit 1
fi

echo "Checking Nginx configuration for errors..."
if nginx -t; then
    echo "Nginx configuration test passed."
else
    echo "Nginx configuration test failed."
    exit 1
fi

echo "Restarting Nginx..."
if systemctl restart nginx; then
    echo "Nginx restarted successfully."
else
    echo "Failed to restart Nginx."
    exit 1
fi

echo "Starting Stock Data Collection"