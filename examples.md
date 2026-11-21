# Examples

Real captures from `benchmarks/examples.py` on `claude-opus-5-5`. Same question, a default assistant (**Normal**, system prompt "You are a helpful assistant.") versus the Kevin voice. One sample each, verbatim. Nothing here is edited.

Back to the [README](README.md).

## What is a memory leak?

**Normal** (332 words)

> A **memory leak** happens when a program allocates memory but never releases it after it's no longer needed. The memory stays reserved, so neither the program nor the operating system can reuse it.
>
> ## Why it's a problem
>
> One small leak usually goes unnoticed. But if leaking code runs repeatedly (in a loop, on every request, every frame), the lost memory accumulates. Over time this can cause:
> - Rising memory usage
> - Slower performance, as the system starts swapping to disk
> - Crashes or out-of-memory errors
> - Instability in long-running programs like servers, browsers, or games
>
> ## A simple example (C)
>
> ```c
> void process() {
>     int *data = malloc(1000 * sizeof(int));  // allocate memory
>     // ... use data ...
>     // forgot to call free(data);
> }   // pointer goes away, but the memory is still allocated
> ```
>
> Each call to `process()` leaks about 4 KB. Call it a million times and you've lost about 4 GB.
>
> ## Do garbage-collected languages have leaks?
>
> Yes, though they look different. Languages like Java, Python, and JavaScript free memory automatically, but only when nothing references it anymore. Leaks occur when you **unintentionally keep references** to objects you no longer need, such as:
> - Caches or lists that grow forever and are never cleared
> - Event listeners that are registered but never removed
> - Global variables holding large objects
> - Closures capturing more data than intended
>
> ```javascript
> const cache = [];
> function handleRequest(req) {
>     cache.push(req);  // never removed, so it grows forever
> }
> ```
>
> ## How to prevent and find them
>
> - **Free what you allocate** in manual-memory languages, or use tools that do it for you (e.g., smart pointers in C++, ownership in Rust).
> - **Remove listeners and subscriptions** when components are destroyed.
> - **Bound your caches** with size limits or expiration.
> - **Use profiling tools** like Valgrind or AddressSanitizer (C/C++), browser DevTools heap snapshots (JavaScript), or VisualVM (Java).
>
> In short, a memory leak is memory your program has lost track of but is still holding onto.

**Kevin** (29 words)

> Program grab memory, never give back. Memory pile up, program get slow, maybe crash.
>
> Common cause: forgot `free`, objects still referenced (caches, listeners, globals), or cycles some collectors miss.

---

## What is the difference between authentication and authorization?

**Normal** (322 words)

> **Authentication** and **authorization** are related security concepts that answer different questions.
>
> ## Authentication: "Who are you?"
> Authentication **verifies identity**. It confirms that a user (or system) is who they claim to be.
>
> **Common methods:**
> - Passwords or PINs
> - Biometrics (fingerprint, face recognition)
> - One-time codes (SMS, authenticator apps)
> - Security keys or certificates
> - Multi-factor authentication (MFA), which combines several of these
>
> ## Authorization: "What are you allowed to do?"
> Authorization **determines permissions**. Once your identity is known, it decides which resources you can access and which actions you can perform.
>
> **Common approaches:**
> - Role-based access control (RBAC): admin, editor, viewer
> - Access control lists (ACLs)
> - Attribute-based access control (ABAC)
> - Permission scopes (e.g., in OAuth)
>
> ## Key Differences
>
> | Aspect | Authentication | Authorization |
> |---|---|---|
> | Purpose | Verifies identity | Grants or denies permissions |
> | Order | Comes first | Comes after authentication |
> | Based on | Credentials (password, biometrics) | Policies, roles, rules |
> | Visible to user? | Usually yes (login screen) | Usually not (happens behind the scenes) |
> | Can user change it? | Partly (e.g., update password) | No, set by admins or the system |
> | Typical failure | **401 Unauthorized** | **403 Forbidden** |
>
> Note: despite its name, HTTP **401** actually signals an *authentication* problem, while **403** signals an *authorization* problem.
>
> ## Real-World Analogy
> At an airport:
> - **Authentication** is showing your passport at security. It proves you are who you say you are.
> - **Authorization** is your boarding pass. It determines which flight you can board and whether you can enter the first-class lounge.
>
> ## Example in Software
> 1. You log into a company app with your username, password, and MFA code. → **Authentication**
> 2. You try to open the payroll dashboard, but only HR managers have access, so you're denied. → **Authorization**
>
> **In short:** authentication establishes *who you are*, and authorization establishes *what you can do*.

**Kevin** (44 words)

> Authentication: prove who you are. Password, key, fingerprint.
> Authorization: decide what you allowed do. Read file, delete user, see admin page.
>
> Authentication come first. Login proves you Kevin. Authorization says Kevin no touch accounting server.
>
> Fail authentication usually give 401. Fail authorization give 403.

---

## Why would a team use a message queue?

**Normal** (384 words)

> Teams use a message queue (RabbitMQ, Kafka, Amazon SQS, Redis Streams, etc.) mainly to **decouple** the parts of a system so they don't all have to be available, fast, and scaled together at the same moment. The main reasons:
>
> ### 1. Decoupling producers from consumers
> The service sending a message doesn't need to know who processes it, where they are, or whether they're running right now. You can add, remove, or rewrite consumers without touching the producer.
>
> ### 2. Asynchronous processing
> Slow work can happen in the background instead of making a user wait.
> - *Example:* A user uploads a video. The API responds "Upload received" immediately, and a worker picks the transcoding job off the queue.
>
> ### 3. Absorbing traffic spikes (load leveling)
> If 10,000 requests arrive in a second but your backend can handle 1,000/sec, the queue buffers the excess so it gets processed over time instead of crashing the system.
>
> ### 4. Reliability and fault tolerance
> - If a consumer crashes, messages wait in the queue until it recovers.
> - Acknowledgments and retries ensure work isn't silently lost.
> - Failed messages can go to a **dead-letter queue** for inspection.
>
> ### 5. Independent scaling
> You can scale consumers horizontally (add more workers) based on queue depth, without scaling the producers.
>
> ### 6. Fan-out / event-driven architecture
> One event ("OrderPlaced") can be delivered to many interested services: billing, inventory, email, analytics. Each reacts independently, which suits microservices.
>
> ### 7. Ordering and replay (in some systems)
> Log-based systems like Kafka preserve order within partitions and let consumers replay past events. That's useful for rebuilding state, auditing, or feeding new services historical data.
>
> ### Trade-offs to be aware of
> - **More infrastructure** to run, monitor, and secure.
> - **Eventual consistency:** results aren't immediate, which complicates UX and reasoning.
> - **Harder debugging:** a request's path spans multiple services and time.
> - **Delivery semantics:** most queues are "at-least-once," so consumers must be **idempotent** (safe to process the same message twice).
> - **Ordering** isn't always guaranteed.
>
> ### Rule of thumb
> Use a queue when work can be deferred, when components fail or scale independently, or when multiple systems need to react to the same event. If you need an immediate answer for the caller (e.g., "Is this password correct?"), a direct synchronous call is usually simpler and better.

**Kevin** (92 words)

> Decouple services. Sender drop message, move on. Receiver process when ready.
>
> Main reasons:
> - **Async work**: slow job (email, video encode) leave request path. User no wait.
> - **Load leveling**: traffic spike pile in queue, not crash worker.
> - **Reliability**: consumer down, message wait. Retry on failure, dead-letter queue for poison message.
> - **Scaling**: add more consumer, drain faster.
> - **Fan-out**: one event, many subscriber (pub/sub).
> - **Decoupling**: producer no know who consume. Teams change services independent.
>
> Cost: more moving part, eventual consistency, duplicate or out-of-order message possible. Consumer must be idempotent.

---

## What does git rebase do?

**Normal** (455 words)

> # What `git rebase` Does
>
> `git rebase` **moves or replays a series of commits onto a new base commit**. It rewrites history so your changes look as if you started them from a different point.
>
> ## The Basic Idea
>
> Say you branched off `main` to work on a feature, and meanwhile `main` got new commits:
>
> ```
>           A---B---C  feature
>          /
>     D---E---F---G  main
> ```
>
> Running this while on `feature`:
>
> ```bash
> git rebase main
> ```
>
> Git takes your commits (A, B, C), temporarily sets them aside, moves `feature` to the tip of `main`, and then reapplies your commits one by one:
>
> ```
>                   A'--B'--C'  feature
>                  /
>     D---E---F---G  main
> ```
>
> `A'`, `B'`, and `C'` are **new commits**. They contain the same changes as the originals but have different hashes, because their parent commits are different.
>
> ## Rebase vs. Merge
>
> Both integrate changes from one branch into another, but they produce different history:
>
> | `git merge main` | `git rebase main` |
> |---|---|
> | Creates a merge commit | No merge commit |
> | Preserves the true history | Rewrites history |
> | Branching history | Linear, cleaner history |
> | Safe on shared branches | Risky on shared branches |
>
> ## Interactive Rebase
>
> `git rebase -i` lets you edit commits as they're replayed:
>
> ```bash
> git rebase -i HEAD~3   # edit the last 3 commits
> ```
>
> This opens an editor where you can mark each commit with an action:
> - **pick**: keep the commit as is
> - **reword**: change the commit message
> - **squash** / **fixup**: combine it with the previous commit
> - **edit**: pause so you can amend the commit
> - **drop**: delete the commit
>
> You can also reorder commits by rearranging the lines.
>
> This is commonly used to clean up messy commits before opening a pull request.
>
> ## Handling Conflicts
>
> If a replayed commit conflicts with the new base, the rebase pauses. Then you:
>
> 1. Fix the conflicted files.
> 2. Run `git add <files>`.
> 3. Run `git rebase --continue`.
>
> To give up and return to the state before the rebase, run `git rebase --abort`.
>
> ## ⚠️ The Golden Rule
>
> **Don't rebase commits that others have already pulled.**
>
> Rebasing creates new commits and abandons the old ones. If someone else built work on the originals, their history and yours will diverge, which causes confusion and duplicate commits.
>
> If you rebase a branch you've already pushed, you'll need to force-push it. Prefer `--force-with-lease` over `--force`, because it refuses to overwrite commits on the remote that you haven't seen:
>
> ```bash
> git push --force-with-lease
> ```
>
> ## Common Uses
>
> - `git pull --rebase`: update your branch without creating merge commits
> - `git rebase main`: bring a feature branch up to date with `main`
> - `git rebase -i`: tidy up local commits before sharing them

**Kevin** (63 words)

> Rebase move your commits onto new base. Git replay each commit on top of target branch, so history look straight, no merge commit.
>
> Example: `git rebase main` on feature branch. Your feature commits now sit after latest `main` commits.
>
> Rebase rewrites history: replayed commits get new hashes. Do not rebase commits other people already pulled, because their copies will no longer match yours.

---

## What is a database index and when should I add one?

**Normal** (539 words)

> # Database Indexes
>
> ## What It Is
>
> An index is a separate data structure that lets the database find rows quickly without scanning the entire table.
>
> **Analogy:** Think of the index at the back of a textbook. Instead of reading every page to find "photosynthesis," you look it up alphabetically and jump straight to page 247.
>
> Without an index, a query like this:
>
> ```sql
> SELECT * FROM users WHERE email = 'alice@example.com';
> ```
>
> forces the database to check **every row** (a "full table scan"). With an index on `email`, it can jump almost directly to the matching row.
>
> ## How It Works (Briefly)
>
> Most indexes are **B-trees**: sorted, balanced tree structures. Lookups take roughly O(log n) time instead of O(n). On a table with 10 million rows, that is the difference between about 23 steps and 10 million.
>
> Other types exist for specific needs: **hash** indexes for exact matches, **GIN/GiST** for full-text search and JSON, and **spatial** indexes for geographic data.
>
> ## The Tradeoff
>
> Indexes are not free:
>
> | Benefit | Cost |
> |---|---|
> | Much faster reads/lookups | Slower `INSERT`, `UPDATE`, `DELETE` (the index must be updated too) |
> | Faster sorting and joins | Extra disk space |
> | Can enforce uniqueness | More memory pressure |
>
> ## When to Add an Index
>
> ✅ **Good candidates:**
>
> - **Columns in `WHERE` clauses** that you filter on frequently
> - **Foreign keys / `JOIN` columns.** Some databases, including PostgreSQL, don't index these automatically.
> - **Columns used in `ORDER BY`** or `GROUP BY` on large tables
> - **Columns that must be unique**, such as email or username. Use a `UNIQUE` index.
> - **High-selectivity columns**, where values are mostly distinct (e.g., `email`, `order_id`)
> - **Slow queries you've actually measured**
>
> ❌ **Usually skip indexing when:**
>
> - The table is small (a few thousand rows). A scan is already fast.
> - The column has low selectivity, such as a boolean `is_active` where 95% of rows are `true`. The database often ignores these indexes anyway.
> - The table is write-heavy and rarely queried, such as logs.
> - The column is rarely used in queries.
>
> ## Practical Tips
>
> **1. Measure first.** Use `EXPLAIN` (or `EXPLAIN ANALYZE`) to see how a query executes:
> ```sql
> EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
> ```
> Look for "Seq Scan" / "Full Table Scan" on large tables. That's a sign an index might help.
>
> **2. Composite indexes: order matters.** An index on `(last_name, first_name)` helps queries filtering on `last_name` alone, or on both columns. It does **not** help queries filtering only on `first_name`. Put the most commonly filtered or most selective column first.
>
> **3. Watch for things that disable indexes.** Wrapping a column in a function usually prevents index use:
> ```sql
> -- Can't use a plain index on created_at:
> WHERE YEAR(created_at) = 2024
> -- Can use it:
> WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
> ```
> Leading wildcards like `LIKE '%smith'` have the same problem.
>
> **4. Remove unused indexes.** Most databases can report index usage statistics. Indexes nobody uses just slow down writes.
>
> ## Rule of Thumb
>
> > Index based on your **actual query patterns**, not guesses. Start with primary keys, foreign keys, and unique constraints, then add indexes when `EXPLAIN` shows slow scans on queries that matter.

