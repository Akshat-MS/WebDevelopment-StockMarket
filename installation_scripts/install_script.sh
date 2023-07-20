#!/bin/bash
# ________________________Folders Creation required for the project____________________
# database folder.
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

# log folder
folder_name="../logs"

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

# Activate the virtual environment
echo "Reloading systemd daemon..."
if source /home/ubuntu/StockMarket/venv/bin/activate; then
    echo "Python Virtual environment activated successfully."
else
    echo "Failed to activate Python virtual Environment."
    exit 1
fi

# ______________________Project Prerequisites____________________
# Installing Prerequisites packages required for the project
echo "Installing project prerequisites..."
if pip install -r project_prerequisiter.txt; then
    echo "Prerequisites installed successfully."
else
    echo "Failed to install prerequisites."
    exit 1
fi

# ________________________Nginx____________________
# Steps to be followed to install Nginx Web server. 
echo "Installing Nginx..."
if sudo apt-get install nginx; then
    echo "Nginx installed successfully."
else
    echo "Failed to install Nginx."
    exit 1
fi

# Start Nginx
echo "Starting Nginx..."
if sudo systemctl start nginx; then
    echo "Nginx started successfully."
else
    echo "Failed to start Nginx."
    exit 1
fi

# Enable Nginx
echo "Enabling Nginx..."
if sudo systemctl enable nginx; then
    echo "Nginx enabled successfully."
else
    echo "Failed to enable Nginx."
    exit 1
fi

# __________________________Copy Systemd Services___________________________
# Copy the stock_job_logger.service file to /etc/systemd/system/
echo "Copying stock_job_logger.service..."
if sudo cp /home/ubuntu/StockMarket/config_files/stock_job_logger.service /etc/systemd/system/stock_job_logger.service; then
    echo "stock_job_logger.service copied successfully."
else
    echo "Failed to copy stock_job_logger.service."
    exit 1
fi

# Copy the stock_job_logger.timer file to /etc/systemd/system/
echo "Copying stock_job_logger.timer..."
if sudo cp /home/ubuntu/StockMarket/config_files/stock_job_logger.timer /etc/systemd/system/stock_job_logger.timer; then
    echo "stock_job_logger.timer copied successfully."
else
    echo "Failed to copy stock_job_logger.timer."
    exit 1
fi

# Copy the stock_job_exec_daily.service file to /etc/systemd/system/
echo "Copying stock_job_exec_daily.service..."
if sudo cp /home/ubuntu/StockMarket/config_files/stock_job_exec_daily.service /etc/systemd/system/stock_job_exec_daily.service; then
    echo "stock_job_exec_daily.service copied successfully."
else
    echo "Failed to copy stock_job_exec_daily.service."
    exit 1
fi

# Copy the stock_job_exec_daily.timer file to /etc/systemd/system/
echo "Copying stock_job_exec_daily.timer..."
if sudo cp /home/ubuntu/StockMarket/config_files/stock_job_exec_daily.timer /etc/systemd/system/stock_job_exec_daily.timer; then
    echo "stock_job_exec_daily.timer copied successfully."
else
    echo "Failed to copy stock_job_exec_daily.timer."
    exit 1
fi

# Copy the stock_market_flask.service file to /etc/systemd/system/
echo "Copying stock_market_flask.service..."
if sudo cp /home/ubuntu/StockMarket/config_files/stock_market_flask.service /etc/systemd/system/stock_market_flask.service; then
    echo "stock_market_flask.service copied successfully."
else
    echo "Failed to copy stock_market_flask.service."
    exit 1
fi

#_______________________________Permissions___________________________________
# Setting ownership and permissions. Config as a group www-data 
echo "Setting ownership and permissions..."
if sudo chown -R ubuntu:www-data /home/ubuntu/StockMarket/ && sudo chmod -R 775 /home/ubuntu/StockMarket/; then
    echo "Ownership and permissions set successfully."
else
    echo "Failed to set ownership and permissions."
    exit 1
fi

