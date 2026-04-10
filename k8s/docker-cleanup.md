### Cleanup for RKE with Docker...

Remember to set this in `/etc/docker/daemon.json`
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "500m",
    "max-file": "3",
    "compress": "true"
  }
}
```

```bash
#!/bin/bash
# Script truncate Docker container json.log nếu > 1GB
# Chạy với root hoặc sudo

LOG_DIR="/var/lib/docker/containers"
MAX_SIZE=$((1 * 1024 * 1024 * 1024))   # 1GB in bytes

echo "=== Docker Log Truncate Script (Max 1GB) ==="
echo "Thời gian: $(date)"
echo "Đang kiểm tra các file log lớn hơn 1GB..."

find "$LOG_DIR" -name "*-json.log" -print0 | while IFS= read -r -d '' logfile; do
    size=$(stat -c %s "$logfile" 2>/dev/null || stat -f %z "$logfile" 2>/dev/null)
    
    if [ -n "$size" ] && [ "$size" -gt "$MAX_SIZE" ]; then
        size_human=$(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "$((size/1024/1024/1024))G")
        container_id=$(basename "$(dirname "$logfile")")
        
        echo "→ Truncate file lớn: $logfile (${size_human})"
        echo "  Container ID: $container_id"
        
        # Truncate về 0 byte (an toàn nhất với Docker)
        truncate -s 0 "$logfile"
        
        echo "  ✓ Đã truncate xong - Giải phóng ${size_human}"
    fi
done

echo "=== Hoàn tất! ==="
df -h /var/lib/docker
```