**Kevin** (136 words)

> Index = sorted lookup structure (usually B-tree) pointing to rows. Database find rows without scanning whole table. Like book index.
>
> Cost: extra disk space, slower writes. Every `INSERT`/`UPDATE`/`DELETE` must update index too.
>
> Add one when:
> - Column often in `WHERE`, `JOIN`, or `ORDER BY`.
> - Table big and query slow. `EXPLAIN` show full table scan.
> - Column selective (many distinct values, like email, user ID).
> - Need uniqueness. Unique index enforce it.
> - Queries filter several columns together. Composite index, order matter: put most-filtered column first.
>
> Skip when:
> - Table small. Scan already fast.
> - Table write-heavy, rarely read.
> - Column low-selectivity (boolean, status with three values). Index rarely help.
> - Duplicate of existing index. Index on `(a, b)` already cover `a` alone.
>
> Rule: measure first. Add index for real slow query, then check `EXPLAIN` again.

---

## What is the difference between a process and a thread?

**Normal** (378 words)

> A **process** is an independent running program with its own memory. A **thread** is a unit of execution *inside* a process. A single process can contain many threads.
>
> ## Process
> - **Own address space.** Each process has separate memory: code, heap, stack, and data.
> - **Isolated.** One process can't directly read or write another's memory. A crash in one usually doesn't affect others.
> - **Own resources.** Each has its own file handles, environment, and security context.
> - **Heavier.** Creating a process and switching between processes costs more, because the OS must set up and swap memory mappings.
> - **Communication** requires inter-process communication (IPC), such as pipes, sockets, shared memory, or message queues.
>
> ## Thread
> - **Shares the process's memory.** All threads in a process see the same heap, global variables, and open files.
> - **Has its own execution state.** Each thread has its own stack, registers, and program counter.
> - **Lightweight.** Threads are cheaper to create and faster to switch between.
> - **Easy communication.** Threads can read and write shared variables directly. This is also the danger: it leads to race conditions, so you need locks, mutexes, or other synchronization.
> - **Less isolated.** A bug in one thread, like a segfault or memory corruption, can bring down the whole process.
>
> ## Analogy
> A **process** is like a house. It has its own walls, kitchen, and address. **Threads** are the people living in it. They share the kitchen and the fridge, which makes cooperation easy, but they can also get in each other's way.
>
> ## Summary Table
>
> | Aspect | Process | Thread |
> |---|---|---|
> | Memory | Separate | Shared within process |
> | Creation cost | High | Low |
> | Context switch | Slower | Faster |
> | Communication | IPC (pipes, sockets, etc.) | Shared memory directly |
> | Isolation/fault tolerance | Strong | Weak |
> | Synchronization needs | Less (unless sharing resources) | More (locks, mutexes) |
>
> ## When to use which
> - **Processes** suit isolation and robustness. Examples include web browsers running each tab as a separate process, and running untrusted code.
> - **Threads** suit concurrent tasks that share a lot of data and need fast communication. Examples include a server handling many requests, or a UI thread plus a background worker.

**Kevin** (58 words)

> Process: running program with own memory space. Isolated. One crash no hurt others.
>
> Thread: execution path inside process. Threads share process memory, so cheap to create and fast to talk to each other. But need locks to avoid race condition, and one bad thread can crash whole process.
>
> Process = house. Thread = people in house sharing kitchen.

---

## What is a closure in JavaScript?

**Normal** (475 words)

> # Closures in JavaScript
>
> A **closure** is a function that remembers the variables from the scope where it was **created**, even after that outer scope has finished executing.
>
> In other words, a function "closes over" its surrounding variables and keeps access to them.
>
> ## A Basic Example
>
> ```javascript
> function outer() {
>   let message = "Hello from outer!";
>
>   function inner() {
>     console.log(message); // inner can access outer's variable
>   }
>
>   return inner;
> }
>
> const myFunction = outer(); // outer() has finished running
> myFunction();               // "Hello from outer!"
> ```
>
> `outer()` has already returned, yet `inner` can still read `message`. That's a closure.
>
> ## Why It Works
>
> JavaScript uses **lexical scoping**: a function's access to variables is determined by where it is written in the code, not where it is called. When a function is created, it keeps a reference to its surrounding scope, so those variables stay alive as long as the function exists.
>
> ## Practical Example: A Counter
>
> ```javascript
> function createCounter() {
>   let count = 0; // private variable
>
>   return {
>     increment() { count++; return count; },
>     decrement() { count--; return count; },
>     getCount()  { return count; }
>   };
> }
>
> const counter = createCounter();
> counter.increment(); // 1
> counter.increment(); // 2
> counter.decrement(); // 1
> console.log(counter.count); // undefined: count can't be accessed directly
> ```
>
> Each call to `createCounter()` creates a **new, independent** closure:
>
> ```javascript
> const a = createCounter();
> const b = createCounter();
> a.increment(); // 1
> a.increment(); // 2
> b.increment(); // 1 (separate count)
> ```
>
> ## Common Uses
>
> 1. **Data privacy / encapsulation**: hiding variables from outside access (as above).
> 2. **Function factories**: generating customized functions:
>    ```javascript
>    function multiplier(factor) {
>      return (n) => n * factor;
>    }
>    const double = multiplier(2);
>    const triple = multiplier(3);
>    double(5); // 10
>    triple(5); // 15
>    ```
> 3. **Callbacks and event handlers**: keeping access to data when the callback runs later:
>    ```javascript
>    function setupButton(name) {
>      document.querySelector("#btn").addEventListener("click", () => {
>        console.log(`${name} clicked!`);
>      });
>    }
>    ```
> 4. **Memoization**: caching results in a variable the function keeps private.
>
> ## A Classic Gotcha
>
> ```javascript
> for (var i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i), 100);
> }
> // Prints: 3, 3, 3
> ```
>
> `var` is function-scoped, so all three callbacks share the **same** `i`, which is 3 by the time they run. Using `let`, which creates a new binding for each iteration, fixes this:
>
> ```javascript
> for (let i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i), 100);
> }
> // Prints: 0, 1, 2
> ```
>
> ## Key Takeaways
>
> - A closure = a function + the variables from the scope where it was defined.
> - Closures capture variables **by reference**, not by value, so they see the variable's current value.
> - Every function in JavaScript forms a closure. It only becomes noticeable when the inner function outlives its outer function.
> - Closures keep variables in memory. Be mindful of this with large objects or long-lived functions.

**Kevin** (69 words)

> Closure = function that remember variables from scope where it born, even after outer function finish.
>
> ```javascript
> function makeCounter() {
>   let count = 0;
>   return function () {
>     count++;
>     return count;
>   };
> }
>
> const counter = makeCounter();
> counter(); // 1
> counter(); // 2
> ```
>
> `makeCounter` done running, but inner function still hold `count`. Each `makeCounter()` call make own private `count`.
>
> Common use: private state, callbacks, event handlers, function factories.

---

## How does HTTPS work?

**Normal** (755 words)

> # How HTTPS Works
>
> **HTTPS** is ordinary HTTP sent through an encrypted, authenticated channel created by **TLS** (Transport Layer Security). It provides three guarantees:
>
> 1. **Confidentiality**: eavesdroppers can't read the traffic.
> 2. **Integrity**: nobody can tamper with data in transit without detection.
> 3. **Authentication**: you're actually talking to the real `yourbank.com`, not an impostor.
>
> ---
>
> ## The Big Picture
>
> When you visit `https://example.com`:
>
> 1. Your browser opens a TCP connection to the server (usually port 443).
> 2. Browser and server perform a **TLS handshake** to:
>    - verify the server's identity, and
>    - agree on shared secret keys.
> 3. All HTTP requests and responses are then encrypted with those keys.
>
> ---
>
> ## Step 1: The TLS Handshake (TLS 1.3, simplified)
>
> ```
> Browser                                         Server
>    |                                               |
>    |--- ClientHello -----------------------------> |
>    |    (supported ciphers, random value,          |
>    |     key share for Diffie-Hellman)             |
>    |                                               |
>    | <-------------------------------- ServerHello |
>    |    (chosen cipher, its key share)             |
>    |    + Certificate                              |
>    |    + CertificateVerify (signature)            |
>    |    + Finished                                 |
>    |                                               |
>    |--- Finished --------------------------------> |
>    |                                               |
>    |====== Encrypted HTTP traffic ================>|
> ```
>
> TLS 1.3 completes this in **one round trip**, and can sometimes resume a previous session with zero round trips.
>
> ---
>
> ## Step 2: Agreeing on a Secret Key (Key Exchange)
>
> Both sides need a shared secret, but they're communicating over a network anyone might be watching. The solution is **Diffie-Hellman key exchange**, typically the elliptic-curve variant (ECDHE):
>
> - Each side generates a temporary private value and sends a corresponding **public** value.
> - Each side combines its own private value with the other's public value.
> - Both arrive at the **same shared secret**, yet an eavesdropper who sees only the public values can't compute it.
>
> **Paint-mixing analogy:** You and I each mix a secret color into a common public color and swap the results. Then each of us adds our own secret color again. We both end up with the same final mixture, but an observer can't "unmix" the paint to figure it out.
>
> Because these keys are temporary ("ephemeral"), HTTPS gets **forward secrecy**: even if the server's long-term private key is stolen later, past recorded sessions can't be decrypted.
>
> ---
>
> ## Step 3: Proving Identity (Certificates)
>
> Key exchange alone doesn't stop a **man-in-the-middle**: an attacker could perform a separate key exchange with each side and relay messages between them. Certificates prevent this.
>
> - The server has a **certificate** containing its domain name and public key, digitally signed by a **Certificate Authority (CA)** such as Let's Encrypt or DigiCert.
> - Your browser or OS ships with a list of trusted **root CAs**.
> - The browser checks that:
>   - the signature chain leads back to a trusted root,
>   - the certificate matches the domain you requested,
>   - the certificate hasn't expired or been revoked.
> - The server then **signs the handshake** with its private key (the CertificateVerify message). This proves it actually holds the private key matching the certificate, rather than just having copied a public certificate.
>
> If any check fails, you see a browser warning like "Your connection is not private."
>
> ---
>
> ## Step 4: Encrypting the Actual Data
>
> After the handshake, both sides derive **symmetric keys** from the shared secret. Symmetric encryption is used for bulk data because it's much faster than public-key cryptography. Common ciphers are:
>
> - **AES-GCM**
> - **ChaCha20-Poly1305**
>
> These are "authenticated encryption" schemes, so every message is both encrypted and protected against tampering.
>
> ---
>
> ## Why Combine Asymmetric and Symmetric Crypto?
>
> | Type | Used for | Why |
> |---|---|---|
> | Asymmetric (RSA, ECDSA, ECDHE) | Identity verification and key agreement | Solves the "how do strangers share a secret?" problem |
> | Symmetric (AES, ChaCha20) | Encrypting the actual data | Fast and efficient |
>
> ---
>
> ## What HTTPS Does and Doesn't Hide
>
> **Hidden from observers:**
> - URL paths and query strings (`/account?id=123`)
> - Headers, cookies, form data, page content
>
> **Still visible:**
> - The server's IP address
> - Usually the domain name, via SNI in the handshake. Encrypted Client Hello (ECH) is beginning to address this.
> - Timing and approximate size of traffic
>
> Also note that HTTPS only proves you're connected to *the owner of that domain*. It doesn't mean the site is trustworthy. Phishing sites can have valid certificates too.
>
> ---
>
> ## TL;DR
>
> 1. The browser and server use **Diffie-Hellman** to create a shared secret over a public network.
> 2. The server proves its identity with a **CA-signed certificate** and a signature from its private key.
> 3. Everything afterward is encrypted with fast **symmetric encryption** derived from the shared secret.

**Kevin** (171 words)

> HTTPS = HTTP inside TLS. TLS give three thing: encryption, integrity, server identity.
>
> How connection start (TLS 1.3):
>
> 1. **Hello.** Browser send supported cipher, random number, key share.
> 2. **Server reply.** Server pick cipher, send own key share plus certificate.
> 3. **Certificate check.** Browser verify certificate signed by trusted Certificate Authority, not expired, match domain. Server also sign handshake with private key. Prove server own certificate.
> 4. **Key agreement.** Both side use Diffie-Hellman with key shares. Each compute same secret. Secret never cross wire.
> 5. **Encrypted traffic.** Shared secret make symmetric keys (usually AES-GCM or ChaCha20). All HTTP data now encrypted. Each record carry auth tag, so tampering get caught.
>
> Why mix two crypto kind: asymmetric crypto good for prove identity and agree key, but slow. Symmetric crypto fast, so it carry bulk data.
>
> Bonus: fresh keys each session give forward secrecy. Server private key leak later? Old traffic stay safe.
>
> HTTPS hide page content, URL path, headers, cookies. Still visible: server IP, and usually domain name (via SNI and DNS).

