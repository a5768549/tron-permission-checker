# TRON Permission Checker (Multi-Sig Inspector)

A zero-dependency Python 3 CLI tool to inspect live `Owner` and `Active` signing permissions of any TRON (`TRC-20`) address directly from TRON mainnet via TronGrid.

## Why This Matters
- **Detect Multi-Sig Scams**: Malicious wallets sometimes share a seed phrase with modified `Owner`/`Active` permissions so deposits are trapped.
- **Verify Vanity Address Takeover**: TRON natively supports on-chain `AccountPermissionUpdate`. After buying or generating a TRON vanity address and transferring `Owner` and `Active` authority to your hardware/primary wallet, use this tool to confirm the original key has zero remaining authority.

## Usage

```bash
python3 check_tron_perm.py TYourTronAddressHere
```

### Possible Statuses
- `UNACTIVATED`: Brand-new address with no on-chain state yet.
- `DEFAULT_SINGLE_SIG`: Original private key has full signing control.
- `PERMISSIONS_TRANSFERRED`: Original key has been completely removed from both `Owner` and `Active` permissions.
- `MULTISIG_SHARED`: Multiple keys hold signing authority—verify every address listed.

## Web Version & Guides
- Online browser checker (no install required): [TRXVanity Permission Checker](https://trxvanity.xyz/tools/permission-checker)
- Step-by-step TronLink permission transfer walkthrough: [TRON Multi-Sig Transfer Guide](https://trxvanity.xyz/guides/multisig)
- How repeating suffixes stop address poisoning: [Address Poisoning Defense](https://trxvanity.xyz/guides/poisoning)

## License
MIT
