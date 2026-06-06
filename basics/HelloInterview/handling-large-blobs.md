# Handling Large Blobs

## Presigned URLs

### Q: What are the different fields in a presigned URL and what do they mean?

```
https://mybucket.s3.amazonaws.com/uploads/user123/video.mp4
?X-Amz-Algorithm=AWS4-HMAC-SHA256
&X-Amz-Credential=AKIAIOSF0DNN7EXAMPLE%2F20240115%2Fus-east-1%2Fs3%2Faws4_request
&X-Amz-Date=20240115T000000Z
&X-Amz-Expires=900
&X-Amz-SignedHeaders=host
&X-Amz-Signature=b2754f5b1c9d7c4b8d4f6e9a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

| Field | Meaning |
|---|---|
| `X-Amz-Algorithm` | Signing algorithm used (AWS4-HMAC-SHA256) |
| `X-Amz-Credential` | URL-encoded: `ACCESS_KEY_ID / date / region / service / terminator` |
| `X-Amz-Date` | Timestamp when the URL was generated (ISO 8601) |
| `X-Amz-Expires` | TTL in seconds (900 = 15 min) — after this the URL is invalid |
| `X-Amz-SignedHeaders` | Which HTTP headers were included in the signature (S3 verifies these match) |
| `X-Amz-Signature` | The actual HMAC-SHA256 cryptographic signature |

### Q: How does S3 verify the signature without the secret key being in the URL?

S3 already has your secret key (from IAM setup). It independently recomputes the signature and checks if it matches.

**Example walkthrough:**

Credentials:
```
Access Key ID:  AKIAIOSF0DNN7EXAMPLE
Secret Key:     wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

1. **Server builds a canonical string** from the request details (method, path, date, expiry, headers):
   ```
   canonicalString = "PUT\n
                      /uploads/user123/video.mp4\n
                      X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...&X-Amz-Date=20240115T000000Z&X-Amz-Expires=900\n
                      host:mybucket.s3.amazonaws.com\n"

   → "PUT\n/uploads/user123/video.mp4\nX-Amz-Algorithm=AWS4-HMAC-SHA256&...\nhost:mybucket.s3.amazonaws.com\n"
   ```

2. **Server derives a signing key** by chaining HMACs — scoped to date, region, and service:
   ```
   step1 = HMAC("AWS4" + "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", "20240115")  →  "kDate:    8a1c2f3d..."
   step2 = HMAC("kDate:    8a1c2f3d...", "us-east-1")                               →  "kRegion:  4e5b6a7c..."
   step3 = HMAC("kRegion:  4e5b6a7c...", "s3")                                      →  "kService: 9d0e1f2a..."
   step4 = HMAC("kService: 9d0e1f2a...", "aws4_request")                            →  "kSigning: 3b4c5d6e..."
   ```

3. **Server signs the canonical string** using the derived signing key:
   ```
   signature = HMAC("kSigning: 3b4c5d6e...", canonicalString)  →  "b2754f5b1c9d7c4b8d..."
   ```

4. **Server embeds the signature in the URL** and returns it to the client:
   ```
   &X-Amz-Signature=b2754f5b1c9d7c4b8d...
   ```

5. **Client uploads directly to S3** using the presigned URL — no credentials needed on the client side.

6. **S3 repeats steps 1–3** using its own stored copy of your secret key:
   ```
   S3 recomputes → "b2754f5b1c9d7c4b8d..."
   Matches X-Amz-Signature?          → YES
   X-Amz-Date + X-Amz-Expires > now? → YES (20240115T000000Z + 900s is still valid)
   → Upload allowed
   ```

The secret key never leaves your server — S3 can verify independently because it already has a copy.

---

## CDN Signed URLs

### Q: What are the different fields in a CloudFront signed URL and what do they mean?

```
https://d123456.cloudfront.net/videos/lecture.mp4
?Expires=1705305600
&Signature=j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3g4h5i6j7k8l9m0
&Key-Pair-Id=APKAIOSF0DNN7EXAMPLE
```

| Field | Meaning |
|---|---|
| `Expires` | Unix timestamp (not TTL like S3) — `1705305600` = Jan 15 2024 00:00:00 UTC |
| `Signature` | RSA signature of the URL + expiry, signed with your private key |
| `Key-Pair-Id` | Tells CloudFront which public key to use to verify the signature |

