#! /bin/bash
# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

echo "Rebuilding global modules..."

# check if poetry is installed
if ! command -v poetry &> /dev/null
then
    echo -e "${BRed}Poetry could not be found${Color_Off}"
    exit
fi

# get current version from poetry
POETRY_VERSION="$(poetry version | awk '{print $2}')"

# Print current version in bold and green color
echo -e "${BGreen}Current version is $POETRY_VERSION${Color_Off}"

# ask new version
echo -e "${BBlue}Enter new version: ${Color_Off}"
read NEW_VERSION

# Print new version in bold and green color
echo -e "${BBlue}New version is $NEW_VERSION${Color_Off}"

# check if new version is valid
if ! [[ $NEW_VERSION =~ ^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}(\.[0-9]{1,2})?$ ]]; then
    echo -e "${BRed}New version is not valid${Color_Off}"
    exit
fi

# check if new version is greater than current version
if [ "$(printf '%s\n' "$NEW_VERSION" "$POETRY_VERSION" | sort -V | head -n1)" != "$POETRY_VERSION" ]; then
    echo -e "${BRed}New version is not greater than current version${Color_Off}"
    exit
fi

poetry version $NEW_VERSION

# for all services in parent directory do poetry update
for d in ../*/ ; do
    echo -e "${BGreen}Updating $d${Color_Off}"
    cd $d
        poetry update global_modules
    done

    cd ../global_modules

echo -e "${BGreen}Done!${Color_Off}"