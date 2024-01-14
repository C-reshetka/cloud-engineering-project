# needs s3cmd https://cloud.yandex.ru/ru/docs/storage/tools/s3cmd

param($Version)

Set-Content -Path ".\version.json" -Value ('{ "Version": "' + $Version + '" }')
s3cmd put version.json s3://comment-service-storage
Remove-Item -Path ".\version.json"