# _____________Loading, Re-loading, enabling and starting of systemd services_________________
# Reloading systemd daemon
echo "Reloading systemd daemon..."
if sudo systemctl daemon-reload; then
    echo "Systemd daemon reloaded successfully."
else
    echo "Failed to reload systemd daemon."
    exit 1
fi

# Enabling stock_job_logger.service
echo "Enabling stock_job_logger.service..."
if sudo systemctl enable stock_job_logger.service; then
    echo "stock_job_logger.service enabled successfully."
else
    echo "Failed to enable stock_job_logger.service."
    exit 1
fi

# Enabling stock_job_logger.timer
echo "Enabling stock_job_logger.timer..."
if sudo systemctl enable stock_job_logger.timer; then
    echo "stock_job_logger.timer enabled successfully."
else
    echo "Failed to enable stock_job_logger.timer."
    exit 1
fi

# Enabling stock_job_exec_daily.service
echo "Enabling stock_job_exec_daily.service..."
if sudo systemctl enable stock_job_exec_daily.service; then
    echo "stock_job_exec_daily.service enabled successfully."
else
    echo "Failed to enable stock_job_exec_daily.service."
    exit 1
fi

# Enabling stock_job_exec_daily.timer
echo "Enabling stock_job_exec_daily.timer..."
if sudo systemctl enable stock_job_exec_daily.timer; then
    echo "stock_job_exec_daily.timer enabled successfully."
else
    echo "Failed to enable stock_job_exec_daily.timer."
    exit 1
fi

# Enabling stock_market_flask.service
echo "Enabling stock_market_flask.service..."
if sudo systemctl enable stock_market_flask.service; then
    echo "stock_market_flask.service enabled successfully."
else
    echo "Failed to enable stock_market_flask.service."
    exit 1
fi

# Starting stock_job_logger.service
echo "Starting stock_job_logger.service..."
if sudo systemctl start stock_job_logger.service; then
    echo "stock_job_logger.service started successfully."
else
    echo "Failed to start stock_job_logger.service."
    exit 1
fi

# Starting stock_job_logger.timer
echo "Starting stock_job_logger.timer..."
if sudo systemctl start stock_job_logger.timer; then
    echo "stock_job_logger.timer started successfully."
else
    echo "Failed to start stock_job_logger.timer."
    exit 1
fi

# Starting stock_job_exec_daily.service
echo "Starting stock_job_exec_daily.service..."
if sudo systemctl start stock_job_exec_daily.service; then
    echo "stock_job_exec_daily.service started successfully."
else
    echo "Failed to start stock_job_exec_daily.service."
    exit 1
fi

# Starting stock_job_exec_daily.timer
echo "Starting stock_job_exec_daily.timer..."
if sudo systemctl start stock_job_exec_daily.timer; then
    echo "stock_job_exec_daily.timer started successfully."
else
    echo "Failed to start stock_job_exec_daily.timer."
    exit 1
fi

# Starting stock_market_flask.service
echo "Starting stock_market_flask.service..."
if sudo systemctl start stock_market_flask.service; then
    echo "stock_market_flask.service started successfully."
else
    echo "Failed to start stock_market_flask.service."
    exit 1
fi

# ________________Configure Nginx based on Project requirement___________________
# Copy nginx_flask.conf to /etc/nginx/conf.d/
echo "Copying nginx_flask.conf to /etc/nginx/conf.d/nginx_flask.conf..."
if sudo cp /home/ubuntu/StockMarket/config_files/nginx_flask.conf /etc/nginx/conf.d/nginx_flask.conf; then
    echo "nginx_flask.conf copied successfully."
else
    echo "Failed to copy nginx_flask.conf."
    exit 1
fi

# Test nginx configuration.
echo "Checking Nginx configuration for errors..."
if sudo nginx -t; then
    echo "Nginx configuration test passed."
else
    echo "Nginx configuration test failed."
    exit 1
fi

# Restart nginx configuration.
echo "Restarting Nginx..."
if sudo systemctl restart nginx; then
    echo "Nginx restarted successfully."
else
    echo "Failed to restart Nginx."
    exit 1
fi

#Start the collection.
echo "Starting Stock Data Collection"