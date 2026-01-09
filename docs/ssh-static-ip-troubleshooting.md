# SSH Connectivity Issue After VM Restart (GCP)
### Permanent Fix Using Static IP and Single SSH Key

## Context
While working on a Google Cloud Compute Engine VM for the **OpenLakeTx** project, I encountered repeated SSH connection failure after stopping and restarting the VM. This document explains the issue, root cause, step-by-step resolution, and long-term prevention strategy

This mirrors a **real-world cloud operations scenario** commonly faced in production environments.

---

## Problem Statement

After stopping and restarting the VM:
- VS Code Remote SSH failed with **connection timeout**
- Manual SSH returned **permission denied (publickey)**
- VM was reachable via browser SSH only

This caused development downtime and inconsistent access.

---

## Symptoms & Errors Observed
### VS Code Remote SSH
```text
ssh: connect to host <old-ip> port 22: Connection timed out
OfflineError (The connection timed out)
```
### Manual SSH
```text
permission denied (publickey)
```
---

## Root Causes Identified
### 1. Ephemeral External IP Changed
- GCP assigns **ephemeral IPs** by default
- Stopping the VM released the IP
- SSH configs still pointed to the old IP

### 2. Multiple SSH Keys in Use
- Browser SSH injected `google-ssh` keys
- Local SSH used a different key
- Resulted in authentication mismatch

---

## Resolution (Step-by-Step)

### Step 1: Promote Ephemeral IP to Static
- Navigated to **VPC Network -> IP Addresses**
- Promoted the VM's existing ephemeral IP to **static**
- Ensured IP persistence across VM restarts

Result:
- External IP no longer changes
- SSH configs remain valid

---

### Step 2: Standardize on a Single SSH Key

#### Generate a dedicated key:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/openlaketx_ed25519
```

### Configure VM:
- Removed all exisiting SSH keys
- Added only `openlaketx_ed25519.pub` in VM metdata
- Cleaned `~/.ssh/authorized_keys` on the VM

### Configure local SSH:
```bash
Host linux-workshop-vm
    HostName <STATIC_IP>
    User <vm-user>
    IdentityFile ~/.ssh/openlaketx_ed25519
    IdentitiesOnly yes
```

### Step 3: Validation
- Manual SSH works without password prompt
- VS Code Remote SSH connects reliably
- VM restat does not break connectivity

### Preventive Measures (Best practices)
- Always use static external IPs for long-lived VMs
- Use one SSH key per project
- Avoid mixing browser SSH and local SSH keys
- Use `IdentitiesOnly yes` to prevent key confusion
- Document operational fixes for future reference

### Key Takeaways
This issue reinforced important cloud fundamentals:
- VM lifecycle impacts networking
- SSH failures are often network or identity-related
- Clean, determiinistic setups reduce operational risk
