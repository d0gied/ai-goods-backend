# Reset
$Color_Off = "`e[0m"       # Text Reset

# Regular Colors
$Black = "`e[0;30m"        # Black
$Red = "`e[0;31m"          # Red
$Green = "`e[0;32m"        # Green
$Yellow = "`e[0;33m"       # Yellow
$Blue = "`e[0;34m"         # Blue
$Purple = "`e[0;35m"       # Purple
$Cyan = "`e[0;36m"         # Cyan
$White = "`e[0;37m"        # White

# Bold
$BBlack = "`e[1;30m"       # Black
$BRed = "`e[1;31m"         # Red
$BGreen = "`e[1;32m"       # Green
$BYellow = "`e[1;33m"      # Yellow
$BBlue = "`e[1;34m"        # Blue
$BPurple = "`e[1;35m"      # Purple
$BCyan = "`e[1;36m"        # Cyan
$BWhite = "`e[1;37m"       # White

Write-Host "Rebuilding global modules..."

# check if poetry is installed
if (!(Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "${BRed}Poetry could not be found${Color_Off}"
    exit
}

# get current version from poetry
$POETRY_VERSION = (poetry version | %{ $_.Split(' ')[1] })

# Print current version in bold and green color
Write-Host "${BGreen}Current version is $POETRY_VERSION${Color_Off}"

# ask new version
Write-Host "${BBlue}Enter new version: ${Color_Off}"
$NEW_VERSION = Read-Host

# Print new version in bold and green color
Write-Host "${BBlue}New version is $NEW_VERSION${Color_Off}"

# check if new version is valid
if (!($NEW_VERSION -match "^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}(\.[0-9]{1,2})?$")) {
    Write-Host "${BRed}New version is not valid${Color_Off}"
    exit
}

# check if new version is greater than current version
if ([version]$NEW_VERSION -le [version]$POETRY_VERSION) {
    Write-Host "${BRed}New version is not greater than current version${Color_Off}"
    exit
}

poetry version $NEW_VERSION

# for all services in parent directory do poetry update
Get-ChildItem "../*/" -Directory | ForEach-Object {
    Write-Host "${BGreen}Updating $_${Color_Off}"
    Set-Location $_.FullName
    poetry update global_modules
}

Set-Location "../global_modules"

Write-Host "${BGreen}Done!${Color_Off}"