## Protect your website and API from malicious traffic with custom rules. Configure mitigation criteria and actions, or explore templates, for better security.

Automation for easy life, my use case, export IPs from secGroup Openstack then migrate to Cloudflare, it is about ~200 ip.

### Setup API Token
Permissions: Zone.Zone WAF
Resource: Your site.

### Get your fucking ZONE ID
Section API in Overview of your site.

### Ruleset ID
Create new rule then save it. After that edit it again, you will see a section "Save with API call", ruleset ID will be there

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