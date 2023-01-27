FILE_ENV=.env

# Copy .env.example to .env if .env does not exist
if [ -f "$FILE_ENV" ]; then
    echo "Skipping copying .env. File exists already."
else 
    cp .env.example .env
    echo "Copied .env.example to .env."
fi
