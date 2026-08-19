Approved — per-field resolution, map-sourced values as assignments,
caller-sourced keeping today's semantics, and the CSV loader re-resolving
existing users rows at load time. All four as you described.

---

## One change to the carve-out

Do not accept hashing and central org resolution as mutually exclusive.

The CSV loader runs inside the collector, so it has the same secret that
`hash_user_id` uses. Apply the same hash to the incoming ACF2 ID before
writing to `org_map` when hashing is enabled, so the key matches what the
collector actually stores. The map's plaintext CSV stays plaintext on the way
in; only the stored key is hashed.

**Verify this before implementing.** Read the code and confirm the loader can
actually reach the hash function and its secret. If it cannot, say so and we
go back to your version — I would rather have your original limitation stated
honestly than a fix that only works on paper.

Do not answer this from the shape of the design. Name the file and line where
the secret is read, and say how the loader gets to it.

Also say what happens to an existing map if the secret rotates.

## One question, answer before writing code

Should the `users` row record where each org value came from — map, caller, or
neither?

`org_map` already has a `source` column, but that describes the map, not the
row. A per-row provenance column would let the dashboard answer "is this
division from the directory, or from someone's hardcoded string".

Tell me whether it is worth one column or is scope creep at this point. Your
call, I will take the answer — but give me the reasoning, not just the verdict.
"Scope creep" is a fine answer if you say what it would cost and what we lose
by skipping it.

---

Answer both of these before writing any code. Then proceed with 9.1 and 9.2.
