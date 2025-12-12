$ErrorActionPreference = 'Stop'
$wc = New-Object System.Net.WebClient

$root = Split-Path -Parent $PSScriptRoot
$img = Join-Path $root 'images'

$u1 = 'https://api.qrserver.com/v1/create-qr-code/?size=600x600&data=https%3A%2F%2Ftadweer-tech-sy.org'
$u2 = 'https://api.qrserver.com/v1/create-qr-code/?size=600x600&data=https%3A%2F%2Fwww.instagram.com%2Ftadweer_sy%3Figsh%3DeHZ5dHh3azJsNzhs'
$u3 = 'https://api.qrserver.com/v1/create-qr-code/?size=600x600&data=https%3A%2F%2Fwww.facebook.com%2Fprofile.php%3Fid%3D61577997235876'

$wc.DownloadFile($u1, (Join-Path $img 'qr_website.png'))
$wc.DownloadFile($u2, (Join-Path $img 'qr_instagram.png'))
$wc.DownloadFile($u3, (Join-Path $img 'qr_facebook.png'))
Write-Host 'QR images saved.'
