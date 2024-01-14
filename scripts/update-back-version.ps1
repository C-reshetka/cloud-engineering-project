param($Ip, $Version)

ssh -o StrictHostKeyChecking=accept-new yc-user@$Ip ("sudo docker exec app bash -c '> version ; echo {0} > version'; truncate -s-1 version" -f $Version)