## Protect your website and API from malicious traffic with custom rules. Configure mitigation criteria and actions, or explore templates, for better security.

Automation for easy life, my use case, export IPs from secGroup Openstack then migrate to Cloudflare, it is about ~200 ip.

### Get your fucking ZONE ID
```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=your-domain-here" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" | python3 -m json.tool | grep '"id"' | head -1
```

### Deploy it!
```bash
export CF_API_TOKEN="..."
export CF_ZONE_ID="..."
export CF_RULE_NAME="..."
export CF_RULESET_ID="..."

# Dry run
python migrate_to_cf.py --input ips.txt --rule-name $CF_RULE_NAME --dry-run

# For real xD
python migrate_to_cf.py --input ips.txt --rule-name "$CF_RULE_NAME" --ruleset-id $CF_RULESET_ID
```