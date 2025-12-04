### Backup Script
```bash
#!/bin/bash
HOST='localhost'
DAYS_TO_KEEP=30   # 0 to keep forever
GZIP=1            # 1 = Compress | 0 = No Compress
BACKUP_PATH='/data/mysql-backup' # change this to which location you want!
#----------------------------------------

# Create the backup folder
if [ ! -d $BACKUP_PATH ]; then
  mkdir -p $BACKUP_PATH
fi

# Get list of database names
databases=$(mysql -e "SHOW DATABASES;" | awk '{if(NR>1) print}')

# Databases to skip. Update this to db you want to skip
skip_databases=('information_schema' 'performance_schema' 'mysql' 'sys' 'world' 'ahhh' 'bbbbb' 'lol' 'zzzz', 'wtf')

for db in $databases; do
  skip=false
  case "${skip_databases[@]}" in *"$db"*) skip=true ;; esac

  if [ "$skip" = true ]; then
    echo "Skipping database: $db"
    continue
  fi

  date=$(date -I)
  if [ "$GZIP" -eq 0 ] ; then
    echo "Backing up database: $db without compression"
    mysqldump -u $USER  -h $HOST --databases $db > $BACKUP_PATH/$(date +%F_%H:%M:%S)-$db.sql
  else
    echo "Backing up database: $db with compression"
    mysqldump -u $USER  -h $HOST --databases $db | gzip -c > $BACKUP_PATH/$(date +%F_%H-%M-%S)-$db.gz
  fi
done

# Delete old backups
if [ "$DAYS_TO_KEEP" -gt 0 ] ; then
  echo "Deleting backups older than $DAYS_TO_KEEP days"
  find $BACKUP_PATH/* -mtime +$DAYS_TO_KEEP -exec rm {} \;
fi
```


### Sync to S3
- Required `s3cmd`. Install it if the host is Ubuntu: `apt install s3cmd`
- Config file s3cmd: `~/.s3cfg`
```
[default]
access_key = ACCESS_KEY_HERE
secret_key = SECRET_KEY_HERE
host_base = https://s3.amazon.com
host_bucket = https://s3.amazon.com
use_https = True
# check_ssl_certificate = False. # Optional
```
- Script for sync to S3, note: this is not optimized, only useful in scenarios where you don't have permission for sync, only put the object.
If you have enough permissions, remove the loop and change the command to sync.
```bash
#!/bin/bash

# Config
LOCAL_DIR="/data/mysql-backup"
S3_BUCKET="s3://mysql-backup"
LOG_FILE="/var/log/s3-backup.log"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

if [ ! -d "$LOCAL_DIR" ]; then
    log "ERROR: Directory $LOCAL_DIR not found."
    exit 1
fi

log "Starting backup from $LOCAL_DIR to $S3_BUCKET"

# Loop through each file.
find "$LOCAL_DIR" -type f | while read -r file; do
    # Get relative path
    relative_path="${file#$LOCAL_DIR/}"
    
    log "Uploading: $relative_path"
    
    if s3cmd put "$file" "$S3_BUCKET/$relative_path" 2>&1 | tee -a "$LOG_FILE"; then
        log "OK: $relative_path"
    else
        log "FAILED: $relative_path"
    fi
done

log "Backup completed"
```