---

## What is the difference between TCP and UDP?

**Normal** (422 words)

> # TCP vs UDP
>
> Both are **transport layer protocols** in the Internet Protocol suite, but they make very different trade-offs.
>
> ## TCP (Transmission Control Protocol)
> **Reliable, connection-oriented communication.**
>
> - **Connection setup:** Establishes a connection with a *three-way handshake* (SYN → SYN-ACK → ACK) before sending data.
> - **Reliability:** Guarantees delivery. Lost packets are detected and retransmitted.
> - **Ordering:** Data arrives in the exact order it was sent.
> - **Error checking:** Uses acknowledgments (ACKs) and checksums.
> - **Flow control:** Prevents a fast sender from overwhelming a slow receiver.
> - **Congestion control:** Slows down when the network is congested.
> - **Overhead:** Larger header (20–60 bytes), with more processing and latency.
> - **Data model:** A continuous **byte stream** with no message boundaries.
>
> ## UDP (User Datagram Protocol)
> **Fast, lightweight, connectionless communication.**
>
> - **No connection setup:** Just sends packets ("datagrams") immediately.
> - **No delivery guarantee:** Packets may be lost, duplicated, or arrive out of order.
> - **No retransmission:** If something is lost, it's gone (unless the application handles it).
> - **No flow or congestion control:** Sends as fast as the application wants.
> - **Low overhead:** Small fixed header (8 bytes).
> - **Data model:** Discrete **messages**, with boundaries preserved.
> - **Supports broadcast and multicast**, which TCP does not.
>
> ## Side-by-Side Comparison
>
> | Feature | TCP | UDP |
> |---|---|---|
> | Connection | Connection-oriented | Connectionless |
> | Reliability | Guaranteed delivery | Best effort |
> | Ordering | Ordered | Not ordered |
> | Speed | Slower | Faster |
> | Header size | 20–60 bytes | 8 bytes |
> | Flow/congestion control | Yes | No |
> | Broadcast/multicast | No | Yes |
> | Data unit | Byte stream (segments) | Datagrams |
>
> ## Typical Use Cases
>
> **TCP**, used when correctness matters more than speed:
> - Web browsing (HTTP/1.1, HTTP/2)
> - Email (SMTP, IMAP, POP3)
> - File transfers (FTP, SFTP)
> - Remote access (SSH)
>
> **UDP**, used when speed matters and some loss is acceptable:
> - Live video/audio streaming and VoIP
> - Online multiplayer games
> - DNS lookups
> - DHCP
> - QUIC / HTTP/3, which builds its own reliability on top of UDP
>
> ## Analogy
> - **TCP** is like a **phone call**: you establish a connection, talk in order, and know if the other person didn't hear you.
> - **UDP** is like **sending postcards**: quick and cheap, but some might get lost or arrive out of order, and you won't be notified.
>
> **In short:** Choose TCP when you need every byte delivered correctly and in order. Choose UDP when low latency matters more than perfect reliability.

**Kevin** (57 words)

> TCP: connection first, guarantee delivery, keep order, resend lost packet, slow down when network busy. More overhead.
>
> UDP: no connection, just send. No guarantee, no order, no resend. Less overhead, lower latency.
>
> Use TCP when every byte matter: web, email, file transfer. Use UDP when speed matter more than few lost packet: video call, gaming, DNS, streaming.

---

## Explain Big-O notation.

**Normal** (657 words)

> # Big-O Notation
>
> **Big-O notation** describes how an algorithm's running time (or memory use) **grows as the input size grows**. It doesn't measure exact speed in seconds. It measures how the cost *scales*.
>
> If `n` is the size of the input (number of items in a list, for example), Big-O answers: *"If I double `n`, roughly how much more work does this take?"*
>
> ---
>
> ## The Core Idea
>
> Big-O focuses on the **dominant term** and ignores details that don't matter for large inputs:
>
> - **Drop constants:** `3n` → `O(n)`
> - **Drop lower-order terms:** `n² + 5n + 100` → `O(n²)`
>
> Why? When `n` is a million, `n²` is a trillion, and the `5n + 100` part is negligible by comparison.
>
> Formally, `f(n) = O(g(n))` means that for large enough `n`, `f(n)` is at most some constant times `g(n)`. In other words, `g(n)` is an **upper bound** on growth.
>
> ---
>
> ## Common Complexities (fastest to slowest)
>
> | Big-O | Name | Example | n = 1,000 → ops (approx.) |
> |---|---|---|---|
> | `O(1)` | Constant | Accessing an array element by index | 1 |
> | `O(log n)` | Logarithmic | Binary search in a sorted array | ~10 |
> | `O(n)` | Linear | Looping through a list once | 1,000 |
> | `O(n log n)` | Linearithmic | Efficient sorting (merge sort, heapsort) | ~10,000 |
> | `O(n²)` | Quadratic | Nested loops over the same list | 1,000,000 |
> | `O(2ⁿ)` | Exponential | Naive recursive Fibonacci, all subsets | astronomically large |
> | `O(n!)` | Factorial | Brute-force traveling salesman | even worse |
>
> ---
>
> ## Code Examples
>
> **O(1): constant time**
> ```python
> def get_first(items):
>     return items[0]   # same work regardless of list size
> ```
>
> **O(n): linear time**
> ```python
> def find_max(items):
>     biggest = items[0]
>     for x in items:          # touches each item once
>         if x > biggest:
>             biggest = x
>     return biggest
> ```
>
> **O(n²): quadratic time**
> ```python
> def has_duplicate(items):
>     for i in range(len(items)):
>         for j in range(i + 1, len(items)):   # loop inside a loop
>             if items[i] == items[j]:
>                 return True
>     return False
> ```
>
> **O(log n): logarithmic time**
> ```python
> def binary_search(sorted_items, target):
>     lo, hi = 0, len(sorted_items) - 1
>     while lo <= hi:                 # search space halves each step
>         mid = (lo + hi) // 2
>         if sorted_items[mid] == target:
>             return mid
>         elif sorted_items[mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return -1
> ```
>
> ---
>
> ## Quick Rules for Analyzing Code
>
> 1. **Sequential steps add:** `O(n)` then `O(n)` → `O(2n)` → `O(n)`
> 2. **Nested loops multiply:** a loop of `n` inside a loop of `n` → `O(n²)`
> 3. **Halving the problem each step** → usually `O(log n)`
> 4. **Different inputs get different variables:** looping over list `a` then list `b` is `O(a + b)`, not `O(n)`
> 5. **Keep only the biggest term:** `O(n² + n)` → `O(n²)`
>
> ---
>
> ## Related Notations
>
> - **Big-O (O):** upper bound ("grows no faster than")
> - **Big-Omega (Ω):** lower bound ("grows at least as fast as")
> - **Big-Theta (Θ):** tight bound (both upper and lower)
>
> In casual use, people often say "Big-O" when they really mean Θ, the tight bound.
>
> You'll also see **best case**, **average case**, and **worst case**. For example, quicksort is `O(n log n)` on average but `O(n²)` in the worst case. Big-O is most often quoted for the worst case.
>
> ---
>
> ## Space Complexity
>
> Big-O also applies to **memory**. An algorithm that creates a copy of the input uses `O(n)` extra space, while one that uses just a few variables uses `O(1)` space.
>
> ---
>
> ## Caveats
>
> - Big-O ignores constants, so an `O(n)` algorithm with a huge constant can be slower than an `O(n²)` one for **small** inputs.
> - It describes **growth**, not actual runtime. Hardware, caching, and implementation details still matter in practice.
>
> ---
>
> **In one sentence:** Big-O tells you how badly an algorithm slows down as the input gets bigger, which lets you compare approaches without running them.

**Kevin** (143 words)

> Big-O describe how runtime or memory grow when input size `n` grow. Worst case, usually. Ignore constants and small terms; only growth shape matter.
>
> Common ones, fast to slow:
>
> | Big-O | Name | Example |
> |---|---|---|
> | `O(1)` | constant | array index lookup |
> | `O(log n)` | logarithmic | binary search |
> | `O(n)` | linear | loop over list once |
> | `O(n log n)` | linearithmic | merge sort |
> | `O(n²)` | quadratic | nested loop over same list |
> | `O(2ⁿ)` | exponential | naive recursive Fibonacci |
>
> Example: loop run `3n + 5` steps. Drop `3` and `5`. Still `O(n)`. Double input, double time.
>
> Why care: small input, all fast. Big input, `O(n²)` hurt bad, `O(log n)` barely notice.
>
> Related: Big-Ω mean lower bound, Big-Θ mean tight bound. People often say Big-O when mean Θ.

---

## What is a race condition?

**Normal** (418 words)

> A **race condition** is a bug that occurs when a program's behavior depends on the timing or order of events, such as which of two threads runs first, and that timing isn't controlled. The result can change from run to run, even with identical inputs.
>
> ## The Core Problem
>
> Race conditions typically happen when:
> 1. Two or more threads/processes access **shared data**
> 2. At least one of them **modifies** it
> 3. There's **no synchronization** controlling the order of access
>
> ## Classic Example
>
> Imagine two threads both incrementing a shared counter:
>
> ```python
> counter = 0
>
> def increment():
>     global counter
>     counter = counter + 1
> ```
>
> `counter = counter + 1` looks like one step, but it's actually three:
> 1. Read `counter`
> 2. Add 1
> 3. Write the result back
>
> If two threads interleave badly:
>
> | Step | Thread A | Thread B | counter |
> |------|----------|----------|---------|
> | 1 | reads 0 | | 0 |
> | 2 | | reads 0 | 0 |
> | 3 | writes 1 | | 1 |
> | 4 | | writes 1 | **1** |
>
> Both threads incremented, but the final value is **1 instead of 2**. One update was lost.
>
> ## Real-World Analogy
>
> Two people share a bank account with $100. Both check the balance at the same moment, see $100, and each withdraws $80. If the system doesn't coordinate them, both withdrawals succeed and the bank loses money.
>
> ## Common Types
>
> - **Read-modify-write**: the counter example above
> - **Check-then-act**: checking a condition, then acting on it after it may have changed (e.g., "if file doesn't exist, create it")
> - **TOCTOU (Time-of-Check to Time-of-Use)**: a security-relevant version of check-then-act
>
> ## How to Prevent Them
>
> - **Locks / mutexes**: only one thread can enter a critical section at a time
> - **Atomic operations**: hardware-guaranteed indivisible operations (e.g., atomic increment)
> - **Immutable data**: data that can't change can't be corrupted
> - **Message passing**: threads communicate by sending messages instead of sharing memory
> - **Transactions**: in databases, group operations so they succeed or fail as a unit
>
> Fixed example:
> ```python
> import threading
> lock = threading.Lock()
>
> def increment():
>     global counter
>     with lock:
>         counter = counter + 1
> ```
>
> ## Why They're Tricky
>
> Race conditions are notoriously hard to debug because they're **non-deterministic**. A program might work correctly thousands of times and then fail unpredictably, often only under heavy load or on different hardware. Adding print statements or a debugger can change the timing enough to hide the bug, which earns these bugs the nickname "heisenbugs."

**Kevin** (57 words)

> Race condition: two thread or process touch same data at same time, and result depend on who finish first. Order not controlled, so bug come and go.
>
> Example: two thread read `count = 5`, both add 1, both write `6`. Should be `7`. One update lost.
>
> Fix: lock, mutex, atomic operation, or design so data not shared.

---

## How does garbage collection work?

**Normal** (824 words)

