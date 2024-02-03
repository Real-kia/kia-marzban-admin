#!/bin/bash

# Function to display the menu
show_menu() {
    clear
    echo " .----------------.  .----------------.  .----------------. "
    echo "| .--------------. || .--------------. || .--------------. |"
    echo "| |  ___  ____   | || |     _____    | || |      __      | |"
    echo "| | |_  ||_  _|  | || |    |_   _|   | || |     /  \     | |"
    echo "| |   | |_/ /    | || |      | |     | || |    / /\ \    | |"
    echo "| |   |  __'.    | || |      | |     | || |   / ____ \   | |"
    echo "| |  _| |  \ \_  | || |     _| |_    | || | _/ /    \ \_ | |"
    echo "| | |____||____| | || |    |_____|   | || ||____|  |____|| |"
    echo "| |              | || |              | || |              | |"
    echo "| '--------------' || '--------------' || '--------------' |"
    echo " '----------------'  '----------------'  '----------------' "
    echo
    echo
    echo  youtube.com/@Real_KiaTech  
    echo  t.me/RealKiaTech
    echo
    echo
    echo
    echo
    echo kia marzban admin bot
    echo
    echo
    echo "Please select an option:"
    echo "1) Install"
    echo "2) Update"
    echo "3) Uninstall"
    echo "4) Status"
    echo "5) Restart"
    echo "0) Exit"
}
   

# Function to read the user's choice
read_choice() {
    local choice
    read -p "Enter choice [1 - 4]: " choice
    case $choice in
        1) install_function ;;
        2) update_function ;;
        3) uninstall_function ;;
        4) status_function ;;
        5) restart_function ;;
        0) exit 0 ;;
        *) echo -e "Error: Invalid option..." && sleep 2
    esac
}


update_function() {
  if [ -d "kia-marzban-admin" ]; then
    cp kia-marzban-admin/config.json .
    
    rm -rf kia-marzban-admin
    
    git clone https://github.com/Real-kia/kia-marzban-admin
    
    mv config.json kia-marzban-admin/
    
    sudo systemctl restart kiamarzbanbot.service
    
    echo "Update completed successfully."
  else
    echo "Error: Could not find the 'kia-marzban-admin' folder."
  fi
}


restart_function() {
    echo "restarting"
    sleep 3
    sudo systemctl restart kiamarzbanbot.service
    echo "restart completed successfully."
    sleep 3
}


install_function() {
    echo "Updating the server..."
    sudo apt-get update 
    echo "Installing Python and pip..."
    sudo apt-get install -y python3 python3-pip

    echo "Installing aiogram 2.25.1 and requests..."
    pip3 install aiogram==2.25.1 requests
    sudo apt-get install git
    git clone https://github.com/Real-kia/kia-marzban-admin

    # Ask for user input and store the values in variables
    read -p "Enter bot token: " bot_token
    read -p "Enter admin chat ID (number): " admin_chat_id
    read -p "Enter panel address: " panel_address
    read -p "Enter panel username: " panel_username
    read -sp "Enter panel password: " panel_pass
    echo

    # Ask for dev_version and convert y/n to true/false
    while true; do
        read -p "Is this a development version? (y/n): " yn
        case $yn in
            [Yy]* ) dev_version=true; break;;
            [Nn]* ) dev_version=false; break;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    # Create config.json file with the provided information
    echo "Creating config.json file..."
    cat > kia-marzban-admin/config.json << EOF
{
    "bot_token": "$bot_token",
    "admin_chat_id": $admin_chat_id,
    "panel_address": "$panel_address",
    "panel_username": "$panel_username",
    "panel_pass": "$panel_pass",
    "dev_version": $dev_version
}
EOF
    # Get the current directory (assuming the install script is in the same directory as the bot script)
    local bot_dir=$(pwd)
    local bot_script="main.py" # Replace with your bot script's name

    # Create a systemd service file for the bot
    echo "Creating a systemd service for the bot..."
    cat << EOF | sudo tee /etc/systemd/system/kiamarzbanbot.service
[Unit]
Description=Kia Marzban Bot Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$bot_dir/kia-marzban-admin
ExecStart=/usr/bin/python3 $bot_dir/kia-marzban-admin/$bot_script
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Reload the systemd daemon to apply new changes
    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload

    # Enable the bot service to start on boot
    echo "Enabling the bot service to start on boot..."
    sudo systemctl enable kiamarzbanbot.service

    # Start the bot service
    echo "Starting the bot service..."
    sudo systemctl start kiamarzbanbot.service

    echo "Bot service is active and running."
}





uninstall_function() {
    echo "Uninstallation started..."

    # Stop the service if it's running
    sudo systemctl stop kiamarzbanbot.service

    # Disable the service to prevent it from starting on boot
    sudo systemctl disable kiamarzbanbot.service

    # Remove the service file
    sudo rm /etc/systemd/system/kiamarzbanbot.service

    # Reload the systemd daemon to apply changes
    sudo systemctl daemon-reload

    # Optionally, reset the failed state of the unit, if any
    sudo systemctl reset-failed

    echo "Uninstallation completed successfully."
    sleep 3
}

status_function() {
    echo "Checking the status of the bot service..."
    # Use systemctl to check the status of the service
    sudo systemctl status kiamarzbanbot.service --no-pager
    sleep 10
}


# Main logic - infinite loop
while true
do
    show_menu
    read_choice
done
