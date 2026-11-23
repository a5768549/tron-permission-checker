#!/usr/bin/env python3
"""Zero-dependency CLI to inspect TRON (TRC-20) Owner & Active permissions on mainnet."""

import json
import sys
import urllib.request


def check_permissions(address: str) -> dict:
    req = urllib.request.Request(
        "https://api.trongrid.io/wallet/getaccount",
        data=json.dumps({"address": address, "visible": True}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if not data or not data.get("address"):
        return {"address": address, "activated": False, "status": "UNACTIVATED"}

    balance_trx = round(int(data.get("balance", 0)) / 1_000_000, 6)
    owner = data.get("owner_permission") or {"threshold": 1, "keys": [{"address": address, "weight": 1}]}
    actives = data.get("active_permission") or [{"threshold": 1, "keys": [{"address": address, "weight": 1}]}]

    owner_addrs = {k["address"] for k in owner.get("keys", [])}
    active_addrs = {k["address"] for ap in actives for k in ap.get("keys", [])}
    orig_has_ctrl = (address in owner_addrs) or (address in active_addrs)

    if orig_has_ctrl and owner_addrs == {address} and active_addrs == {address}:
        status = "DEFAULT_SINGLE_SIG"
    elif not orig_has_ctrl:
        status = "PERMISSIONS_TRANSFERRED"
    else:
        status = "MULTISIG_SHARED"

    return {
        "address": address,
        "activated": True,
        "balance_trx": balance_trx,
        "status": status,
        "owner_keys": owner.get("keys", []),
        "active_keys": [k for ap in actives for k in ap.get("keys", [])],
        "original_key_has_control": orig_has_ctrl,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_tron_perm.py <TRON_ADDRESS>")
        sys.exit(1)
    result = check_permissions(sys.argv[1].strip())
    print(json.dumps(result, indent=2))