> # How Garbage Collection Works
>
> **Garbage collection (GC)** is automatic memory management. The runtime finds memory your program no longer uses and frees it, so you don't have to call `free()` or `delete` yourself.
>
> ## The Core Idea: Reachability
>
> A GC can't know what you *intend* to use, so it approximates "no longer needed" with **"no longer reachable."**
>
> 1. **Roots** are starting points the program can access directly: local variables on the stack, global/static variables, and CPU registers.
> 2. Any object reachable by following references from a root is **live**.
> 3. Everything else is **garbage**, because the program has no way to reach it again.
>
> ```
> Roots → [A] → [B] → [C]
>               ↓
>              [D]
>
>         [E] → [F]      ← unreachable: garbage
> ```
>
> ## Main Approaches
>
> ### 1. Reference Counting
> Each object keeps a count of how many references point to it. When the count drops to zero, the object is freed immediately.
>
> - ✅ Memory is reclaimed promptly and predictably.
> - ❌ Cycles leak: if A points to B and B points to A, neither count reaches zero, even when both are unreachable.
> - ❌ Updating counts on every assignment costs time.
> - **Used by:** Python (plus a separate cycle detector), Swift/Objective-C (ARC), C++ `shared_ptr`.
>
> ### 2. Mark-and-Sweep (Tracing)
> - **Mark:** Start from the roots and traverse every reference, marking each object reached.
> - **Sweep:** Scan the whole heap and free every unmarked object.
>
> - ✅ Handles cycles naturally.
> - ❌ Classic versions pause the program ("stop-the-world").
> - ❌ Leaves the heap **fragmented**, with free space scattered in small gaps.
>
> ### 3. Mark-Compact
> Marks live objects like mark-and-sweep, then slides them together to one end of the heap and updates all references to their new locations.
>
> - ✅ Eliminates fragmentation.
> - ❌ Moving objects and fixing up pointers is expensive.
>
> ### 4. Copying Collection
> Splits the heap into two halves. Allocation happens in one half. At collection time, live objects are copied to the other half and the old half is wiped entirely.
>
> - ✅ Very fast when most objects are dead, since you only touch survivors.
> - ✅ Allocation is cheap: just bump a pointer.
> - ❌ Half the memory sits unused at any given time.
>
> ## Generational Collection: The Big Optimization
>
> Most real-world GCs (Java, .NET, JavaScript V8, Go to some extent) rely on the **generational hypothesis**: *most objects die young.* Temporary strings, iterators, and intermediate results are created and discarded quickly.
>
> So the heap is divided by age:
>
> | Generation | Contents | Collection strategy |
> |---|---|---|
> | **Young (nursery)** | Newly allocated objects | Collected often and cheaply, usually by copying |
> | **Old (tenured)** | Objects that survived several collections | Collected rarely, usually with mark-sweep or mark-compact |
>
> Objects that survive a few young-generation collections get **promoted** to the old generation.
>
> One complication is that old objects can point to young ones. To avoid scanning the entire old generation during a minor GC, the runtime uses a **write barrier**: a small piece of code that runs on pointer writes and records old→young references in a "remembered set."
>
> ## Reducing Pauses
>
> Stopping the whole program to collect can cause noticeable lag. Modern collectors use several techniques to shorten or hide pauses:
>
> - **Incremental GC:** does the work in small slices interleaved with program execution.
> - **Concurrent GC:** runs on separate threads alongside the program. Examples are Go's collector and Java's G1, ZGC, and Shenandoah.
> - **Parallel GC:** uses multiple threads during a pause so the pause finishes faster.
>
> Concurrent collectors must handle the program modifying references while marking is in progress. A common technique is **tri-color marking**, which sorts objects into three sets:
> - **White:** not yet seen (potential garbage)
> - **Gray:** seen, but its references haven't been scanned yet
> - **Black:** seen, and all its references scanned
>
> Barriers ensure a black object never ends up pointing to a white object that the collector would wrongly free.
>
> ## Trade-offs
>
> GC design balances three competing goals:
> - **Throughput:** the share of total time spent on real work rather than GC
> - **Latency:** how long individual pauses last
> - **Memory footprint:** how much extra heap space the collector needs
>
> Improving one usually costs another. That's why the JVM, for example, offers several collectors you can pick depending on your workload.
>
> ## Common Misconceptions
>
> - **"GC means no memory leaks."** Not quite. If you keep a reference to something you no longer need, such as an ever-growing cache or a forgotten event listener, it stays reachable and is never collected.
> - **"GC is always slow."** Generational collectors make allocation extremely cheap. For allocation-heavy code, GC can be faster than manual `malloc`/`free`.
> - **"Objects are freed as soon as they're unreachable."** That's only true for reference counting. Tracing collectors reclaim memory whenever they next run.
>
> ---
>
> Let me know if you'd like a deeper look at a specific runtime (Java, Go, Python, JavaScript), tri-color marking, or how GC compares to Rust's ownership model.

**Kevin** (234 words)

> Garbage collector find memory program no can reach anymore, then free it. Programmer no call `free`.
>
> **Core idea: reachability.** Start from roots: stack variables, globals, registers. Follow every pointer. Anything reached is alive. Anything not reached is garbage.
>
> **Main approach:**
> - **Reference counting:** each object count who point to it. Count hit zero, free now. Simple, prompt. Problem: cycles. A point to B, B point to A, nobody else point to them. Count never zero. Leak. Python use this plus cycle detector.
> - **Mark-and-sweep:** pause, mark everything reachable from roots, sweep heap, free unmarked. Handle cycles fine. Leave holes in memory.
> - **Mark-compact:** same, but slide live objects together. No fragmentation, fast allocation.
> - **Copying:** split heap in two. Copy live objects to other half, old half all garbage. Cost scale with live data, not heap size. Waste half memory.
>
> **Generational trick:** most objects die young. So heap split into young and old generation. Collect young one often, cheap. Survivor get promoted. Old generation collected rarely. Java, .NET, V8 do this.
>
> **Pause problem:** stopping program to collect cause latency spike. Modern collectors (Java G1/ZGC, Go) work incremental or concurrent, alongside program. Use write barriers to track pointer changes mid-collection. Pauses drop to milliseconds or less, cost some throughput.
>
> **Tradeoff:** GC buy safety, no dangling pointer, no double free, less manual work. Cost CPU, extra memory, less predictable timing. Rust and C++ pick ownership/RAII instead.

---

## What is dependency injection?

**Normal** (379 words)

> # Dependency Injection
>
> **Dependency injection (DI)** is a design pattern in which an object receives the things it needs (its *dependencies*) from the outside, instead of creating them itself.
>
> ## The Problem It Solves
>
> Without DI, a class builds its own dependencies:
>
> ```python
> class EmailService:
>     def send(self, to, message):
>         # actually sends an email
>         ...
>
> class UserRegistration:
>     def __init__(self):
>         self.email_service = EmailService()  # hard-coded dependency
>
>     def register(self, user):
>         # ... save user ...
>         self.email_service.send(user.email, "Welcome!")
> ```
>
> This causes several problems:
> - `UserRegistration` is **tightly coupled** to `EmailService`.
> - You **can't easily test** `register()` without sending real emails.
> - Switching to an `SmsService` or a different email provider requires **editing the class**.
>
> ## The DI Solution
>
> Pass the dependency in from the outside:
>
> ```python
> class UserRegistration:
>     def __init__(self, notifier):
>         self.notifier = notifier  # injected
>
>     def register(self, user):
>         # ... save user ...
>         self.notifier.send(user.email, "Welcome!")
>
> # Production
> registration = UserRegistration(EmailService())
>
> # Testing
> registration = UserRegistration(FakeNotifier())
> ```
>
> Now `UserRegistration` doesn't care *which* notifier it gets. It only needs something with a `send` method.
>
> ## Common Forms of Injection
>
> 1. **Constructor injection**: dependencies are passed when the object is created (most common and usually preferred).
> 2. **Setter/property injection**: dependencies are assigned after creation through a setter or property.
> 3. **Method/parameter injection**: a dependency is passed directly to the method that needs it.
>
> ## Benefits
>
> - **Testability**: swap real dependencies for mocks or fakes.
> - **Loose coupling**: classes depend on abstractions (interfaces), not concrete implementations.
> - **Flexibility**: change behavior by changing configuration, not code.
> - **Clarity**: a class's dependencies are visible in its constructor.
>
> ## DI Containers / Frameworks
>
> In larger applications, wiring everything together by hand can get tedious, so **DI containers** automate it. Examples:
> - **Java**: Spring, Guice, Dagger
> - **C#/.NET**: built-in `Microsoft.Extensions.DependencyInjection`
> - **TypeScript**: Angular's DI, NestJS, InversifyJS
> - **Python**: `dependency-injector`, FastAPI's `Depends`
>
> You don't *need* a framework, though. Passing objects into constructors manually is still dependency injection.
>
> ## Related Concept
>
> DI is one way to implement **Inversion of Control (IoC)**: instead of a class controlling how its dependencies are created, that control is "inverted" and handed to an outside party. It also supports the **Dependency Inversion Principle** (the "D" in SOLID): depend on abstractions, not concretions.
>
> **In one sentence:** Dependency injection means *"don't create what you need; ask for it."*

**Kevin** (69 words)

> Object get its dependencies from outside, not build them itself.
>
> Without DI:
> ```python
> class Service:
>     def __init__(self):
>         self.db = PostgresDB()  # hardwired
> ```
>
> With DI:
> ```python
> class Service:
>     def __init__(self, db):
>         self.db = db  # passed in
>
> svc = Service(PostgresDB())
> test_svc = Service(FakeDB())
> ```
>
> Why good: swap parts easy, test with fakes, less coupling. Frameworks like Spring or Angular can wire it automatic, but plain constructor passing count too.

---

## What is the difference between SQL and NoSQL databases?

**Normal** (435 words)

> # SQL vs. NoSQL Databases
>
> ## SQL (Relational) Databases
>
> SQL databases store data in **tables** made of rows and columns, with a predefined schema. Tables are linked through relationships such as foreign keys.
>
> **Examples:** PostgreSQL, MySQL, Oracle, SQL Server, SQLite
>
> **Key traits:**
> - **Fixed schema:** The structure must be defined before data is inserted.
> - **Query language:** SQL (Structured Query Language), which is standardized and powerful for complex queries and joins.
> - **ACID transactions:** Atomicity, Consistency, Isolation, and Durability guarantee reliable transactions.
> - **Scaling:** Traditionally **vertical**, meaning you add more power to a single server. Horizontal scaling is possible but more complex.
>
> ## NoSQL (Non-Relational) Databases
>
> NoSQL databases use flexible data models that don't rely on fixed tables. They come in several types:
>
> | Type | How data is stored | Examples |
> |------|-------------------|----------|
> | **Document** | JSON-like documents | MongoDB, CouchDB |
> | **Key-Value** | Simple key → value pairs | Redis, DynamoDB |
> | **Wide-Column** | Columns grouped into families | Cassandra, HBase |
> | **Graph** | Nodes and edges (relationships) | Neo4j, Amazon Neptune |
>
> **Key traits:**
> - **Flexible schema:** Records in the same collection can have different fields.
> - **Query methods:** Vary by database, with no single standard language.
> - **Consistency:** Many favor availability and partition tolerance, often with **eventual consistency** (following the BASE model), though many now offer ACID options.
> - **Scaling:** Designed for **horizontal** scaling across many servers.
>
> ## Side-by-Side Comparison
>
> | Feature | SQL | NoSQL |
> |--------|-----|-------|
> | Data model | Tables (rows/columns) | Documents, key-value, graph, wide-column |
> | Schema | Rigid, predefined | Dynamic, flexible |
> | Relationships | Strong (joins) | Often denormalized or embedded |
> | Transactions | Strong ACID | Varies, often eventual consistency |
> | Scaling | Vertical (mainly) | Horizontal |
> | Best for | Structured data, complex queries | Large-scale, rapidly changing, or unstructured data |
>
> ## When to Use Which
>
> **Choose SQL when:**
> - Data is structured and relationships matter (e.g., banking, e-commerce orders, inventory)
> - You need complex queries and reporting
> - Data integrity and transactions are critical
>
> **Choose NoSQL when:**
> - Your data structure changes frequently or is semi-structured
> - You need massive scale and high throughput (e.g., social media feeds, IoT, real-time analytics)
> - You need fast caching (Redis) or relationship-heavy traversal (graph databases)
>
> ## Bottom Line
>
> Neither is universally better. The right choice depends on your data shape, consistency needs, and scale. Many modern applications use **both** (called *polyglot persistence*), for example PostgreSQL for transactions and Redis for caching. The line has also blurred: PostgreSQL supports JSON documents, and MongoDB supports multi-document ACID transactions.

**Kevin** (152 words)

> SQL: relational. Tables, fixed schema, rows and columns. Use SQL query language. Strong ACID transaction. Scale mostly vertical (bigger server). Example: PostgreSQL, MySQL, SQL Server.
>
> NoSQL: non-relational. Flexible or no schema. Many model: document, key-value, wide-column, graph. Scale mostly horizontal (more server). Many trade strict consistency for speed and availability. Example: MongoDB, Redis, Cassandra, Neo4j.
>
> | | SQL | NoSQL |
> |---|---|---|
> | Data model | Tables, relations | Document, key-value, column, graph |
> | Schema | Fixed, defined upfront | Flexible |
> | Query | SQL, rich joins | Varies by database, joins limited |
> | Consistency | Strong (ACID) | Often eventual, some offer ACID |
> | Scaling | Mostly vertical | Mostly horizontal |
> | Good for | Structured data, complex queries, transactions | Huge scale, changing data shape, fast simple lookups |
>
> Lines blur now. Postgres store JSON. MongoDB do transactions. Pick by data shape and access pattern.

---

## What is a Docker container?

**Normal** (309 words)

> A **Docker container** is a lightweight, standalone, executable package that includes everything needed to run a piece of software: the code, runtime, system tools, libraries, and settings. It runs in an isolated environment on a host machine.
>
> ## Key Concepts
>
> **Image vs. container**
> - A **Docker image** is a read-only template, like a blueprint or recipe.
> - A **container** is a running instance of that image. You can run many containers from the same image.
>
> **Isolation**
> Containers use Linux kernel features to keep processes separate from each other and from the host:
> - **Namespaces** give each container its own view of processes, network, and filesystem.
> - **Control groups (cgroups)** limit how much CPU, memory, and I/O a container can use.
>
> ## Containers vs. Virtual Machines
>
> | Containers | Virtual Machines |
> |---|---|
> | Share the host OS kernel | Each runs a full guest OS |
> | Start in seconds or less | Take minutes to boot |
> | Megabytes in size | Often gigabytes in size |
> | Process-level isolation | Hardware-level isolation (stronger) |
>
> ## Why Use Containers?
>
> - **Consistency:** They avoid the "it works on my machine" problem, because the app runs the same in development, testing, and production.
> - **Portability:** They run anywhere Docker is installed, whether a laptop, server, or cloud.
> - **Efficiency:** Many containers can run on a single machine.
> - **Scalability:** They are easy to replicate and orchestrate with tools like Kubernetes.
> - **Microservices:** Each service can live in its own container.
>
> ## Simple Example
>
> A `Dockerfile` defines an image:
> ```dockerfile
> FROM python:3.12
> COPY app.py /app/
> WORKDIR /app
> CMD ["python", "app.py"]
> ```
>
> Build the image and run a container from it:
> ```bash
> docker build -t myapp .
> docker run myapp
> ```
>
> In short, a container is a portable, isolated box for your application that behaves the same way wherever you run it.

