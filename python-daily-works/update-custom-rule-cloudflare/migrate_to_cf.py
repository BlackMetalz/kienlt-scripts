#!/usr/bin/env python3
"""
migrate_to_cf.py
----------------
Read text file containing list of IP/CIDR (1 IP per line),
create 1 Cloudflare WAF Custom Rule in format:
  ip.src in {1.2.3.4 5.6.7.8 ...} → skip (allow)

Usage:
    python migrate_to_cf.py --input ips.txt --rule-name "allow home"
    python migrate_to_cf.py --input ips.txt --rule-name "allow home" --dry-run

Env:
    CF_API_TOKEN   Cloudflare API token
    CF_ZONE_ID     Zone ID (Dashboard → domain → Overview → right side)
"""

import os
import sys
import json
import logging
import argparse
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

CF_API_TOKEN = os.getenv("CF_API_TOKEN", "")
CF_ZONE_ID   = os.getenv("CF_ZONE_ID",   "")
CF_BASE      = "https://api.cloudflare.com/client/v4"


def load_ips(path: str) -> list[str]:
    ips = []
    with open(path) as f:
        for line in f:
            ip = line.strip()
            if ip and not ip.startswith("#"):
                ips.append(ip)
    return list(dict.fromkeys(ips))  # dedupe, preserve order


def build_expression(ips: list[str]) -> str:
    """
    CF WAF expression — use `in {}` for both single IP and CIDR,
    more concise than using eq for each one.
    """
    ip_list = " ".join(ips)
    return f"ip.src in {{{ip_list}}}"


class CloudflareClient:
    def __init__(self):
        if not CF_API_TOKEN:
            raise RuntimeError("CF_API_TOKEN is not set.")
        if not CF_ZONE_ID:
            raise RuntimeError("CF_ZONE_ID is not set.")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type":  "application/json",
        })

    def get_or_create_ruleset(self) -> str:
        url = f"{CF_BASE}/zones/{CF_ZONE_ID}/rulesets"
        resp = self.session.get(url)
        resp.raise_for_status()
        for rs in resp.json().get("result", []):
            if rs.get("phase") == "http_request_firewall_custom":
                log.info(f"Existing Ruleset: {rs['id']}")
                return rs["id"]

        log.info("Creating new WAF custom ruleset...")
        resp = self.session.post(url, json={
            "name": "Custom Firewall Rules",
            "kind": "zone",
            "phase": "http_request_firewall_custom",
            "rules": [],
        })
        data = resp.json()
        if not data.get("success"):
            raise RuntimeError(f"Failed to create ruleset: {data.get('errors')}")
        return data["result"]["id"]

    def append_rule(self, ruleset_id: str, name: str, expression: str, action: str) -> dict:
        url = f"{CF_BASE}/zones/{CF_ZONE_ID}/rulesets/{ruleset_id}/rules"
        payload = {
            "description": name,
            "expression":  expression,
            "action":      action,
            "enabled":     True,
        }
        if action == "skip":
            payload["action_parameters"] = {"ruleset": "current"}

        resp = self.session.post(url, json=payload)
        data = resp.json()
        if not data.get("success"):
            raise RuntimeError(f"CF API error: {data.get('errors')}")
        rules = data["result"].get("rules", [])
        return rules[-1] if rules else data["result"]


def main():
    parser = argparse.ArgumentParser(description="Push IP list → Cloudflare WAF Custom Rule")
    parser.add_argument("--input",      required=True,  help="Text file containing IP/CIDR, 1 IP per line")
    parser.add_argument("--rule-name",  default="allow list", help="Rule name on CF (default: 'allow list')")
    parser.add_argument("--action",     choices=["skip", "block", "log"], default="skip",
                        help="Action when match (default: skip = allow)")
    parser.add_argument("--ruleset-id", default="",     help="Existing Ruleset ID, skip if you want to auto-detect")
    parser.add_argument("--dry-run",    action="store_true", help="Do not push, only print the expression")
    args = parser.parse_args()

    ips = load_ips(args.input)
    if not ips:
        log.error("IP file is empty or invalid.")
        sys.exit(1)

    expression = build_expression(ips)

    print(f"\n  Rule name  : {args.rule_name}")
    print(f"  Total IPs  : {len(ips)}")
    print(f"  Action     : {args.action}")
    print(f"  Expression :\n    {expression}\n")

    if args.dry_run:
        log.info("[DRY-RUN] Not pushing to CF.")
        return

    cf = CloudflareClient()
    ruleset_id = args.ruleset_id or cf.get_or_create_ruleset()

    result = cf.append_rule(ruleset_id, args.rule_name, expression, args.action)
    log.info(f"✓ CF rule created successfully! ID: {result.get('id')}")
    print(f"\n  → https://dash.cloudflare.com/zones/{CF_ZONE_ID}/security/waf/custom-rules\n")


if __name__ == "__main__":
    main()