### Q: How does CloudFront verify the signature? (RSA asymmetric cryptography)

Unlike S3 (which uses symmetric HMAC), CloudFront uses **asymmetric RSA** — signed with a private key, verified with a public key.

**Setup (one time):**
```
You generate a key pair:
  Private key  →  stays on your server (never shared)
  Public key   →  uploaded to CloudFront (Key-Pair-Id = APKAIOSF0DNN7EXAMPLE)
```

**Signing (your server):**

1. **Build the message to sign** from the URL path and expiry:
   ```
   message = "https://d123456.cloudfront.net/videos/lecture.mp4" + "Expires=1705305600"

   → "https://d123456.cloudfront.net/videos/lecture.mp4Expires=1705305600"
   ```

2. **Hash the message** using SHA-1:
   ```
   hash = SHA1("https://d123456.cloudfront.net/videos/lecture.mp4Expires=1705305600")

   → "a3f9bc72e1d84c..."
   ```

3. **Encrypt the hash with your private key** — this is the signature:
   ```
   signature = RSA_ENCRYPT(privateKey, "a3f9bc72e1d84c...")

   → "j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7..."
   ```

4. **Embed in URL** and return to client:
   ```
   ?Expires=1705305600&Signature=j1k2l3m4n5o6...&Key-Pair-Id=APKAIOSF0DNN7EXAMPLE
   ```

**Verification (CloudFront edge):**

5. **User requests the URL.** CloudFront reads `Key-Pair-Id=APKAIOSF0DNN7EXAMPLE` → looks up the corresponding public key.

6. **Decrypt the signature** using the public key:
   ```
   decrypted = RSA_DECRYPT(publicKey, "j1k2l3m4n5o6...")

   → "a3f9bc72e1d84c..."
   ```

7. **Independently hash** the URL path + Expires from the incoming request:
   ```
   expected = SHA1("https://d123456.cloudfront.net/videos/lecture.mp4Expires=1705305600")

   → "a3f9bc72e1d84c..."
   ```

8. **Compare:**
   ```
   decrypted == expected?   →  "a3f9bc72e1d84c..." == "a3f9bc72e1d84c..."  →  YES
   Expires > now()?         →  1705305600 > 1705300000                      →  YES
   → Serve the file from edge cache
   ```

**Why this is secure:**
- The private key never leaves your server — CloudFront only has the public key
- The public key can only decrypt, not forge new signatures
- Even if an attacker gets the public key, they cannot produce a valid signature without the private key
- CloudFront edge servers worldwide can verify independently without calling back to your origin

---

## When NOT to Use Presigned URLs / Direct Blob Storage

### Q: When should you NOT use presigned URLs and just proxy through the server?

This pattern adds complexity only worth it for actual scale or size problems. Avoid it in these cases:

---

### 1. Small files don't need it (< 10MB)

**Example:** A user submits a contact form with a profile picture (2MB JPEG).

```
With presigned URL (overkill):
  Client → POST /get-upload-url → Server generates presigned URL → Client uploads to S3
  = 2 round trips, signing overhead, extra complexity

Just use a normal API endpoint:
  Client → POST /api/profile-picture (multipart form) → Server → Server uploads to S3
  = 1 round trip, server handles it fine, thousands of these per second is no problem
```

Note: data still ends up in S3 either way — the difference is only the path it takes.

---

### 2. Synchronous validation requirements

**Example:** A fintech app lets users import transactions via CSV. Columns must be `date, amount, merchant` — wrong format should be rejected immediately.

```
With presigned URL (broken UX):
  Client uploads CSV directly to S3
  Worker picks it up async, finds wrong headers
  User gets an error notification 30 seconds later
  → Bad: user already thought the upload succeeded

With server proxy (correct):
  Client → POST /api/import → Server streams CSV bytes as they arrive
  Server reads first few lines: "wrong headers" → 400 Bad Request immediately
  → User sees the error before upload even completes and can fix it
```

---

### 3. Compliance and data inspection