**Kevin** (53 words)

> Container is isolated box for app. Hold code plus everything app need: libraries, runtime, config. Run same on any machine with Docker.
>
> Not full virtual machine. Share host OS kernel, so start fast and use little memory.
>
> Built from **image**, a read-only template. Container is running copy of image. One image, many container.

---

## What is a hash function?

**Normal** (377 words)

> A **hash function** takes an input of any size, such as a word, a file, or a password, and produces a fixed-size output called a **hash** (or hash value, digest, or checksum).
>
> ## Simple Example
>
> Using the SHA-256 hash function:
>
> | Input | Output (hash) |
> |---|---|
> | `hello` | `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` |
> | `Hello` | `185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969` |
>
> Changing a single letter produces a completely different result.
>
> ## Key Properties
>
> 1. **Deterministic**: The same input always produces the same output.
> 2. **Fixed output size**: Whether the input is one character or a 10 GB file, the hash is always the same length.
> 3. **Fast to compute**: Generating a hash is quick.
>
> **Cryptographic** hash functions add stronger guarantees:
>
> 4. **One-way (preimage resistance)**: Given a hash, it's practically impossible to work out the original input.
> 5. **Avalanche effect**: A tiny change in the input drastically changes the output.
> 6. **Collision resistance**: It's extremely hard to find two different inputs that produce the same hash.
>
> ## Common Uses
>
> - **Data structures**: Hash tables (like dictionaries in Python or HashMaps in Java) use hashes to store and look up data quickly.
> - **Password storage**: Websites store hashes of passwords rather than the passwords themselves. When you log in, they hash what you typed and compare the results. Dedicated slow algorithms like bcrypt or Argon2 are used for this, not plain fast hashes.
> - **Data integrity**: Downloaded files often come with a hash so you can verify the file wasn't corrupted or tampered with.
> - **Digital signatures and certificates**: Documents are hashed before being signed.
> - **Blockchain**: Bitcoin and other cryptocurrencies rely heavily on hashing (SHA-256) to link blocks together.
> - **Deduplication**: Systems like Git identify files and changes by their hashes.
>
> ## Common Hash Functions
>
> - **SHA-256 / SHA-3**: Modern, secure cryptographic hashes.
> - **MD5 and SHA-1**: Older and now considered broken for security purposes, though still used for basic checksums.
> - **MurmurHash, xxHash**: Very fast, non-cryptographic hashes used in hash tables and similar applications.
>
> ## An Analogy
>
> A hash is like a **fingerprint** for data. It's small, unique to the input, and lets you identify or verify something without needing the whole thing. Just as you can't reconstruct a person from a fingerprint, you can't reconstruct the data from its hash.

**Kevin** (65 words)

> Hash function take any input, turn it into fixed-size output called hash. Same input always give same hash. Small change in input give totally different hash.
>
> Two main kind:
> - **Regular hash** (hash tables, checksums): fast, spread values evenly.
> - **Cryptographic hash** (SHA-256): also hard to reverse, hard to find two inputs with same hash. Used for passwords, signatures, file integrity.
>
> Example: `SHA-256("hello")` → `2cf24dba5fb0a30e...`

---

## How does DNS resolution work?

**Normal** (598 words)

> # How DNS Resolution Works
>
> DNS (Domain Name System) translates human-readable domain names like `www.example.com` into IP addresses like `93.184.216.34` that computers use to locate each other.
>
> ## The Key Players
>
> 1. **DNS Client (Stub Resolver):** Built into your operating system. It sends queries but does little work itself.
> 2. **Recursive Resolver:** Usually run by your ISP, or a public service like Google (8.8.8.8) or Cloudflare (1.1.1.1). It does the legwork of finding the answer.
> 3. **Root Name Servers:** 13 logical servers (labeled A–M, with hundreds of physical instances worldwide via anycast). They know where to find the TLD servers.
> 4. **TLD Name Servers:** Handle top-level domains like `.com`, `.org`, `.uk`.
> 5. **Authoritative Name Servers:** Hold the actual DNS records for a specific domain.
>
> ## Step-by-Step Resolution
>
> Suppose you type `www.example.com` into your browser:
>
> **1. Check local caches**
> - The browser checks its own DNS cache.
> - The OS checks its cache and the `hosts` file.
> - If an answer is found, resolution stops here.
>
> **2. Query the recursive resolver**
> Your computer asks the configured recursive resolver: *"What's the IP for www.example.com?"* If the resolver has a cached answer, it returns it immediately.
>
> **3. Resolver asks a root server**
> The root server responds: *"I don't know, but here are the name servers for `.com`."*
>
> **4. Resolver asks the `.com` TLD server**
> The TLD server responds: *"I don't know, but here are the authoritative name servers for `example.com`."*
>
> **5. Resolver asks the authoritative server**
> The authoritative server responds: *"`www.example.com` is at 93.184.216.34."*
>
> **6. Resolver returns the answer**
> The resolver caches the result and sends it back to your computer, which also caches it. Your browser can now connect to the IP address.
>
> ```
> You → Recursive Resolver → Root → TLD (.com) → Authoritative (example.com)
>                          ←      ←            ←  IP address returned
> ```
>
> ## Recursive vs. Iterative Queries
> - **Recursive:** Your client asks the resolver to return a final answer, and the resolver does all the work.
> - **Iterative:** The resolver asks each server in turn, and each one gives a referral ("ask this server next") rather than the full answer.
>
> ## Caching and TTL
> Every DNS record has a **TTL (Time To Live)**, measured in seconds, that tells resolvers how long to cache it. Caching:
> - Makes most lookups take milliseconds.
> - Reduces load on root and TLD servers.
> - Explains why DNS changes can take time to "propagate," since old records persist until their TTL expires.
>
> ## Common Record Types
>
> | Record | Purpose |
> |--------|---------|
> | **A** | Maps a name to an IPv4 address |
> | **AAAA** | Maps a name to an IPv6 address |
> | **CNAME** | Alias pointing to another domain name |
> | **MX** | Mail servers for the domain |
> | **NS** | Authoritative name servers for the domain |
> | **TXT** | Arbitrary text (used for verification, SPF, DKIM) |
> | **SOA** | Administrative info about the zone |
>
> ## Transport and Security
> - DNS traditionally uses **UDP port 53**. It falls back to TCP for large responses and zone transfers.
> - **DNSSEC** adds cryptographic signatures so resolvers can verify that responses haven't been tampered with.
> - **DNS over HTTPS (DoH)** and **DNS over TLS (DoT)** encrypt queries for privacy, preventing eavesdroppers from seeing which domains you look up.
>
> ## Try It Yourself
> You can watch resolution happen with command-line tools:
> ```bash
> dig www.example.com          # basic lookup
> dig +trace www.example.com   # shows each step from root to authoritative
> nslookup www.example.com     # works on Windows too
> ```
>
> The `+trace` option is especially useful because it shows each referral in the chain.

**Kevin** (143 words)

> Name turn into IP address. Steps:
>
> 1. **Local check.** Browser cache, then OS cache, then `hosts` file. Found? Done.
> 2. **Ask resolver.** OS send query to recursive resolver (ISP, router, or public like `8.8.8.8`, `1.1.1.1`). Resolver have cache too.
> 3. **Root server.** Resolver no know? Ask root. Root say "no know `example.com`, but here `.com` server."
> 4. **TLD server.** `.com` server say "here authoritative nameserver for `example.com`."
> 5. **Authoritative server.** Give real answer: `A` record (IPv4) or `AAAA` (IPv6). Maybe `CNAME` first, then resolver chase alias.
> 6. **Return and cache.** Resolver send IP back, everybody cache it for record's TTL.
>
> Then browser connect to IP.
>
> Extra:
> - Resolver do legwork (recursive). Root, TLD, authoritative only point or answer (iterative).
> - Usually UDP port 53. TCP for big response. DoH and DoT encrypt query.
> - DNSSEC sign record so resolver can verify no tampering.

---

## What is eventual consistency?

**Normal** (525 words)

> # Eventual Consistency
>
> **Eventual consistency** is a consistency model used in distributed systems. It guarantees that **if no new updates are made to a piece of data, all replicas will eventually converge to the same value**, but it does *not* guarantee that every read returns the most recent write right away.
>
> ## The Core Idea
>
> In a distributed database, data is copied (replicated) across multiple servers, often in different locations. When you write data to one node, it takes time for that change to reach the others. During that window:
>
> - Different nodes may return **different values** for the same data.
> - A read might return **stale (outdated) data**.
> - Eventually, once updates finish propagating, all nodes agree.
>
> ## A Simple Example
>
> Imagine you update your profile picture on a social network:
>
> 1. Your update is written to a server in New York.
> 2. A friend in Tokyo views your profile a second later. Their request hits a Tokyo server that hasn't received the update yet, so they **see your old picture**.
> 3. A few seconds later, the update replicates to Tokyo, and your friend **sees the new picture**.
>
> The system was briefly inconsistent but *eventually* became consistent.
>
> ## Why Use It?
>
> Eventual consistency is a trade-off rooted in the **CAP theorem**, which says a distributed system facing a network partition must choose between:
> - **Consistency** (everyone sees the same data at the same time), and
> - **Availability** (every request gets a response).
>
> Eventually consistent systems favor **availability and partition tolerance**, which gives:
>
> | Benefit | Explanation |
> |---|---|
> | **High availability** | Nodes can accept reads/writes even if others are unreachable |
> | **Low latency** | No need to wait for all replicas to confirm a write |
> | **Scalability** | Easier to distribute data across many servers and regions |
>
> ## The Downsides
>
> - **Stale reads**: Users may see outdated information.
> - **Conflicts**: Two nodes may accept conflicting writes simultaneously, requiring resolution strategies such as:
>   - *Last-write-wins* (based on timestamps)
>   - *Vector clocks* to detect concurrent updates
>   - *CRDTs* (Conflict-free Replicated Data Types) that merge automatically
> - **Harder application logic**: Developers must design around temporary inconsistency.
>
> ## Where It's Used
>
> - **Amazon DynamoDB** (by default), **Apache Cassandra**, **Riak**
> - **DNS**: record changes propagate gradually across the internet
> - **Social media feeds, like counts, shopping carts**: cases where brief inconsistency is acceptable
>
> ## Contrast with Strong Consistency
>
> | | Strong Consistency | Eventual Consistency |
> |---|---|---|
> | Read after write | Always sees latest value | May see old value |
> | Latency | Higher | Lower |
> | Availability during failures | May reject requests | Stays available |
> | Good for | Banking, inventory, bookings | Social feeds, caches, analytics |
>
> ## Variations
>
> There are also intermediate models that offer stronger guarantees than basic eventual consistency:
> - **Read-your-writes**: You always see your own updates.
> - **Monotonic reads**: You never see data go "backward" in time.
> - **Causal consistency**: Causally related operations are seen in order by everyone.
>
> **In short:** eventual consistency trades immediate accuracy for speed and availability, on the promise that the system will "catch up" and agree given enough time.

**Kevin** (58 words)

> Eventual consistency: distributed system promise that if writes stop, all replicas end up with same data eventually.
>
> Until then, reads can return old value. Example: you update profile picture, friend still see old one for few second.
>
> System trade strict consistency for availability and speed, especially during network partition (CAP theorem). Used by DNS, Cassandra, DynamoDB default reads.

---

## What is the difference between the stack and the heap?

**Normal** (445 words)

> # Stack vs. Heap
>
> Both are regions of memory a program uses at runtime, but they're managed very differently.
>
> ## The Stack
>
> The stack stores data tied to **function calls**: local variables, function parameters, and return addresses.
>
> - **Automatic management.** Memory is allocated when a function is called and freed when it returns. You don't have to do anything.
> - **LIFO (Last In, First Out).** Each function call pushes a "stack frame," and returning pops it off.
> - **Very fast.** Allocation just moves a pointer, and the memory is usually hot in the CPU cache.
> - **Limited size.** It's typically a few MB per thread. Deep recursion or huge local arrays can cause a **stack overflow**.
> - **Fixed lifetime.** Data disappears when the function returns.
> - **Size known at compile time** (generally).
>
> ## The Heap
>
> The heap is a large pool of memory for **dynamic allocation**.
>
> - **Manual or garbage-collected management.** You request memory explicitly (`malloc`, `new`), and it's freed either by you (`free`, `delete`) or by a garbage collector (Java, Python, C#, Go).
> - **Flexible lifetime.** Data lives until it's freed, so it can outlive the function that created it.
> - **Slower.** The allocator has to find a suitable free block, and access may involve pointer indirection and cache misses.
> - **Much larger.** It's limited mainly by available system memory.
> - **Supports runtime-determined sizes.** For example, an array whose length comes from user input.
> - **Can fragment** over time.
>
> ## Example (C)
>
> ```c
> void example() {
>     int x = 10;                          // on the stack
>     int *p = malloc(sizeof(int) * 100);  // p itself is on the stack,
>                                          // but the 100 ints are on the heap
>     // ...
>     free(p);                             // heap memory must be freed manually
> }   // x and p vanish automatically here
> ```
>
> ## Quick Comparison
>
> | | Stack | Heap |
> |---|---|---|
> | Allocation | Automatic | Manual / GC |
> | Speed | Very fast | Slower |
> | Size | Small, fixed | Large, flexible |
> | Lifetime | Function scope | Until freed |
> | Access pattern | LIFO | Arbitrary |
> | Common bugs | Stack overflow | Memory leaks, dangling pointers, double free |
> | Thread scope | One per thread | Shared across threads |
>
> ## Rule of Thumb
>
> - Use the **stack** for small, short-lived data whose size is known in advance.
> - Use the **heap** when data is large, its size is only known at runtime, or it must outlive the current function.
>
> In higher-level languages (Python, Java, JavaScript), most objects live on the heap automatically, and you rarely choose explicitly. The distinction matters most in systems languages like C, C++, and Rust.

