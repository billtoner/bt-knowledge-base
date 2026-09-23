# password-strategy

Personal password strategy for Apple Passwords (iCloud). Goal: easy for me, hard for others, no reuse. Not a tool — a decision cheat-sheet.

**Tags:** passwords · secrets

## The two-tier model

- **Tier 0 — memorize ~4, as passphrases** (4-5 random words, e.g. `copper-lantern-vivid-otter`): Apple ID password, Mac login, primary email, phone passcode. 2FA on all. These unlock everything else, so they get the most care.
- **Tier 1 — everything else, never memorized:** every website login = Apple's **suggested strong password**, filled by AutoFill. The gibberish is the point — unguessable, and one site's breach reveals nothing about another.

## Generated random vs. passphrase — which to use

- **AutoFill will be there** (normal sites/apps) → **generated random**. ~95% of accounts. Never typed, so unmemorable is fine.
- **You'll sometimes type it by hand** (smart TV, game console, someone else's computer, Apple ID on a fresh device) → **passphrase** (random words): strong *and* typeable.

### Satisfying composition rules (upper/number/special)

- **Tier 1 — let the generator do it.** Apple's suggestion (`hupvEw-2kimyb-Zt9dfp`) already has upper+lower+number+hyphen, satisfying nearly all sites. Picky site (bans hyphen / needs a symbol) → tap suggestion → **"Other Options"** or hand-edit, then **save whatever the site accepted**. Never typed, so ugliness doesn't matter.
- **Tier 0 — passphrase + a memorable "compliance tail":** 3-4 words, Capitalize each first letter (upper+lower), append a digit + safe symbol. E.g. `Harbor-Mango-Quilt-9!`, `Copper-Lantern-Otter-4$`. Meets upper/lower/number/special/length everywhere. Safe symbols: `! # $` and `-`; avoid `@` space quote `%` `^` (often rejected). Keep the 4 word-sets distinct; a shared tail like `-9!` is fine (entropy is in the words).

### Why NOT a shared-base pattern (`Base-amzn`, `Base-goog`…)

Better than reuse, but **derivable**: one site breach/phish exposes `Base-amzn` → attacker computes every other site. That re-creates the cascade you're avoiding. And it's moot — the manager remembers Tier 1 for you, so a pattern solves a problem you no longer have. Random for Tier 1; independent passphrases for Tier 0.

## Duplicate / reuse cleanup — by priority, not volume

Two separate problems:
- **Duplicate entries** (same site twice, from the 3-vault merge) → Apple Passwords → Security flags them → **merge**.
- **Reused passwords** → fix highest-value first, ignore the long tail:
  1. email  2. Apple ID + Google  3. banks/brokerage/anything with money or SSN  4. Amazon / saved-card sites  5. reset hubs / holds others' data

Per account: log in → change password → accept Apple's strong suggestion → enable 2FA. Then **"touch it, fix it"**: rotate a reused password the next time you happen to log into that site. The list drains itself over months; no marathon.

## Force-multipliers

- **2FA beats raw password strength** on email + Apple ID + bank. Apple Passwords can store the TOTP codes too.
- **Passkeys** = endgame. Where offered (Google, GitHub, Amazon…), create one: stored in Apple Passwords, Face/Touch ID to use, phishing-proof, nothing to reuse or leak.

## Emergency / estate access (so my wife isn't locked out)

Biometrics are NOT the gate — Face/Touch ID is just a local unlock shortcut; the real gate is Apple ID password + device passcode, and biometric failure always falls back to the passcode. So no one is *permanently* locked out by a fingerprint. Three mechanisms, use all three:

- **Shared Group** (Passwords app → "Share with Family") — best for ongoing access. Wife uses her *own* Apple ID + her own biometrics on her own devices; share all or a chosen subset. Syncs across her devices.
- **Legacy Contact** (Apple ID setting) — posthumous access. She gets an access key now; with that + a death certificate, Apple grants access to the account incl. iCloud Keychain.
- **Break-glass envelope** — Apple ID password + device passcodes written in the estate/legal docs or a fireproof safe. Always works, biometrics irrelevant.

Note: enrolling a 2nd fingerprint (Mac Touch ID up to 3, iPhone up to 5) or a Face ID "alternate appearance" only adds *local device* unlock — it does NOT grant vault access to another person the way a Shared Group or Legacy Contact does. Don't rely on it for spousal access.
