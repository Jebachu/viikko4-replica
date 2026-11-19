#!/usr/bin/env bash
# Hourly pull backup of server A's /var/www/html to server B.
set -u

SRC="ubuntu@192.168.1.245:/var/www/html/"
DEST_ROOT="/srv/backups/www"
KEY="/home/ubuntu/.ssh/backup_ed25519"
LOG="/home/ubuntu/backup.log"
KEEP=48

umask 077
STAMP=$(date '+%Y-%m-%d_%H%M%S')
DEST="$DEST_ROOT/$STAMP"
LATEST=$(ls -1d "$DEST_ROOT"/20* 2>/dev/null | tail -n 1)

LINK_OPT=()
if [ -n "$LATEST" ]; then
    LINK_OPT=(--link-dest="$LATEST")
fi

if rsync -a "${LINK_OPT[@]}" -e "ssh -i $KEY -o BatchMode=yes" "$SRC" "$DEST/"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') SUCCESS backup $STAMP" >> "$LOG"
    # Keep only the newest $KEEP backups
    ls -1d "$DEST_ROOT"/20* | head -n -"$KEEP" | xargs -r rm -rf
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') FAILURE backup $STAMP" >> "$LOG"
    rm -rf "$DEST"
    exit 1
fi