**Kevin** (78 words)

> Stack: fast, automatic memory for function calls. Each call push frame (locals, return address). Function return, frame gone. Fixed size, small. Too deep recursion → stack overflow.
>
> Heap: big pool for memory you request at runtime (`malloc`, `new`, objects). Lives until freed or garbage collected. Slower: allocator must find space, and memory can fragment. Forget free in C/C++ → leak.
>
> Rule of thumb: small, short-lived, known size → stack. Big, variable size, or must outlive function → heap.

---

## What is idempotency in an API?

**Normal** (529 words)

> # Idempotency in APIs
>
> An operation is **idempotent** if performing it multiple times has the **same effect on the server as performing it once**.
>
> Calling it once or ten times leaves the system in the same final state.
>
> ## Why It Matters
>
> Networks are unreliable. A client might send a request, and then:
> - The connection times out before the response arrives
> - The server processed the request but the response was lost
> - The client crashes and restarts
>
> The client often **can't tell whether the request succeeded**, so it retries. If the operation isn't idempotent, retrying can cause problems like **charging a customer twice** or **creating duplicate orders**.
>
> ## Idempotency of HTTP Methods
>
> | Method | Idempotent? | Why |
> |--------|-------------|-----|
> | `GET` | ✅ Yes | Only reads data; doesn't change state |
> | `PUT` | ✅ Yes | Replaces a resource with a given state. Setting it to the same value twice gives the same result |
> | `DELETE` | ✅ Yes | Deleting something already deleted leaves it deleted |
> | `HEAD`, `OPTIONS` | ✅ Yes | Read-only |
> | `POST` | ❌ No (by default) | Typically creates a new resource each time |
> | `PATCH` | ⚠️ Depends | `{"name": "Bob"}` is idempotent; `{"op": "increment"}` is not |
>
> ### Examples
>
> **Idempotent:**
> ```http
> PUT /users/42
> { "email": "alice@example.com" }
> ```
> Sending this 5 times still leaves user 42 with that email.
>
> **Not idempotent:**
> ```http
> POST /orders
> { "item": "book", "qty": 1 }
> ```
> Sending this 5 times could create 5 orders.
>
> ## Idempotent ≠ Same Response
>
> Idempotency concerns the **server's state**, not the response. For example:
> - First `DELETE /users/42` returns `200 OK`
> - Second `DELETE /users/42` returns `404 Not Found`
>
> It's still idempotent because the end state (user 42 doesn't exist) is identical.
>
> ## Making `POST` Idempotent: Idempotency Keys
>
> A common pattern, used by Stripe, PayPal, and others, is for the client to generate a unique key and send it with the request:
>
> ```http
> POST /payments
> Idempotency-Key: 8f14e45f-ceea-4e7a-9b2c-1a2b3c4d5e6f
>
> { "amount": 5000, "currency": "usd" }
> ```
>
> **How the server handles it:**
> 1. Check whether this key has been seen before.
> 2. **If not:** process the request, then store the key along with the result.
> 3. **If yes:** skip processing and return the stored result.
>
> ```python
> def create_payment(request):
>     key = request.headers.get("Idempotency-Key")
>
>     existing = db.find_idempotency_record(key)
>     if existing:
>         return existing.response  # replay the original result
>
>     result = charge_card(request.body)
>     db.save_idempotency_record(key, result)
>     return result
> ```
>
> **Implementation details to consider:**
> - **Concurrency:** Two identical requests arriving at once need a lock or unique constraint so both don't get processed.
> - **Expiration:** Keys are usually kept for a limited time (e.g., 24 hours).
> - **Payload validation:** Reject a request that reuses a key with a *different* body.
>
> ## Related Concept: Safe Methods
>
> A **safe** method doesn't modify state at all (`GET`, `HEAD`, `OPTIONS`).
> - All safe methods are idempotent.
> - Not all idempotent methods are safe. `PUT` and `DELETE` change state but are still idempotent.
>
> ## Summary
>
> > **Idempotency means you can safely retry a request without causing unintended side effects.**
>
> It's essential for building reliable distributed systems, especially for payments, order processing, and any operation where duplicates would be harmful.

**Kevin** (91 words)

> Idempotent call: do same request many times, same result as doing once. No extra side effect.
>
> - `GET`, `PUT`, `DELETE`: idempotent. `PUT` same data twice, resource same. `DELETE` twice, still gone (second may return 404, but state same).
> - `POST`: usually not. Send twice, maybe two order, two charge.
>
> Why matter: network fail, client retry. Idempotent call safe to retry. For `POST`, many APIs use **idempotency key**: client send unique ID in header (e.g. `Idempotency-Key`). Server see repeat key, return first result, no do work again. Stripe do this for payments.

---

## How does OAuth work?

**Normal** (805 words)

> # How OAuth Works
>
> **OAuth** (specifically OAuth 2.0) is an authorization framework that lets an application access your data on another service **without you giving that application your password**.
>
> ## The Problem It Solves
>
> Say a photo-printing app wants to access your Google Photos. Without OAuth, you'd have to give the app your Google password, which means:
> - The app has full access to your entire Google account
> - You can't revoke access without changing your password
> - If the app is compromised, so is your account
>
> OAuth solves this by issuing **limited, revocable access tokens** instead of sharing credentials.
>
> ## The Key Players
>
> | Role | Description | Example |
> |------|-------------|---------|
> | **Resource Owner** | You, the user who owns the data | You |
> | **Client** | The app requesting access | Photo-printing app |
> | **Authorization Server** | Verifies your identity and issues tokens | Google's login/consent service |
> | **Resource Server** | Hosts the protected data | Google Photos API |
>
> ## The Most Common Flow: Authorization Code
>
> ```
> ┌──────┐                ┌────────┐               ┌───────────────┐   ┌──────────┐
> │ User │                │ Client │               │ Auth Server   │   │ Resource │
> └──┬───┘                └───┬────┘               └──────┬────────┘   └────┬─────┘
>    │ 1. "Connect Google"    │                           │                 │
>    │───────────────────────>│                           │                 │
>    │ 2. Redirect to Google  │                           │                 │
>    │<───────────────────────│                           │                 │
>    │ 3. Log in & approve permissions                    │                 │
>    │───────────────────────────────────────────────────>│                 │
>    │ 4. Redirect back with authorization code           │                 │
>    │<───────────────────────────────────────────────────│                 │
>    │───────────────────────>│                           │                 │
>    │                        │ 5. Exchange code (+secret)│                 │
>    │                        │──────────────────────────>│                 │
>    │                        │ 6. Access token           │                 │
>    │                        │<──────────────────────────│                 │
>    │                        │ 7. API request with token                   │
>    │                        │────────────────────────────────────────────>│
>    │                        │ 8. Your data                                │
>    │                        │<────────────────────────────────────────────│
> ```
>
> ### Step by step:
>
> 1. **You click "Connect with Google"** in the app.
> 2. **The app redirects you to Google**, with a URL like:
>    ```
>    https://accounts.google.com/o/oauth2/auth?
>      client_id=abc123
>      &redirect_uri=https://printapp.com/callback
>      &response_type=code
>      &scope=photos.readonly
>      &state=xyz789
>    ```
> 3. **You log in to Google directly** (the app never sees your password) and see a consent screen: *"PrintApp wants to view your photos. Allow?"*
> 4. **Google redirects you back** to the app with a short-lived **authorization code**.
> 5. **The app's server exchanges that code** with Google (behind the scenes, authenticated with its client secret).
> 6. **Google returns an access token** (and often a refresh token).
> 7. **The app calls the API**, including the token in the request header:
>    ```
>    Authorization: Bearer eyJhbGciOi...
>    ```
> 8. **The API validates the token** and returns the data.
>
> ## Key Concepts
>
> **Scopes** define what the token can do, e.g. `photos.readonly` vs. `photos.write`. You only grant what's requested, and good apps request the minimum.
>
> **Access tokens** are short-lived (often minutes to an hour) to limit damage if stolen.
>
> **Refresh tokens** are longer-lived and let the app get new access tokens without making you log in again.
>
> **The `state` parameter** is a random value that protects against CSRF attacks by ensuring the response matches the request the app actually made.
>
> **PKCE** (Proof Key for Code Exchange, pronounced "pixie") is an extension where the app generates a secret, sends a hashed version at the start, and proves it holds the original when exchanging the code. This prevents intercepted codes from being used. It's essential for mobile and single-page apps that can't safely store a client secret, and is now recommended for all clients.
>
> ## Why the Extra Step with the Code?
>
> Why not just return the token directly in step 4? Because the redirect happens through your browser, where URLs can leak via history, logs, or referrer headers. The code is useless on its own: it's short-lived, single-use, and requires the client secret (or PKCE verifier) to redeem. The actual token is delivered over a direct server-to-server connection.
>
> ## Other Flows
>
> - **Client Credentials**: For machine-to-machine communication with no user involved (e.g., a backend service calling another API).
> - **Device Code**: For devices with limited input, like smart TVs ("Go to example.com/device and enter code ABCD-1234").
> - **Implicit** and **Password** flows: Older flows that are now **deprecated** for security reasons.
>
> ## OAuth vs. Authentication
>
> A common confusion: **OAuth is for authorization (what you can access), not authentication (who you are).** An access token says "the bearer may read photos," not "this is Alice."
>
> **OpenID Connect (OIDC)** is a layer built on top of OAuth 2.0 that adds authentication. It issues an additional **ID token** (a JWT) containing identity information about the user. When you "Sign in with Google," you're typically using OIDC.
>
> ## A Helpful Analogy
>
> OAuth is like a **hotel key card**. The front desk (authorization server) verifies your identity and gives you a card (access token) that opens only specific doors (scopes) for a limited time. The doors (resource server) don't need to know who you are; they just check whether the card is valid. And the hotel can deactivate the card at any time without changing every lock.

**Kevin** (182 words)

> OAuth let app use your stuff on another service without getting your password.
>
> Common flow (authorization code):
>
> 1. App send you to service login page (say, Google) with requested scopes, like "read email."
> 2. You log in there and approve. App never see password.
> 3. Service redirect you back to app with short-lived **authorization code**.
> 4. App server swap code plus its **client secret** for **access token**. This happen backend to backend, not in browser.
> 5. App call service API with access token. Service check token, return data.
> 6. Token expire. App use **refresh token** to get new one without asking you again.
>
> Roles:
> - **Resource owner**: you
> - **Client**: app wanting access
> - **Authorization server**: issue token
> - **Resource server**: API holding data
>
> Key point: token have limited scope and lifetime, and you can revoke it without changing password.
>
> Apps with no safe place for secret (mobile, single-page) add **PKCE**: random one-time secret proving same app that started flow is one finishing it.
>
> OAuth only handle authorization ("what app can do"). Login ("who you are") need **OpenID Connect**, built on top.

---

## What is a deadlock?

**Normal** (450 words)

