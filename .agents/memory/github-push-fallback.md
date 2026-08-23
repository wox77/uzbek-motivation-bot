---
name: GitHub push fallback
description: Repository push behavior in this Replit environment when the configured HTTPS remote lacks usable git credentials.
---

When a GitHub integration is attached but `git push` over the HTTPS remote fails authentication, the repository can still be updated through the authenticated GitHub integration proxy using Git blobs, trees, commits, and a branch ref update.

**Why:** The local remote may be configured correctly yet have no interactive GitHub credential helper; asking for a token in chat is neither necessary nor safe.

**How to apply:** Verify the target branch first, create the remote commit against its current tree, update the ref without force, then verify the resulting file and commit through the API.