**Example:** A healthcare app lets doctors upload patient documents (HIPAA). All data must pass through a certified DLP (Data Loss Prevention) scanner before storage.

```
With presigned URL (non-compliant):
  Patient document goes directly: Client → S3
  No certified system ever inspects the bytes
  Auditor asks: "who scanned this before storage?" → no answer
  → HIPAA violation

With server proxy (compliant):
  Client → Server (certified) → DLP scanner → S3
  Every byte passes through your certified infrastructure
  Full audit log of who uploaded what and when
```

---

### 4. When the experience demands immediate response

**Example:** A dating app where users upload a profile photo and face detection immediately crops and centers it.

```
With presigned URL + async processing (broken UX):
  1. Client uploads photo directly to S3
  2. S3 event triggers Lambda worker
  3. Worker runs face detection, crops image, saves result
  4. Worker notifies client via WebSocket: "done"
  5. Client refreshes profile photo
  Total time: 3–8 seconds. User sees a spinner. Feels broken.

With server proxy (smooth UX):
  1. Client sends photo to server
  2. Server runs face detection inline
  3. Server responds with cropped image in the same HTTP response
  4. Client displays it immediately
  Total time: ~500ms. Feels instant.
```

Rule of thumb: if the user needs to **see a result based on the file contents** before moving on, proxy through your server. Async is only fine when the user can walk away and come back.

---

## Chunked Uploads & Resumability

### Q: What if the upload fails at 99%?

When files exceed 100MB, use chunked uploads. The storage service tracks which parts uploaded successfully, so a failed connection doesn't mean starting over.

| Provider | API | Min chunk size |
|---|---|---|
| S3 | Multipart Upload | 5 MB |
| GCS | Resumable Uploads | Any size |
| Azure | Block Blobs | 4 MB |

**How resuming works:**
```
User uploads a 2GB video in 200 parts (10MB each)
Parts 1–19 succeed, part 20 fails (connection drops)

On reconnect:
  S3:    Client calls ListParts(UploadId)       → sees parts 1–19 completed
  GCS:   Client checks resumable session status → gets byte offset to resume from
  Azure: Client lists committed blocks          → sees which block IDs succeeded

Client resumes from part 20 only — parts 1–19 are not re-uploaded
```

**Session tracking:** The client must persist the upload session identifier across restarts:
- S3: `UploadId`
- GCS: resumable upload URL
- Azure: block blob container URL

Many teams store this in `localStorage` so uploads can resume even after the app restarts or the browser is closed.

---

### Q: What about the cost of incomplete uploads?

Incomplete parts sit in S3 and are billed even though no visible object exists in the bucket.

```
Day 0, 10:00am  → User initiates multipart upload (UploadId: abc123)
Day 0, 10:05am  → Parts 1–150 uploaded (1.5GB), connection drops, user abandons
Day 0 – Day 2   → 1.5GB of orphaned parts sitting in S3, billed every month
Day 2, 10:00am  → Lifecycle policy kicks in → S3 deletes all parts → billing stops
```

**Fix: set a lifecycle policy on the bucket:**

```json
{
  "Rules": [{
    "ID": "cleanup-incomplete-multipart-uploads",
    "Status": "Enabled",
    "Filter": { "Prefix": "uploads/" },
    "AbortIncompleteMultipartUpload": {
      "DaysAfterInitiation": 2
    }
  }]
}
```

This is automatic and rule-based — defined once, S3 enforces it without any code on your end.

**Why 1-2 days?**
- Too short (e.g. 1 hour): a user on a slow connection uploading over several hours gets their upload invalidated mid-way
- Too long (e.g. 30 days): orphaned parts rack up significant storage costs
- 1-2 days covers legitimate slow uploads and app restarts while keeping costs in check

**Lifecycle policies can also handle storage tier transitions:**
```
Day 0   → S3 Standard         (frequent access, most expensive)
Day 30  → S3 Infrequent Access (60% cheaper, ~30ms retrieval)
Day 90  → S3 Glacier           (80% cheaper, minutes–hours retrieval)
Day 365 → Delete permanently
```

Example: a video platform keeps recent uploads in Standard, archives videos older than 30 days to Infrequent Access, and deletes raw unprocessed uploads after 90 days once transcoding is complete.