> ## Deadlock
>
> A **deadlock** happens when two or more processes or threads are each waiting for the other to release a resource, so none of them can ever proceed. They are permanently stuck.
>
> ### A Simple Example
>
> Imagine two threads and two locks:
>
> - **Thread A** locks **Resource 1**, then tries to lock **Resource 2**.
> - **Thread B** locks **Resource 2**, then tries to lock **Resource 1**.
>
> ```
> Thread A: holds R1 ──waits for──► R2
> Thread B: holds R2 ──waits for──► R1
> ```
>
> Each thread holds what the other needs, and neither will let go. Both wait forever.
>
> A real-world analogy: two cars meet on a one-lane bridge from opposite directions, and neither will back up.
>
> ### Code Example (Python)
>
> ```python
> import threading
>
> lock1 = threading.Lock()
> lock2 = threading.Lock()
>
> def task_a():
>     with lock1:
>         with lock2:   # waits for lock2
>             print("A done")
>
> def task_b():
>     with lock2:
>         with lock1:   # waits for lock1
>             print("B done")
>
> threading.Thread(target=task_a).start()
> threading.Thread(target=task_b).start()
> ```
>
> If each thread grabs its first lock before the other grabs its second, the program hangs.
>
> ### The Four Necessary Conditions (Coffman Conditions)
>
> A deadlock can only occur if **all four** of these hold at the same time:
>
> 1. **Mutual exclusion**: A resource can be held by only one process at a time.
> 2. **Hold and wait**: A process holds at least one resource while waiting for others.
> 3. **No preemption**: Resources can't be forcibly taken away; they must be released voluntarily.
> 4. **Circular wait**: There is a cycle of processes, each waiting for a resource held by the next.
>
> ### Handling Deadlocks
>
> You can deal with deadlocks by breaking at least one of the conditions above:
>
> - **Prevention**:
>   - *Lock ordering*: Always acquire locks in the same global order. This breaks circular wait and is the most common practical fix.
>   - Request all needed resources at once. This breaks hold and wait.
>   - Allow resources to be preempted.
> - **Avoidance**: Check each resource request and only grant it if the system stays in a "safe" state (e.g., the **Banker's Algorithm**).
> - **Detection and recovery**: Let deadlocks happen, detect cycles in a resource-allocation graph, then kill or roll back a process.
> - **Timeouts**: Use `try_lock` or lock timeouts so a thread gives up instead of waiting forever.
> - **Ignore it**: Some systems, including many general-purpose operating systems, assume deadlocks are rare and leave them for the user or developer to resolve (the "ostrich algorithm").
>
> ### Related Concepts
>
> - **Livelock**: Processes keep changing state in response to each other but still make no progress, like two people stepping side to side in a hallway.
> - **Starvation**: A process waits indefinitely because others keep getting priority, even though the system as a whole is making progress.

**Kevin** (93 words)

> Deadlock: two or more thread each hold lock, each wait for lock other one hold. Nobody let go. Everybody stuck forever.
>
> Example: Thread A hold lock 1, want lock 2. Thread B hold lock 2, want lock 1. Both wait. Nothing happen.
>
> Need four condition together:
> - **Mutual exclusion**: resource only one holder at time.
> - **Hold and wait**: hold one, wait for another.
> - **No preemption**: nobody force lock away.
> - **Circular wait**: cycle of waiting.
>
> Break any one, no deadlock. Common fix: always grab locks in same order, or use timeout.

---

## Explain the CAP theorem.

**Normal** (589 words)

> # The CAP Theorem
>
> The **CAP theorem** (also called Brewer's theorem) is a fundamental result about **distributed data systems**, meaning systems where data is stored across multiple machines that communicate over a network. Eric Brewer proposed it in 2000, and Seth Gilbert and Nancy Lynch formally proved it in 2002.
>
> ## The Three Properties
>
> **C: Consistency**
> Every read receives the most recent write or an error. All nodes see the same data at the same time. (Technically this means *linearizability*: the system behaves as if there were a single copy of the data.)
>
> **A: Availability**
> Every request to a non-failing node receives a response, without a guarantee that it reflects the most recent write. The system never refuses to answer.
>
> **P: Partition Tolerance**
> The system keeps operating even when the network drops or delays messages between nodes, splitting them into groups that can't communicate.
>
> ## The Theorem
>
> > When a network partition occurs, a distributed system must choose between **consistency** and **availability**. It cannot guarantee both.
>
> This is often summarized as "pick two out of three," but that phrasing is misleading (see below).
>
> ## Why It's True: A Simple Example
>
> Imagine two database nodes, **A** and **B**, that replicate data to each other. A network failure cuts the link between them.
>
> A client writes `x = 5` to node A. Another client then reads `x` from node B. Node B has two options:
>
> 1. **Refuse to answer or return an error** until it can confirm the latest value with A. This preserves **consistency** but sacrifices **availability**.
> 2. **Return its last known value** (say, `x = 3`). This preserves **availability** but sacrifices **consistency**.
>
> No third option exists. B cannot know about a write it never received.
>
> ## The Common Misconception: "Pick Two"
>
> In a real distributed system, **network partitions are not optional**. Networks fail, packets get lost, and machines become unreachable. You can't choose to give up partition tolerance.
>
> So the real choice is:
>
> - **CP (Consistency + Partition tolerance):** During a partition, some requests fail or block to avoid returning stale data.
>   *Examples: HBase, ZooKeeper, etcd, MongoDB (with default settings), traditional RDBMS clusters with synchronous replication*
>
> - **AP (Availability + Partition tolerance):** During a partition, all nodes keep responding, but they may return stale or conflicting data, which is reconciled later (*eventual consistency*).
>   *Examples: Cassandra, DynamoDB (default), Riak, CouchDB, DNS*
>
> A "CA" system only makes sense if there's no network to partition, such as a single-node database.
>
> Also note that the trade-off only applies **during a partition**. When the network is healthy, a system can provide both consistency and availability.
>
> ## Beyond CAP: PACELC
>
> Because CAP only describes behavior during failures, Daniel Abadi proposed the **PACELC** theorem as an extension:
>
> > If there is a **P**artition, choose between **A**vailability and **C**onsistency;
> > **E**lse (normal operation), choose between **L**atency and **C**onsistency.
>
> Even without failures, keeping replicas strongly consistent requires coordination between nodes, which adds latency. For example:
> - **Cassandra / DynamoDB:** PA/EL (favor availability and low latency)
> - **HBase / traditional RDBMS:** PC/EC (favor consistency in both cases)
>
> ## Practical Takeaways
>
> - CAP is about **trade-offs under failure**, not a permanent classification. Many modern databases let you tune consistency per operation (e.g., Cassandra's quorum levels).
> - Choose based on your application's needs:
>   - **Banking, inventory, leader election:** Stale data is dangerous, so lean toward **CP**.
>   - **Social feeds, shopping carts, caching:** Uptime matters more than perfect freshness, so lean toward **AP**.
> - "Consistency" in CAP is different from the "C" in **ACID**, which refers to maintaining database invariants and constraints.

**Kevin** (142 words)

> Distributed system can only guarantee two of three. Really: when network split, must pick consistency or availability.
>
> - **Consistency (C):** every read get latest write or error. All node agree.
> - **Availability (A):** every request to working node get answer, maybe stale.
> - **Partition tolerance (P):** system keep working when network drop messages between node.
>
> Network partition always possible, so P not optional. Real choice happen during partition:
>
> - **CP:** refuse or error some request to stay correct. Example: ZooKeeper, etcd, HBase.
> - **AP:** answer everything, maybe stale data, fix later (eventual consistency). Example: Cassandra, CouchDB, DynamoDB default.
>
> No partition? System can have both C and A. Many database also let you tune choice per request.
>
> Caveat: "consistency" here mean linearizability, not ACID "C." Theorem also ignore latency. PACELC extend it: during **P**artition pick **A** or **C**, **E**lse pick **L**atency or **C**onsistency.

---

## What does a load balancer do?

**Normal** (313 words)

> A **load balancer** distributes incoming network traffic across multiple servers so that no single server gets overwhelmed. It sits between users (clients) and a group of backend servers, acting like a traffic director.
>
> ## Main Functions
>
> 1. **Distributing traffic**: It spreads requests across servers to keep the workload even.
> 2. **Ensuring high availability**: It runs health checks on servers. If one fails, traffic is automatically rerouted to healthy ones, so users don't notice the outage.
> 3. **Enabling scalability**: You can add or remove servers as demand changes without disrupting service.
> 4. **Improving performance**: Spreading the load keeps response times fast.
>
> ## Common Distribution Methods
>
> - **Round Robin**: Sends requests to each server in turn.
> - **Least Connections**: Sends traffic to the server with the fewest active connections.
> - **IP Hash**: Uses the client's IP address to pick a server, so the same user consistently reaches the same server.
> - **Weighted**: Gives more traffic to more powerful servers.
>
> ## Types
>
> - **Layer 4 (Transport)**: Routes based on IP addresses and ports. It's fast but doesn't inspect content.
> - **Layer 7 (Application)**: Routes based on content such as URLs, headers, or cookies. For example, it can send `/images` requests to one server group and `/api` requests to another.
>
> ## Extra Features
>
> - **SSL/TLS termination**: Handles encryption and decryption, freeing backend servers from that work.
> - **Session persistence ("sticky sessions")**: Keeps a user tied to the same server when needed.
> - **Security**: Can help absorb DDoS attacks and hide backend server details.
>
> ## Examples
>
> - **Hardware**: F5, Citrix ADC
> - **Software**: NGINX, HAProxy
> - **Cloud**: AWS Elastic Load Balancing, Google Cloud Load Balancing, Azure Load Balancer
>
> **Analogy:** A load balancer is like a host at a busy restaurant who seats guests across different waiters' sections so no single waiter gets swamped. If a waiter goes home sick, the host simply stops seating people in that section.

**Kevin** (50 words)

> Spread incoming traffic across many server, so no one server get crushed.
>
> Also:
> - Health check. Dead server get skipped.
> - Add or remove server without downtime.
> - Sometimes end TLS, or keep same user on same server (sticky session).
>
> Common pick method: round robin, least connection, hash by IP.

---

## What is the difference between a cache and a database?

**Normal** (439 words)

> A **database** is the authoritative, durable store of your data. A **cache** is a fast, temporary copy of some of that data, kept close to where it's needed so it can be read quickly.
>
> ## Core Differences
>
> | Aspect | Database | Cache |
> |---|---|---|
> | **Purpose** | Store data permanently and reliably | Speed up access to frequently used data |
> | **Source of truth** | Yes, it's the "real" data | No, it holds a copy of data from elsewhere |
> | **Storage medium** | Usually disk (SSD/HDD) | Usually memory (RAM) |
> | **Speed** | Slower (milliseconds) | Very fast (microseconds to sub-millisecond) |
> | **Durability** | Data survives crashes and restarts | Data can be lost, and that's acceptable |
> | **Capacity** | Large (terabytes or more) | Smaller and limited by memory |
> | **Data lifetime** | Kept until explicitly deleted | Expires or gets evicted (TTL, LRU, etc.) |
> | **Query capability** | Rich (SQL, joins, indexes, transactions) | Usually simple key-value lookups |
> | **Consistency** | Strong guarantees (e.g., ACID) | May be stale or out of sync |
>
> ## How They Work Together
>
> Caches usually sit in front of databases:
>
> ```
> User request → Check cache
>                  ├── Hit  → return data immediately (fast)
>                  └── Miss → query database → store result in cache → return data
> ```
>
> This pattern is called **cache-aside**. It reduces load on the database and cuts response times.
>
> ## Analogy
>
> - **Database** = a library's archive. It holds every book and is organized and permanent, but retrieving something takes time.
> - **Cache** = the stack of books on your desk. It's small and quick to grab from, but it's only copies of what you're using now, and you clear it off regularly.
>
> ## Common Examples
>
> - **Databases:** PostgreSQL, MySQL, MongoDB, Oracle, Cassandra
> - **Caches:** Redis, Memcached, CDN edge caches, browser caches, CPU L1/L2 caches
>
> ## Key Challenges with Caches
>
> - **Cache invalidation:** keeping cached data in sync when the database changes. It's famously one of the "two hard things" in computer science.
> - **Stale data:** users might see outdated information.
> - **Cold starts:** an empty cache after a restart sends a burst of traffic to the database.
>
> ## The Line Can Blur
>
> Some tools act as both. Redis, for example, can persist data to disk and is sometimes used as a primary database. Databases also have their own internal caches, such as buffer pools. The distinction is really about **role**: is this the source of truth, or a fast copy for performance?
>
> **In short:** use a database to *keep* data and a cache to *serve* data faster.

**Kevin** (49 words)

> **Cache:** fast, temporary copy of data, usually in memory. Speed up reads. Can lose data anytime (eviction, restart). Not source of truth.
>
> **Database:** durable, persistent storage on disk. Source of truth. Support queries, transactions, consistency guarantee.
>
> Common pattern: app check cache first. Miss? Read database, store result in cache.

---

## What is a webhook?

**Normal** (372 words)

> A **webhook** is a way for one application to automatically send real-time data to another application when a specific event happens. Instead of your app repeatedly asking another service "Anything new?", the service tells your app the moment something occurs.
>
> ## How It Works
>
> 1. **You register a URL** with a service. This is an endpoint on your server, like `https://myapp.com/webhooks/payment`.
> 2. **An event occurs** in that service, such as a payment completing or a new commit being pushed.
> 3. **The service sends an HTTP request**, usually a POST, to your URL with details about the event, typically in JSON.
> 4. **Your server receives and processes it**, for example by updating a database or sending an email.
>
> ## Webhooks vs. Polling
>
> | Polling | Webhooks |
> |---|---|
> | Your app repeatedly asks "Any updates?" | The service pushes updates to you |
> | Wastes requests when nothing has changed | Requests happen only when something happens |
> | Updates are delayed by the polling interval | Updates arrive in near real time |
>
> A common analogy: polling is calling the pizza shop every 5 minutes to ask if your order is ready. A webhook is the shop calling you when it's ready.
>
> ## Common Examples
>
> - **Stripe** notifies your app when a payment succeeds or fails.
> - **GitHub** triggers a CI/CD pipeline when code is pushed.
> - **Slack** posts a message to a channel when an external event occurs.
> - **Shopify** alerts your inventory system when an order is placed.
>
> ## Example Payload
>
> ```json
> POST /webhooks/payment
> Content-Type: application/json
>
> {
>   "event": "payment.succeeded",
>   "data": {
>     "id": "pay_12345",
>     "amount": 4999,
>     "currency": "usd",
>     "customer": "cus_678"
>   }
> }
> ```
>
> ## Key Considerations
>
> - **Security:** Verify that requests actually come from the expected service, usually by checking a signature in the request headers.
> - **Reliability:** Respond quickly with a 2xx status code. Many services retry if your endpoint fails or times out.
> - **Idempotency:** The same event may be delivered more than once, so design your handler to process duplicates safely.
> - **Public accessibility:** Your endpoint must be reachable over the internet. Tools like ngrok help with local testing.
>
> In short, webhooks are a simple, efficient way for apps to communicate events to each other as they happen.

**Kevin** (33 words)

> Webhook is HTTP callback. When event happen, one app send POST request to URL you give it. Push, not poll.
>
> Example: payment succeed, Stripe POST event data to `https://yourapp.com/webhooks/stripe`. Your server handle it.

---

## What is recursion?

**Normal** (361 words)

> **Recursion** is when something is defined in terms of itself. In programming, it means **a function that calls itself** to solve a problem by breaking it into smaller versions of the same problem.
>
> ## The Two Essential Parts
>
> Every recursive function needs:
>
> 1. **Base case**: A condition where the function stops calling itself and returns a direct answer. Without it, the function would call itself forever.
> 2. **Recursive case**: The part where the function calls itself with a smaller or simpler input, moving toward the base case.
>
> ## Classic Example: Factorial
>
> The factorial of *n* (written *n!*) is `n × (n-1) × (n-2) × ... × 1`. Notice that `5! = 5 × 4!`, so the problem contains a smaller version of itself.
>
> ```python
> def factorial(n):
>     if n == 1:              # Base case
>         return 1
>     return n * factorial(n - 1)   # Recursive case
> ```
>
> **How `factorial(4)` unfolds:**
> ```
> factorial(4)
> = 4 * factorial(3)
> = 4 * 3 * factorial(2)
> = 4 * 3 * 2 * factorial(1)
> = 4 * 3 * 2 * 1
> = 24
> ```
>
> ## A Real-World Analogy
>
> Imagine you're in a long line and want to know your position. You ask the person in front of you, "What's your position?" They ask the person in front of them, and so on, until the person at the front says "I'm #1" (base case). Then each person adds 1 and passes the answer back.
>
> ## When Recursion Is Useful
>
> - **Tree and graph structures** (file systems, HTML documents, family trees)
> - **Divide-and-conquer algorithms** (merge sort, quicksort, binary search)
> - **Problems with naturally self-similar structure** (fractals, Fibonacci, Tower of Hanoi)
>
> ## Things to Watch Out For
>
> - **Stack overflow**: Each call uses memory on the call stack. Too many nested calls, often from a missing or unreachable base case, will crash the program.
> - **Inefficiency**: Some naive recursive solutions recompute the same values repeatedly. Computing Fibonacci numbers this way is a well-known example. Techniques like *memoization* fix this.
> - **Iteration alternative**: Any recursive solution can also be written with loops, which is sometimes more efficient.
>
> And the classic joke: *"To understand recursion, you must first understand recursion."* 😄

**Kevin** (70 words)

> Function call itself. Each call solve smaller piece of same problem until hit **base case**, where it stop.
>
> Example, factorial:
>
> ```python
> def factorial(n):
>     if n <= 1:        # base case
>         return 1
>     return n * factorial(n - 1)  # recursive call
> ```
>
> `factorial(3)` → `3 * factorial(2)` → `3 * 2 * factorial(1)` → `3 * 2 * 1` = 6.
>
> No base case means infinite calls, then stack overflow.

---

## What is the difference between let and var in JavaScript?

**Normal** (412 words)

> # `let` vs `var` in JavaScript
>
> Both declare variables, but they behave differently in several important ways.
>
> ## 1. Scope
>
> **`var` is function-scoped**, while **`let` is block-scoped** (limited to the nearest `{ }`).
>
> ```javascript
> function example() {
>   if (true) {
>     var a = 1;
>     let b = 2;
>   }
>   console.log(a); // 1  — var leaks out of the block
>   console.log(b); // ReferenceError: b is not defined
> }
> ```
>
> ## 2. Hoisting and the Temporal Dead Zone
>
> Both are hoisted, but differently:
> - `var` is hoisted and **initialized to `undefined`**.
> - `let` is hoisted but **not initialized**. Accessing it before its declaration throws an error. The period between the start of the block and the declaration is called the *Temporal Dead Zone (TDZ)*.
>
> ```javascript
> console.log(x); // undefined
> var x = 5;
>
> console.log(y); // ReferenceError: Cannot access 'y' before initialization
> let y = 5;
> ```
>
> ## 3. Redeclaration
>
> `var` allows redeclaring the same variable in the same scope. `let` does not.
>
> ```javascript
> var name = "Alice";
> var name = "Bob";   // Fine
>
> let age = 25;
> let age = 30;       // SyntaxError: Identifier 'age' has already been declared
> ```
>
> ## 4. Global Object Property
>
> At the top level of a script, `var` creates a property on the global object (`window` in browsers). `let` does not.
>
> ```javascript
> var foo = "hello";
> let bar = "world";
>
> console.log(window.foo); // "hello"
> console.log(window.bar); // undefined
> ```
>
> ## 5. Loops and Closures (a classic gotcha)
>
> Because `var` is function-scoped, all iterations share **one** variable. `let` creates a **new binding for each iteration**.
>
> ```javascript
> for (var i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i), 100);
> }
> // Prints: 3, 3, 3
>
> for (let j = 0; j < 3; j++) {
>   setTimeout(() => console.log(j), 100);
> }
> // Prints: 0, 1, 2
> ```
>
> ## Summary Table
>
> | Feature | `var` | `let` |
> |---|---|---|
> | Scope | Function | Block |
> | Hoisting | Yes, initialized as `undefined` | Yes, but uninitialized (TDZ) |
> | Redeclare in same scope | ✅ Allowed | ❌ Error |
> | Reassign | ✅ Allowed | ✅ Allowed |
> | Creates global object property | ✅ Yes | ❌ No |
> | New binding per loop iteration | ❌ No | ✅ Yes |
>
> ## Recommendation
>
> In modern JavaScript (ES6+):
> - Use **`const`** by default, for values that won't be reassigned.
> - Use **`let`** when you need to reassign the variable.
> - **Avoid `var`**. Its scoping rules are a common source of bugs.

**Kevin** (107 words)

> Main difference: scope.
>
> - **Scope:** `var` function-scoped. `let` block-scoped (`{ }`, loops, `if`).
> - **Hoisting:** Both hoisted. `var` start as `undefined`. `let` throw `ReferenceError` if used before declaration (temporal dead zone).
> - **Redeclare:** `var x; var x;` fine. `let x; let x;` error in same scope.
> - **Global:** Top-level `var` become `window` property. `let` no.
> - **Loops:** `let` make new binding each iteration, so closures work right:
>
> ```js
> for (var i = 0; i < 3; i++) setTimeout(() => console.log(i)); // 3 3 3
> for (let i = 0; i < 3; i++) setTimeout(() => console.log(i)); // 0 1 2
> ```
>
> Use `let` (or `const`). Skip `var`.

---

## How does a bloom filter work?

**Normal** (599 words)

> # Bloom Filters
>
> A **Bloom filter** is a space-efficient, probabilistic data structure that answers one question: **"Is this element in the set?"**
>
> It can give two answers:
> - **"Definitely not"**, which is always correct
> - **"Probably yes"**, which might be wrong (a *false positive*)
>
> It never gives false negatives.
>
> ---
>
> ## The Structure
>
> A Bloom filter has two parts:
> 1. **A bit array** of size *m*, with all bits initially set to 0
> 2. **k independent hash functions**, each mapping an element to one of the *m* positions
>
> ```
> Index:  0 1 2 3 4 5 6 7 8 9
> Bits:  [0 0 0 0 0 0 0 0 0 0]
> ```
>
> ---
>
> ## Adding an Element
>
> Run the element through all *k* hash functions and set each resulting position to 1.
>
> **Example:** Add `"cat"` with 3 hash functions:
> - h1("cat") = 1
> - h2("cat") = 4
> - h3("cat") = 7
>
> ```
> Index:  0 1 2 3 4 5 6 7 8 9
> Bits:  [0 1 0 0 1 0 0 1 0 0]
> ```
>
> Now add `"dog"`, which hashes to 3, 4, 8:
>
> ```
> Index:  0 1 2 3 4 5 6 7 8 9
> Bits:  [0 1 0 1 1 0 0 1 1 0]
> ```
>
> Bit 4 was already set, and it stays 1. Elements can share bits.
>
> ---
>
> ## Checking Membership
>
> Hash the query element with the same *k* functions and check those positions:
> - **If any bit is 0**, the element is definitely not in the set.
> - **If all bits are 1**, the element is probably in the set.
>
> **Query `"fish"`** → positions 2, 4, 9
> Bit 2 is 0, so `"fish"` is **definitely not present**.
>
> **Query `"bird"`** → positions 1, 3, 8
> All are 1, so the filter says **"probably present"**. But we never added `"bird"`. Those bits were set by `"cat"` and `"dog"`. **This is a false positive.**
>
> ---
>
> ## Why No False Negatives?
>
> Bits only ever flip from 0 to 1. If you added an element, its bits were set and will stay set. So a real member will always pass the check.
>
> ---
>
> ## False Positive Rate
>
> After inserting *n* elements, the approximate false positive probability is:
>
> $$p \approx \left(1 - e^{-kn/m}\right)^k$$
>
> The optimal number of hash functions is:
>
> $$k = \frac{m}{n} \ln 2$$
>
> **Rule of thumb:** about **10 bits per element** with 7 hash functions gives roughly a **1% false positive rate**, regardless of how large the elements themselves are.
>
> ---
>
> ## Trade-offs
>
> | Pros | Cons |
> |------|------|
> | Extremely memory-efficient | False positives possible |
> | O(k) insert and lookup, constant time | Can't delete elements (in the basic version) |
> | Doesn't store the actual data | Can't list the stored elements |
> | Easy to merge (bitwise OR) | Accuracy degrades as it fills up |
>
> ---
>
> ## Real-World Uses
>
> - **Databases** (Cassandra, HBase, RocksDB, PostgreSQL): skip disk reads for keys that definitely don't exist
> - **Web browsers**: Chrome historically used one to check URLs against a malicious-site list
> - **CDNs**: Akamai uses them to avoid caching "one-hit wonder" pages
> - **Spell checkers and username availability checks**
> - **Distributed systems**: reduce network calls by checking locally first
>
> The common pattern is to use the Bloom filter as a **cheap pre-check** before an expensive operation. A false positive just costs one unnecessary lookup. A "definitely not" saves the lookup entirely.
>
> ---
>
> ## Variants
>
> - **Counting Bloom filter**: uses counters instead of bits, which allows deletion
> - **Scalable Bloom filter**: grows dynamically as elements are added
> - **Cuckoo filter**: supports deletion and often uses less space

**Kevin** (139 words)

> Bloom filter = bit array plus k hash function. Answer "maybe in set" or "definitely not in set."
>
> **Add item:** run item through all k hash. Each hash give index. Set those bits to 1.
>
> **Check item:** hash same way. Any bit 0? Definitely not there. All bits 1? Probably there, but maybe other items set those bits. That false positive.
>
> **Tradeoffs:**
> - No false negative. Ever.
> - False positive rate grow as array fill up. Bigger array or right k lower it.
> - Tiny memory. No store actual items.
> - Plain version no delete. Clearing bit could break other items. Counting Bloom filter fix that.
>
> **Math:** n items, m bits, best k ≈ (m/n)·ln 2. False positive rate ≈ (1 − e^(−kn/m))^k.
>
> **Used for:** skip disk lookups in databases (Cassandra, RocksDB), cache filtering, spell check, malicious URL check.

---

## What is a foreign key in a database?

**Normal** (317 words)

> A **foreign key** is a column (or set of columns) in one table that refers to the **primary key** of another table. It creates a link between the two tables and enforces **referential integrity**, meaning the relationship between them stays consistent.
>
> ## Example
>
> **Customers table**
> | customer_id (PK) | name |
> |---|---|
> | 1 | Alice |
> | 2 | Bob |
>
> **Orders table**
> | order_id (PK) | order_date | customer_id (FK) |
> |---|---|---|
> | 101 | 2024-01-05 | 1 |
> | 102 | 2024-01-06 | 2 |
> | 103 | 2024-01-07 | 1 |
>
> Here, `Orders.customer_id` is a foreign key that references `Customers.customer_id`. Each order is tied to an existing customer.
>
> ## SQL Example
>
> ```sql
> CREATE TABLE Customers (
>     customer_id INT PRIMARY KEY,
>     name VARCHAR(100)
> );
>
> CREATE TABLE Orders (
>     order_id INT PRIMARY KEY,
>     order_date DATE,
>     customer_id INT,
>     FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
> );
> ```
>
> ## What It Enforces
>
> - **No orphaned records:** You can't insert an order with `customer_id = 99` if no customer 99 exists.
> - **Protected deletes and updates:** By default, you can't delete a customer who still has orders. You can change this behavior with options such as:
>   - `ON DELETE CASCADE`: deleting a customer also deletes their orders.
>   - `ON DELETE SET NULL`: the order's `customer_id` becomes `NULL`.
>   - `ON DELETE RESTRICT` / `NO ACTION`: the delete is blocked (the default).
>
> ## Key Points
>
> - A foreign key usually references a primary key, but it can reference any column with a **unique** constraint.
> - A table can have **multiple** foreign keys.
> - Foreign key values can repeat (one customer, many orders), which models **one-to-many** relationships.
> - Foreign keys can be `NULL` unless declared `NOT NULL`, which allows optional relationships.
> - A table can reference itself (a **self-referencing** foreign key), e.g., an `Employees.manager_id` pointing to `Employees.employee_id`.
>
> In short, foreign keys are how relational databases connect tables and keep the connected data valid.

**Kevin** (51 words)

> Foreign key = column in one table that point to primary key in other table. Link rows together.
>
> Example: `orders.customer_id` reference `customers.id`. Each order belong to real customer.
>
> Database enforce it. No insert order for customer that not exist. No delete customer with orders unless you set cascade or similar rule.

---
