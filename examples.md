# Examples

Real captures from the benchmark. Same prompt, a default assistant (**Normal**) versus the Kevin voice. Nothing here is fabricated; Normal answers are verbatim, Kevin answers verbatim with subagent recap lines removed.

Back to the [README](README.md).

## What is a memory leak?

**Normal** (211 words)

> A memory leak is a programming bug where a program allocates memory but fails to release it after it's no longer needed. The memory stays reserved even though nothing in the program can still use it, so it's effectively wasted.
>
> Over time, repeated leaks cause the program's memory usage to grow continuously. This can slow the system down, exhaust available memory, and eventually crash the program or the whole machine.
>
> Common causes:
> - Allocating memory and losing the reference to it before freeing it (e.g., forgetting `free()`/`delete` in C/C++).
> - Holding onto references you no longer need so the garbage collector can't reclaim them (e.g., objects lingering in a long-lived collection, caches, or event listeners in Java, Python, JavaScript).
> - Circular references in systems that rely on reference counting.
> - Unclosed resources like file handles, sockets, or database connections.
>
> Even in garbage-collected languages, leaks happen — not because memory isn't freed automatically, but because the program keeps unintended references alive, so the collector considers the memory "still in use."
>
> Typical fixes: free memory explicitly when done, drop references you no longer need, use weak references for caches, close resources promptly (or use scope-based cleanup like RAII, `with`, or `try-with-resources`), and use profiling tools (Valgrind, heap profilers, etc.) to locate the source.

**Kevin** (40 words)

> Memory leak: program grabs memory, never gives back.
>
> Unused memory stays allocated. App can't reclaim it. Usage creeps up over time. Enough leaks, app slows, runs out, crashes.
>
> Common cause: lost reference. Forgot to free. Dangling cache. Listener never removed.

---

## What is the difference between authentication and authorization?

**Normal** (220 words)

> Authentication and authorization are related but distinct security concepts:
>
> **Authentication** ("authn") — verifies *who you are*. It confirms your identity by checking credentials like a password, biometric, security token, or certificate. It answers the question: "Are you really who you claim to be?"
>
> **Authorization** ("authz") — determines *what you're allowed to do*. Once your identity is established, it controls which resources, actions, or data you can access. It answers the question: "Do you have permission to do this?"
>
> **Key differences:**
>
> | Aspect | Authentication | Authorization |
> |--------|---------------|---------------|
> | Purpose | Verifies identity | Grants/denies permissions |
> | Order | Comes first | Comes after authentication |
> | Question | "Who are you?" | "What can you do?" |
> | Example | Logging in with username/password | Being allowed to edit vs. only view a file |
> | Visibility | User provides credentials directly | Happens behind the scenes |
> | Data used | Credentials (passwords, tokens, biometrics) | Policies, roles, permissions |
>
> **Analogy:** Think of an airport. Authentication is showing your passport at the gate to prove your identity. Authorization is your boarding pass determining which flight, seat, and cabin (economy vs. first class) you're permitted to access.
>
> In practice, authentication always happens before authorization — you must establish who someone is before deciding what they're permitted to do.

**Kevin** (33 words)

> Authentication = who you are. Prove identity. Password, key, fingerprint.
>
> Authorization = what you can do. Permissions. Access granted or denied.
>
> Auth first, then authz. Login proves you. Rules decide what you reach.

---

## Why would a team use a message queue?

**Normal** (318 words)

> A team uses a message queue to decouple parts of a system so they can communicate without being directly connected. Here are the main reasons:
>
> **Decoupling**
> Producers and consumers don't need to know about each other. One service drops a message; another picks it up. You can change, deploy, or replace either side independently.
>
> **Asynchronous processing**
> The producer doesn't have to wait for the work to finish. It hands off the task and moves on, which keeps user-facing requests fast (e.g., accept an order now, send the confirmation email in the background).
>
> **Load leveling / buffering**
> Queues absorb traffic spikes. If requests arrive faster than they can be processed, they pile up in the queue instead of overwhelming the downstream service. Consumers drain the backlog at their own pace.
>
> **Scalability**
> You can add more consumers to process messages in parallel. The queue distributes work across workers, making it easy to scale horizontally based on queue depth.
>
> **Reliability and durability**
> Messages persist in the queue until successfully processed. If a consumer crashes, the message isn't lost — it can be retried or redelivered. This helps survive transient failures.
>
> **Smoothing out differing speeds**
> When two systems run at different rates (a fast web tier and a slow batch processor), the queue lets each operate at its own tempo.
>
> **Retries and failure handling**
> Failed messages can be retried automatically, and persistently failing ones moved to a dead-letter queue for later inspection, rather than blocking the pipeline.
>
> **Common use cases:**
> - Background jobs (emails, image/video processing, report generation)
> - Order processing and event-driven workflows
> - Communication between microservices
> - Ingesting and buffering high-volume data or logs
> - Spreading bursty workloads over time
>
> **Trade-offs to keep in mind:** queues add operational complexity, introduce eventual consistency, make end-to-end debugging harder, and require handling concerns like message ordering and duplicate delivery. They're worth it when you need the decoupling and resilience, but they're not free.

**Kevin** (51 words)

> Decouple producer from consumer. No direct call.
>
> Buffer load spikes. Queue absorbs burst, consumer drains pace.
>
> Async work. Producer fire, move on. No wait.
>
> Resilience. Consumer down? Messages wait, no data lost.
>
> Scale consumers independent. Add workers, drain faster.
>
> Smooth retries. Fail message requeue, dead-letter catch.
>
> Fan-out. One message, many consumers.

---

## What does git rebase do?

**Normal** (277 words)

> Git rebase moves or replays a series of commits onto a new base commit. Instead of merging two branches together with a merge commit, rebasing takes the commits from your branch and reapplies them, one by one, on top of another commit — rewriting their history in the process.
>
> Common uses:
>
> - **Updating a feature branch:** `git rebase main` takes the commits unique to your branch and replays them on top of the latest `main`, so your branch looks as if you'd started it from the current tip of `main`. This gives a clean, linear history without merge commits.
>
> - **Cleaning up commits:** `git rebase -i HEAD~5` (interactive rebase) lets you reorder, edit, squash, combine, or drop the last 5 commits before sharing them.
>
> How it works under the hood:
>
> 1. Git finds the common ancestor of your branch and the target base.
> 2. It saves the diffs of each of your commits as temporary patches.
> 3. It moves your branch pointer to the new base.
> 4. It reapplies each saved commit in order. If a patch conflicts, the rebase pauses so you can resolve it, then you continue with `git rebase --continue` (or abort with `git rebase --abort`).
>
> Key points:
>
> - Rebasing **rewrites commit history** — it creates new commits with new SHA hashes, even if the changes are identical.
> - **Golden rule:** Don't rebase commits that have been pushed and that others are working on. Rewriting shared history forces everyone else to reconcile the divergence. Rebase is best for local, not-yet-shared commits.
> - Rebase vs. merge: merge preserves the exact history and adds a merge commit; rebase produces a linear, cleaner history but alters it.

**Kevin** (64 words)

> Reorders or replays commits onto new base.
> Takes your commits, sets them on top of another commit.
> Rewrites history — new commit hashes.
>
> Two main uses:
> - Move branch onto updated main. Linear history, no merge commit.
> - Clean up own commits (squash, reorder, edit, drop).
>
> Warning: rewrites history. No rebase shared/pushed branches others use — breaks their copies. Safe on local, unpushed work.

---

## What is a database index and when should I add one?

**Normal** (350 words)

> A database index is a separate data structure (usually a B-tree) that stores a sorted copy of one or more columns along with pointers back to the table rows. It lets the database find matching rows by traversing the index instead of scanning every row in the table.
>
> **The trade-off:** indexes make reads faster but writes slower (every INSERT/UPDATE/DELETE must also update the index), and they consume extra disk space.
>
> **Add an index when:**
>
> - A column is frequently used in `WHERE` clauses, `JOIN` conditions, or `ORDER BY` / `GROUP BY`.
> - The table is large enough that a full scan is noticeably slow.
> - A query filters or joins on the column often and the column has decent selectivity (many distinct values, e.g. email, user_id).
> - You enforce uniqueness (a unique index does double duty).
> - Foreign key columns — many databases don't index these automatically, and unindexed FKs slow down joins and cascading deletes.
>
> **Skip or reconsider an index when:**
>
> - The table is small (the planner will just scan it anyway).
> - The column has low cardinality (e.g. a boolean or status with two values) — an index often won't help, though partial indexes can.
> - The table is write-heavy and read-light, where the write penalty outweighs read gains.
> - You'd be adding redundant indexes (a composite index on `(a, b)` already covers queries filtering on `a` alone).
>
> **Practical tips:**
>
> - Use `EXPLAIN` / `EXPLAIN ANALYZE` to confirm a query is actually slow and that an index would be (or is) used. Measure before and after.
> - For multi-column filters, a composite index can beat several single-column ones — order the columns by how the queries use them (equality columns first, then range/sort columns).
> - Consider covering indexes (including extra columns) so the query can be answered from the index alone without touching the table.
> - Don't over-index. Add them in response to real, observed query patterns rather than speculatively on every column.
>
> In short: index the columns your slow, frequent queries filter, join, or sort on — then verify with the query planner that it helped.

**Kevin** (125 words)

> Database index: lookup shortcut for a table. Like book index — find rows by value without scanning every row. DB keeps sorted structure (usually B-tree) pointing at matching rows.
>
> Without index: full table scan, every row. With index: jump straight to matches.
>
> Add one when:
> - Column in `WHERE`, `JOIN`, or `ORDER BY` a lot.
> - Foreign keys. Almost always.
> - Table big and queries slow.
> - Column used for uniqueness (unique index).
>
> Skip when:
> - Table tiny. Scan cheap anyway.
> - Column written far more than read. Index slows every insert/update.
> - Low-cardinality column (like boolean). Index barely helps.
>
> Cost: each index takes disk, slows writes. More indexes = slower inserts. Don't index everything.
>
> Rule: index what you query, measure with `EXPLAIN`, drop unused.

---

## What is the difference between a process and a thread?

**Normal** (259 words)

> A process is an independent program in execution with its own private memory space; a thread is a unit of execution that runs inside a process. The key differences:
>
> **Memory and isolation**
> - A process has its own separate address space (code, heap, data, stack). One process cannot directly read another's memory.
> - Threads within a process share the same address space — the same heap, global variables, and open file descriptors. Each thread has its own stack and registers.
>
> **Communication**
> - Processes communicate through inter-process communication (IPC): pipes, sockets, shared memory, message queues — relatively heavyweight.
> - Threads communicate simply by reading and writing shared memory, which is fast but requires synchronization (locks, mutexes, semaphores) to avoid race conditions.
>
> **Cost and creation**
> - Processes are more expensive to create and to context-switch between (the OS must swap out the full memory map).
> - Threads are lighter; creating one and switching between threads in the same process is cheaper.
>
> **Failure isolation**
> - If a process crashes, other processes are unaffected.
> - If a thread crashes (e.g., corrupts shared memory or segfaults), it can bring down the entire process and all its threads.
>
> **Relationship**
> - A process always has at least one thread (the main thread). It can spawn many threads.
> - Threads belong to exactly one process and are scheduled by the OS for CPU time.
>
> **Quick analogy**: A process is like a house with its own walls and utilities; threads are the people living in that house, sharing the rooms and resources but each doing their own tasks.

**Kevin** (84 words)

> Process: own memory space. Heavyweight. Isolated.
> Thread: lives inside process. Shares process memory. Lightweight.
>
> Key splits:
> - Memory. Processes separate. Threads share heap/code, own only stack + registers.
> - Cost. Spawn/switch process expensive. Thread cheap.
> - Crash. One process crash no kill others. One thread crash can sink whole process.
> - Comm. Processes talk via IPC (pipes, sockets). Threads share memory direct.
> - Isolation. Process protected by OS. Threads trust each other, need locks.
>
> One process holds one-plus threads. Threads = unit OS schedules.

---

## What is a closure in JavaScript?

**Normal** (298 words)

> A closure in JavaScript is a function bundled together with references to the variables from the scope in which it was defined. Even after that outer scope has finished executing, the inner function retains access to those variables.
>
> In other words, a function "remembers" the environment where it was created, not just where it's called.
>
> ```javascript
> function makeCounter() {
>   let count = 0;          // local variable in the outer scope
>
>   return function () {     // inner function = the closure
>     count += 1;
>     return count;
>   };
> }
>
> const counter = makeCounter();
> counter(); // 1
> counter(); // 2
> counter(); // 3
> ```
>
> Here `makeCounter` has already returned, but the inner function still has live access to `count`. Each call updates and reads the same preserved variable.
>
> Key points:
>
> - **Lexical scoping**: closures work because JavaScript resolves variable names based on where functions are written in the source, not where they're invoked.
> - **Persistent state**: the captured variables live on as long as the closure does, which is how you get private, encapsulated state.
> - **Independent instances**: calling `makeCounter()` again creates a fresh `count`, so each closure has its own separate environment.
>
> Common uses:
>
> - **Data privacy / encapsulation** — hiding variables that can only be touched through the returned functions (the module pattern).
> - **Factory functions** — generating customized functions, e.g. `multiplier(2)` returning a function that doubles its input.
> - **Callbacks and event handlers** — preserving state for asynchronous code, timers, and DOM events.
>
> A classic gotcha is capturing a loop variable. Using `var` shares one binding across all iterations, while `let` creates a new binding per iteration:
>
> ```javascript
> for (let i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i), 0); // logs 0, 1, 2
> }
> // With var, this would log 3, 3, 3
> ```

**Kevin** (58 words)

> Closure: function bundled with its surrounding scope. Inner function keeps access to outer function's variables even after outer returns.
>
> ```javascript
> function counter() {
>   let count = 0;
>   return () => ++count;
> }
> const next = counter();
> next(); // 1
> next(); // 2
> ```
>
> `count` lives on. `next` remembers it. State stays private.
>
> Uses: data privacy, callbacks, factories, currying.

---

## How does HTTPS work?

**Normal** (626 words)

> HTTPS is HTTP running over an encrypted, authenticated channel (TLS). Here's how it works end to end.
>
> ## The problem it solves
>
> Plain HTTP sends data as readable text over the network. Anyone between you and the server (your ISP, someone on the same Wi-Fi, a router along the way) can read it, tamper with it, or impersonate the server. HTTPS adds three guarantees:
>
> - **Encryption** — eavesdroppers see only ciphertext.
> - **Integrity** — tampering with the data is detectable.
> - **Authentication** — you're really talking to the site you think you are.
>
> ## The building blocks
>
> - **Asymmetric (public-key) cryptography** — a key pair where the public key encrypts/verifies and the private key decrypts/signs. Slow, but solves the "how do two strangers agree on a secret" problem.
> - **Symmetric cryptography** — one shared key for both encrypt and decrypt. Fast. Used for the actual data once a shared key exists.
> - **Certificates** — a file binding a domain name to a public key, signed by a trusted Certificate Authority (CA).
>
> The trick: use slow asymmetric crypto briefly to establish a shared secret, then switch to fast symmetric crypto for the bulk traffic.
>
> ## The TLS handshake (TLS 1.3, the modern version)
>
> 1. **ClientHello** — the browser connects and says: which TLS versions and cipher suites it supports, plus its key-exchange material (an ephemeral Diffie-Hellman public key).
>
> 2. **ServerHello** — the server picks the parameters, sends its own Diffie-Hellman public key, and sends its **certificate** along with a signature proving it owns the matching private key.
>
> 3. **Key agreement** — both sides combine their own private value with the other's public value (Diffie-Hellman). They independently arrive at the same shared secret without ever sending it over the wire. An eavesdropper who saw both public keys still can't compute it.
>
> 4. **Certificate verification** — the browser checks the certificate:
>    - Is it signed by a CA the browser trusts? (Browsers/OSes ship with a list of root CAs.)
>    - Does the domain name match the site being visited?
>    - Is it unexpired and not revoked?
>    
>    If any check fails, you get the scary "Your connection is not private" warning.
>
> 5. **Finished** — both sides derive symmetric session keys from the shared secret and exchange a verification message. From here, all HTTP traffic is encrypted with those symmetric keys.
>
> TLS 1.3 does this in **one round trip** (1-RTT), and can resume prior sessions in **zero round trips** (0-RTT). The older TLS 1.2 handshake took two round trips and worked a bit differently (often RSA key transport instead of mandatory ephemeral Diffie-Hellman).
>
> ## After the handshake
>
> Normal HTTP requests and responses flow, but each is encrypted and authenticated with the session keys, typically using an AEAD cipher like **AES-GCM** or **ChaCha20-Poly1305**, which provides confidentiality and integrity together.
>
> ## A couple of important properties
>
> - **Forward secrecy** — because the Diffie-Hellman keys are ephemeral (thrown away after the session), recording today's traffic and stealing the server's private key later still won't decrypt it.
> - **Chain of trust** — your server's certificate is usually signed by an intermediate CA, which is signed by a root CA. The browser walks this chain up to a root it trusts.
> - **What HTTPS does NOT hide** — the domain/IP you're connecting to is still largely visible (DNS lookups, and the SNI field in the handshake, unless Encrypted Client Hello is used). HTTPS protects the *content*, not entirely the *fact* that you visited a site.
>
> ## The short version
>
> Browser and server use public-key crypto and Diffie-Hellman to agree on a shared secret no one else can compute, the server proves its identity with a CA-signed certificate, and then they switch to fast symmetric encryption for the actual web traffic. That's HTTP + TLS = HTTPS.

**Kevin** (131 words)

> HTTPS = HTTP + TLS encryption. Flow:
>
> 1. **TCP connect.** Browser opens connection to server, port 443.
>
> 2. **TLS handshake.**
>    - Client sends "hello": supported cipher suites, random number.
>    - Server replies: chosen cipher, its certificate (holds public key), random number.
>    - Browser verifies certificate against trusted Certificate Authorities. Confirms server owns domain. Stops if bad.
>    - Key exchange (modern: ECDHE). Both sides derive same shared session key. Eavesdropper can not.
>
> 3. **Encrypted traffic.** Session key encrypts all data with fast symmetric crypto (AES). Each request/response scrambled.
>
> Three guarantees:
> - **Confidentiality** — nobody reads data in transit.
> - **Integrity** — nobody tampers undetected.
> - **Authentication** — server proven real, not impostor.
>
> Key trick: asymmetric crypto (slow) sets up handshake and proves identity. Symmetric crypto (fast) does bulk work. Best of both.

---

## What is the difference between TCP and UDP?

**Normal** (256 words)

> TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are both transport-layer protocols, but they make very different tradeoffs.
>
> **TCP — connection-oriented, reliable**
> - Establishes a connection first (the three-way handshake: SYN, SYN-ACK, ACK).
> - Guarantees delivery: lost packets are retransmitted.
> - Guarantees order: data arrives in the sequence it was sent.
> - Includes flow control (won't overwhelm a slow receiver) and congestion control (backs off when the network is busy).
> - More overhead: larger headers (20+ bytes), acknowledgments, and connection state.
> - Use cases: web (HTTP/HTTPS), email, file transfer, SSH — anything where correctness matters more than speed.
>
> **UDP — connectionless, "fire and forget"**
> - No handshake; just sends datagrams.
> - No guarantee of delivery, ordering, or duplicate protection.
> - No flow or congestion control built in.
> - Low overhead: small 8-byte header, no connection state, low latency.
> - Use cases: live video/voice, online gaming, DNS lookups, streaming — anything where speed and low latency beat perfect reliability.
>
> **Quick comparison**
>
> | Feature | TCP | UDP |
> |---|---|---|
> | Connection | Connection-oriented | Connectionless |
> | Reliability | Guaranteed delivery | Best-effort |
> | Ordering | Ordered | Unordered |
> | Speed | Slower | Faster |
> | Header size | 20–60 bytes | 8 bytes |
> | Flow/congestion control | Yes | No |
>
> In short: TCP trades speed for reliability and ordering; UDP trades reliability for speed and low latency. Many modern protocols (like QUIC, which underlies HTTP/3) build on UDP and add their own reliability layer to get the best of both.

**Kevin** (58 words)

> TCP: connection-based. Handshake first. Reliable—acks, retransmits, ordered, no dupes. Flow + congestion control. Slower, more overhead. Use: web, email, file transfer.
>
> UDP: connectionless. Fire and forget. No acks, no order, packets can drop or arrive out of order. Tiny overhead, fast. Use: video, voice, games, DNS.
>
> Core trade: TCP buys reliability with speed. UDP buys speed with reliability.

---

## Explain Big-O notation.

**Normal** (432 words)

> Big-O notation describes how an algorithm's resource use (usually time, sometimes memory) grows as the input size grows. It's a way to talk about scalability without worrying about hardware, language, or constant factors.
>
> ## The core idea
>
> Big-O expresses an **upper bound** on growth as input size `n` approaches infinity. We drop constants and lower-order terms, because for large `n` they don't matter much:
>
> - `3n² + 5n + 100` becomes `O(n²)`
> - The `n²` term dominates; everything else is noise as `n` grows.
>
> The question it answers: *"If I double the input, what happens to the work?"*
>
> ## Common complexities (fastest to slowest growth)
>
> | Notation | Name | Doubling `n` does what? | Example |
> |---|---|---|---|
> | `O(1)` | constant | nothing | array index lookup |
> | `O(log n)` | logarithmic | adds one step | binary search |
> | `O(n)` | linear | doubles work | scanning a list |
> | `O(n log n)` | linearithmic | slightly more than doubles | merge sort, quicksort |
> | `O(n²)` | quadratic | quadruples work | nested loops over the same data |
> | `O(2ⁿ)` | exponential | squares the work | brute-force subset generation |
> | `O(n!)` | factorial | explodes | brute-force traveling salesman |
>
> ## Quick examples
>
> **O(1)** — one operation regardless of size:
> ```python
> def first(items):
>     return items[0]
> ```
>
> **O(n)** — work scales with the list length:
> ```python
> def contains(items, target):
>     for x in items:        # touches each element once
>         if x == target:
>             return True
>     return False
> ```
>
> **O(n²)** — a loop inside a loop:
> ```python
> def has_duplicate(items):
>     for i in items:        # n iterations
>         for j in items:    # n iterations each
>             ...
> ```
>
> **O(log n)** — the input is halved each step:
> ```python
> def binary_search(sorted_items, target):
>     lo, hi = 0, len(sorted_items) - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2   # discard half each time
>         ...
> ```
>
> ## Things to keep in mind
>
> - **It's about growth, not speed.** An `O(n)` algorithm can be slower than an `O(n²)` one for small inputs. Big-O matters when `n` gets large.
> - **Best/average/worst cases differ.** Quicksort is `O(n log n)` on average but `O(n²)` worst case. Big-O usually refers to the worst case unless stated otherwise.
> - **Related notation:** Big-O is an upper bound, Big-Ω (Omega) is a lower bound, and Big-Θ (Theta) is a tight bound (both at once).
> - **Space complexity** uses the same notation for memory instead of time.
>
> The practical takeaway: Big-O is a vocabulary for predicting whether an algorithm will still work when your data gets big.

**Kevin** (106 words)

> Big-O = how runtime grows as input grows. Worst-case ceiling.
>
> Common ones, slow to fast:
>
> - **O(1)** constant. Array index. Size no matter.
> - **O(log n)** logarithmic. Halve each step. Binary search.
> - **O(n)** linear. Touch each once. Loop.
> - **O(n log n)** linearithmic. Good sorts. Mergesort.
> - **O(n²)** quadratic. Nested loop. Bubble sort.
> - **O(2ⁿ)** exponential. Doubles per input. Slow. Naive recursion.
> - **O(n!)** factorial. Worst. All permutations.
>
> Rules:
>
> - Drop constants. O(2n) = O(n).
> - Drop small terms. O(n² + n) = O(n².
> - Count by input size, not exact ops.
>
> Why care: pick algorithm before data big. n=10 nobody care. n=1,000,000 O(n²) dies.

---

## What is a race condition?

**Normal** (257 words)

> A race condition is a flaw that occurs when the behavior of a program depends on the relative timing or interleaving of multiple threads, processes, or operations that access shared state concurrently. The "race" is between these operations, and the outcome changes depending on which one happens to win.
>
> The classic example is a non-atomic read-modify-write. Imagine two threads both incrementing a shared counter that starts at 0:
>
> 1. Thread A reads the value (0).
> 2. Thread B reads the value (0).
> 3. Thread A writes 0 + 1 = 1.
> 4. Thread B writes 0 + 1 = 1.
>
> The counter ends at 1 instead of 2, because both threads read before either wrote. The result depends on timing.
>
> Key characteristics:
> - Requires concurrency (multiple threads/processes/async tasks) or interrupts.
> - Involves shared, mutable state.
> - At least one access is a write.
> - The accesses are not properly synchronized.
>
> Common types:
> - Read-modify-write races (like the counter above).
> - Check-then-act races, also called TOCTOU (time-of-check to time-of-use), e.g. checking a file exists, then opening it, when it could be deleted in between. These are also a frequent source of security vulnerabilities.
>
> Why they're nasty: race conditions are often nondeterministic and timing-dependent, so they may appear rarely, vanish under a debugger, and be very hard to reproduce.
>
> Common fixes:
> - Mutual exclusion: locks, mutexes, or semaphores to serialize access.
> - Atomic operations: hardware/library primitives that do read-modify-write indivisibly.
> - Avoiding shared mutable state: immutability, message passing, or thread-local data.
> - Higher-level constructs: transactions, channels, or compare-and-swap loops.

**Kevin** (48 words)

> Two threads touch same data same time. Order not guaranteed. Result changes run to run. Bug from timing, not logic.
>
> Classic: read-modify-write. Thread A reads X=5. Thread B reads X=5. Both add 1. Both write 6. Should be 7. One lost.
>
> Fix: serialize access. Locks, mutexes, atomics, channels.

---

## How does garbage collection work?

**Normal** (442 words)

> Garbage collection (GC) is automatic memory management: the runtime reclaims memory occupied by objects that the program can no longer reach, so you don't have to free memory manually.
>
> ## The core idea: reachability
>
> An object is "live" if it can be reached by following references starting from a set of **roots** (local variables on the stack, global/static variables, CPU registers, active function frames). Anything not reachable from a root is garbage and can be collected.
>
> ## Major algorithms
>
> **Reference counting**
> - Each object tracks how many references point to it. When the count hits zero, it's freed immediately.
> - Simple and prompt, but can't reclaim **reference cycles** (A points to B, B points to A, nothing else points to either) without extra machinery. Used by CPython (plus a cycle detector) and Swift (ARC).
>
> **Tracing GC** (the more common meaning of "GC")
> - **Mark-and-sweep**: Starting from roots, traverse and *mark* every reachable object. Then *sweep* the heap, freeing anything unmarked. Can leave fragmentation.
> - **Mark-compact**: Like mark-sweep, but after marking it slides live objects together to eliminate fragmentation (at the cost of updating references).
> - **Copying / semispace**: Divide the heap in two halves. Allocate in one; when full, copy live objects to the other half and discard the rest wholesale. Fast allocation and no fragmentation, but uses 2x memory.
>
> ## Generational GC
>
> Based on the **weak generational hypothesis**: most objects die young. The heap is split into generations:
> - New objects go in the **young generation**, collected frequently and cheaply (minor GC).
> - Objects that survive several collections get **promoted** to the **old generation**, collected rarely (major/full GC).
>
> This concentrates effort where most garbage is, which is why JVM (G1, ZGC), .NET, and V8 all use generational collectors.
>
> ## Practical concerns
>
> - **Stop-the-world pauses**: Naively, the program must pause while the GC runs. Modern collectors reduce this with **concurrent** (GC runs alongside the app) and **incremental** (work split into small chunks) techniques.
> - **Write barriers**: Small bits of bookkeeping code on pointer writes, needed so generational/concurrent collectors know when an old object starts referencing a young one.
> - **Throughput vs. latency tradeoff**: You can tune for total work done (throughput) or for short, predictable pauses (latency), but rarely maximize both.
>
> ## Quick comparison vs. manual management
>
> GC trades some runtime overhead and less predictable timing for safety: it eliminates whole classes of bugs like use-after-free, double-free, and many memory leaks. Languages like Rust take a different route entirely, using compile-time ownership rules instead of a runtime collector.
>
> If you tell me a specific language or runtime (JVM, Go, Python, V8, .NET), I can go into how its collector works in detail.

**Kevin** (138 words)

> Garbage collection auto-frees memory program no longer uses. No manual free.
>
> Core idea: find live objects, reclaim rest.
>
> **Reachability**
> Start from roots: stack vars, globals, registers.
> Follow pointers. Anything reached = live.
> Anything not reached = garbage. Collect it.
>
> **Main strategies**
>
> Mark-and-sweep.
> Mark: walk from roots, flag live objects.
> Sweep: scan heap, free unmarked.
> Downside: pauses, fragmentation.
>
> Reference counting.
> Each object counts refs to it.
> Count hits zero, free now.
> Downside: misses cycles. A points B, B points A, both dead, both leak.
>
> Copying / generational.
> Most objects die young.
> Split heap young/old gens.
> Collect young often, old rarely.
> Survivors get promoted. Copying compacts, kills fragmentation.
>
> **Cost**
> Tradeoff: throughput vs pause time.
> Stop-the-world freezes app to collect.
> Concurrent/incremental GC spreads work, smaller pauses.
>
> Examples: Java (G1, ZGC), Go (concurrent mark-sweep), Python (refcount + cycle detector), JS (generational mark-sweep).

---

## What is dependency injection?

**Normal** (334 words)

> Dependency injection is a design pattern in which an object or function receives the other objects or values it depends on (its "dependencies") from an external source, rather than creating them itself.
>
> **The core idea**
>
> Instead of a component constructing what it needs internally:
>
> ```js
> class OrderService {
>   constructor() {
>     this.db = new PostgresDatabase(); // hard-wired dependency
>   }
> }
> ```
>
> You pass the dependency in from outside:
>
> ```js
> class OrderService {
>   constructor(database) {
>     this.db = database; // injected
>   }
> }
>
> const service = new OrderService(new PostgresDatabase());
> ```
>
> The component declares *what* it needs but not *how* to build it. Some external code (a caller, a factory, or a framework's "container") is responsible for creating and supplying it.
>
> **Why it's useful**
>
> - **Testability** — you can inject a fake or mock database in tests instead of hitting a real one.
> - **Decoupling** — the component depends on an abstraction (an interface) rather than a concrete implementation, so you can swap implementations without changing the component.
> - **Flexibility / configuration** — different environments can wire up different dependencies (e.g., in-memory store for dev, real store for prod).
> - **Single responsibility** — components focus on their own logic, not on constructing and wiring their collaborators.
>
> **Common forms of injection**
>
> - **Constructor injection** — dependencies passed in via the constructor (most common, makes dependencies explicit and required).
> - **Setter/property injection** — dependencies set through a setter method or property after construction.
> - **Method injection** — a dependency passed directly into the method that uses it.
>
> **Relationship to other concepts**
>
> Dependency injection is one way to achieve *Inversion of Control* (IoC) — the broader principle that a component shouldn't control the creation of its own dependencies. Many frameworks (Spring in Java, Angular, ASP.NET Core, NestJS) provide a "DI container" that automatically resolves and injects dependencies based on declared types or configuration.
>
> In short: **don't have your objects make their own dependencies — hand the dependencies to them.** This keeps code loosely coupled, easier to test, and easier to reconfigure.

**Kevin** (103 words)

> Dependency injection: pass object dependencies in from outside, not built inside.
>
> Instead of class making own collaborators, you hand them over — constructor, setter, or method.
>
> ```
> // without DI
> class Car {
>   constructor() { this.engine = new GasEngine(); }
> }
>
> // with DI
> class Car {
>   constructor(engine) { this.engine = engine; }
> }
> ```
>
> Why good:
> - Swap implementations. Real engine, fake engine for tests.
> - Loose coupling. Car no care which engine.
> - Test easy. Inject mock.
>
> Three flavors: constructor injection, setter injection, interface injection. Constructor most common.
>
> "Injection" word scary. Just means: give thing its stuff, don't make it forage.

---

## What is the difference between SQL and NoSQL databases?

**Normal** (289 words)

> SQL and NoSQL databases differ in several fundamental ways:
>
> ## Data Model
>
> **SQL (Relational)**
> - Data stored in tables with rows and columns
> - Predefined, rigid schema — you define structure before inserting data
> - Relationships modeled with foreign keys and joins
>
> **NoSQL (Non-relational)**
> - Various models: document (JSON-like), key-value, column-family, graph
> - Flexible or dynamic schema — structure can vary between records
> - Relationships often handled by embedding or denormalization
>
> ## Schema
>
> - **SQL:** Schema-on-write. Changing it requires migrations and can be cumbersome.
> - **NoSQL:** Schema-on-read (often schemaless). Easy to evolve as needs change.
>
> ## Scaling
>
> - **SQL:** Traditionally scales **vertically** (bigger server). Horizontal scaling is possible but harder.
> - **NoSQL:** Designed to scale **horizontally** (add more commodity servers/shards) more easily.
>
> ## Consistency & Transactions
>
> - **SQL:** Strong **ACID** guarantees (Atomicity, Consistency, Isolation, Durability). Great for data integrity.
> - **NoSQL:** Often favors **BASE** (Basically Available, Soft state, Eventual consistency) and the AP/CP tradeoffs of the CAP theorem, though many modern NoSQL databases now offer ACID support.
>
> ## Query Language
>
> - **SQL:** Standardized SQL across most engines.
> - **NoSQL:** Database-specific APIs and query languages (e.g., MongoDB query syntax, Cassandra's CQL).
>
> ## Examples
>
> - **SQL:** PostgreSQL, MySQL, Oracle, SQL Server, SQLite
> - **NoSQL:** MongoDB (document), Redis (key-value), Cassandra (column-family), Neo4j (graph)
>
> ## When to Use Which
>
> **Choose SQL when:**
> - Data is highly structured with clear relationships
> - You need strong consistency and complex queries/joins
> - Transactional integrity matters (e.g., financial systems)
>
> **Choose NoSQL when:**
> - Data is unstructured, semi-structured, or rapidly evolving
> - You need massive horizontal scale and high write throughput
> - Flexibility and speed of development outweigh strict consistency
>
> In practice, many systems use both (**polyglot persistence**), picking the right tool for each part of the workload.

**Kevin** (58 words)

> SQL: relational. Fixed schema, tables, rows. Vertical scale. Strong consistency (ACID). Good for structured data, complex joins, transactions. Postgres, MySQL.
>
> NoSQL: non-relational. Flexible schema. Horizontal scale. Often eventual consistency. Good for big volume, fast writes, unstructured data. Types: document (Mongo), key-value (Redis), column (Cassandra), graph (Neo4j).
>
> Pick SQL: relations, transactions, fixed shape.
> Pick NoSQL: scale, speed, loose shape.

---

## What is a Docker container?

**Normal** (222 words)

> A Docker container is a lightweight, standalone, executable package that bundles an application together with everything it needs to run—code, runtime, system libraries, and settings—so it behaves consistently across different environments.
>
> Key points:
>
> - **Based on images**: A container is a running instance of a Docker *image*, which is a read-only template. You can start many containers from the same image.
>
> - **Process isolation**: Containers isolate applications from each other and from the host using Linux kernel features like namespaces (isolated process, network, and filesystem views) and cgroups (resource limits on CPU, memory, etc.).
>
> - **Shares the host kernel**: Unlike a virtual machine, a container does not include a full guest operating system. It shares the host's OS kernel, which makes containers much smaller, faster to start (seconds or less), and less resource-intensive than VMs.
>
> - **Ephemeral by default**: Containers are typically disposable. When one stops, changes to its writable layer are lost unless you persist data using volumes or bind mounts.
>
> - **Portable**: Because the image carries all dependencies, the same container runs the same way on a developer laptop, a test server, or cloud infrastructure—solving the classic "it works on my machine" problem.
>
> In short, a Docker container is a running, isolated, portable instance of an application packaged with its dependencies, sharing the host OS kernel rather than virtualizing hardware.

**Kevin** (50 words)

> Software box. Bundles app plus all need run — code, libraries, configs, deps.
>
> Runs isolated on shared OS kernel. Lighter than VM, no full guest OS.
>
> Built from image. Same image runs same everywhere — laptop, server, cloud. Kills "works on my machine".
>
> Start fast, stop fast, throw away cheap.

---

## What is a hash function?

**Normal** (250 words)

> A hash function is a function that takes an input of arbitrary size (a "message," file, or any data) and deterministically produces a fixed-size output, usually called a hash, digest, or hash value.
>
> Key properties:
>
> - **Deterministic**: The same input always produces the same output.
> - **Fixed-size output**: A 3-byte input and a 3-gigabyte input both yield a digest of the same length (e.g., 256 bits for SHA-256).
> - **Fast to compute**: Producing the hash for any input is efficient.
>
> Common uses:
>
> - **Hash tables**: Mapping keys to bucket indices for fast lookup, insertion, and deletion (average O(1)).
> - **Integrity checks**: Detecting whether data has changed (checksums).
> - **Deduplication and caching**: Quickly comparing large items by comparing their hashes.
>
> Cryptographic hash functions (e.g., SHA-256, BLAKE3) add stronger guarantees:
>
> - **Preimage resistance**: Given a hash, it's infeasible to find an input that produces it.
> - **Second-preimage resistance**: Given an input, it's infeasible to find a different input with the same hash.
> - **Collision resistance**: It's infeasible to find any two distinct inputs that hash to the same value.
> - **Avalanche effect**: A tiny change in input drastically changes the output.
>
> These are used for password storage (with salting), digital signatures, blockchains, and verifying file authenticity.
>
> A note on **collisions**: Since inputs are unlimited but outputs are fixed-size, multiple inputs must eventually map to the same hash (pigeonhole principle). Good hash functions distribute outputs evenly to minimize collisions, and non-cryptographic hash table implementations handle them via techniques like chaining or open addressing.

**Kevin** (56 words)

> Function mapping any input to fixed-size output. Same input, same output. Tiny input change, big output change.
>
> Key traits:
> - One-way. Easy forward, hard reverse.
> - Deterministic. Same in, same out.
> - Fixed size out. Any size in.
> - Collision-resistant. Two inputs rare share output.
>
> Uses: hash tables, checksums, passwords, crypto, dedup.
> Examples: SHA-256, MD5, bcrypt.

---

## How does DNS resolution work?

**Normal** (453 words)

> DNS (Domain Name System) resolution is the process of translating a human-readable domain name (like `example.com`) into a machine-usable IP address (like `93.184.216.34`). Here's how it works step by step:
>
> ## The Key Players
>
> - **DNS resolver** (recursive resolver): Usually run by your ISP or a service like Cloudflare (1.1.1.1) or Google (8.8.8.8). It does the legwork of finding the answer.
> - **Root nameservers**: The top of the hierarchy. There are 13 logical root server addresses worldwide.
> - **TLD nameservers**: Handle top-level domains like `.com`, `.org`, `.net`.
> - **Authoritative nameservers**: Hold the actual DNS records for a specific domain.
>
> ## The Resolution Flow
>
> When you type `www.example.com` into your browser:
>
> 1. **Browser/OS cache check**: The system first checks local caches (browser cache, OS cache, `hosts` file). If the answer is there and not expired, it's used immediately.
>
> 2. **Query the recursive resolver**: If not cached, your computer asks its configured DNS resolver.
>
> 3. **Resolver checks its cache**: If the resolver recently looked this up, it returns the cached answer.
>
> 4. **Ask a root nameserver**: If uncached, the resolver asks a root server. The root doesn't know the IP, but it knows where the `.com` TLD servers are and replies with a referral.
>
> 5. **Ask the TLD nameserver**: The resolver asks the `.com` TLD server, which replies with the authoritative nameservers for `example.com`.
>
> 6. **Ask the authoritative nameserver**: The resolver asks `example.com`'s authoritative server, which returns the actual IP address (the A or AAAA record).
>
> 7. **Return and cache**: The resolver hands the IP back to your computer and caches it for future use (per the record's TTL). Your browser then connects to that IP.
>
> ## Recursive vs. Iterative
>
> - The query from your device **to the resolver** is **recursive** — "give me the final answer."
> - The queries from the resolver **to the root/TLD/authoritative servers** are typically **iterative** — each server gives a referral to the next, and the resolver follows the chain.
>
> ## Caching and TTL
>
> Every DNS record has a **TTL (Time To Live)** that controls how long it can be cached. Caching happens at multiple layers (browser, OS, resolver), which dramatically reduces lookups and speeds up the web — most queries never reach the authoritative server.
>
> ## Common Record Types
>
> - **A** — maps a name to an IPv4 address
> - **AAAA** — maps a name to an IPv6 address
> - **CNAME** — alias pointing one name to another name
> - **MX** — mail server for the domain
> - **NS** — nameservers for the domain
> - **TXT** — arbitrary text (used for SPF, DKIM, verification, etc.)
>
> The whole process usually completes in a few milliseconds to a few hundred milliseconds, and thanks to caching, the full chain only runs occasionally.

**Kevin** (88 words)

> Client checks cache first. Browser, OS cache. Hit means done.
>
> Miss goes to resolver. Usually your ISP or 8.8.8.8.
>
> Resolver walks hierarchy if no cache:
> - Root server: knows where .com lives.
> - TLD server: knows where example.com lives.
> - Authoritative server: holds real IP for www.example.com.
>
> Resolver caches answer per TTL. Returns IP to client.
>
> Client opens connection to IP. Done.
>
> Recursive vs iterative: resolver does iterative legwork, client gets one recursive answer.
>
> UDP port 53 mostly. TCP for big answers. DNSSEC signs records. DoH/DoT encrypt query.

---

## What is eventual consistency?

**Normal** (274 words)

> Eventual consistency is a consistency model used in distributed systems that guarantees that, if no new updates are made to a given piece of data, all replicas (copies of that data across different nodes) will *eventually* converge to the same value.
>
> Key characteristics:
>
> - **Weak guarantee on timing**: It promises convergence will happen, but makes no promise about *when*. During the window before convergence, different replicas may temporarily return different (stale) values for the same read.
> - **High availability**: By not requiring all replicas to agree before responding, the system can keep serving reads and writes even during network partitions or node failures. This makes it a common choice for systems prioritizing availability and partition tolerance.
> - **CAP theorem context**: In CAP terms (Consistency, Availability, Partition tolerance), eventual consistency favors **A** and **P**, relaxing the strong **C**. It is often associated with the "AP" side and with the BASE philosophy (Basically Available, Soft state, Eventual consistency) as opposed to ACID.
>
> **Example**: When you update your profile picture on a large social network, some friends might see the new picture immediately while others still see the old one for a few seconds or minutes. Eventually, every server holding a copy reflects the new picture.
>
> **How convergence is achieved**: Systems use techniques like anti-entropy protocols, gossip protocols, read-repair, vector clocks, and conflict resolution strategies (e.g., last-write-wins or CRDTs) to reconcile divergent replicas.
>
> **Common in**: Amazon DynamoDB, Apache Cassandra, Riak, DNS, and many CDN/caching systems.
>
> **Trade-off**: You gain availability and low latency at the cost of potentially reading stale data. Stronger models (strong consistency, linearizability) avoid stale reads but require more coordination, reducing availability and increasing latency.

**Kevin** (45 words)

> Eventual consistency. Distributed data model.
>
> Replicas can disagree short-term. No new writes, all converge same value eventually.
>
> Tradeoff: reads may return stale data. Gain: high availability, low latency, partition tolerance.
>
> Versus strong consistency: every read sees newest write, costs coordination.
>
> Examples: DNS, Cassandra, DynamoDB, S3.

---

## What is the difference between the stack and the heap?

**Normal** (362 words)

> The stack and the heap are two regions of memory a program uses at runtime, with different management strategies and trade-offs.
>
> ## The Stack
>
> - **Structure:** A LIFO (last-in, first-out) data structure. Memory is added and removed in a strict order.
> - **What lives there:** Local variables, function parameters, return addresses, and bookkeeping for function calls (call frames).
> - **Allocation:** Automatic. When a function is called, a frame is pushed; when it returns, the frame is popped. Just moving a stack pointer.
> - **Speed:** Very fast — allocation/deallocation is a single pointer adjustment.
> - **Size:** Small and fixed-ish (often 1–8 MB per thread). Overflowing it causes a *stack overflow* (e.g., deep/infinite recursion).
> - **Lifetime:** Tied to scope. Data vanishes automatically when the function returns.
> - **Layout:** Contiguous and well-ordered; good cache locality.
>
> ## The Heap
>
> - **Structure:** A large, unstructured pool of memory.
> - **What lives there:** Data whose size isn't known at compile time or that must outlive the function that created it (dynamically allocated objects).
> - **Allocation:** Manual or managed. You request memory explicitly (`malloc`/`new`) and must free it (`free`/`delete`), or a garbage collector handles it.
> - **Speed:** Slower — the allocator must search for a suitable free block and track allocations.
> - **Size:** Large, limited mainly by available system memory.
> - **Lifetime:** Lasts until explicitly freed (or garbage-collected). Independent of function scope.
> - **Layout:** Can become fragmented over time; worse cache locality.
>
> ## Key Differences at a Glance
>
> | Aspect | Stack | Heap |
> |---|---|---|
> | Management | Automatic | Manual / GC |
> | Speed | Fast | Slower |
> | Size | Small, limited | Large |
> | Lifetime | Scope-bound | Until freed |
> | Access pattern | LIFO | Random |
> | Fragmentation | None | Possible |
>
> ## Common Pitfalls
>
> - **Stack:** Returning a pointer/reference to a local variable (it's gone after return); stack overflow from deep recursion.
> - **Heap:** Memory leaks (forgetting to free), dangling pointers (using freed memory), double-free errors.
>
> **Rule of thumb:** Use the stack for small, short-lived, fixed-size data; use the heap for large data, data of unknown size, or data that must persist beyond a single function call.

**Kevin** (80 words)

> Stack: ordered memory. Fast. Auto-managed. Holds local vars, call frames, return addresses. Grows/shrinks as functions push and pop. Size known at compile time. Limited, small. Overflow if deep recursion.
>
> Heap: free-form pool. Manual or GC-managed. Holds dynamic data, lives past function scope. Slower, fragmentable. Big. You allocate, you free (or leak).
>
> Key diffs:
> - Stack auto, heap manual.
> - Stack fast, heap slow.
> - Stack fixed-size per frame, heap dynamic.
> - Stack lifetime tied to scope, heap lives till freed.

---

## What is idempotency in an API?

**Normal** (343 words)

> Idempotency in an API means that making the same request multiple times produces the same result as making it once. The operation has no additional side effects beyond the first successful application, no matter how many times it's repeated.
>
> **Why it matters:** Networks are unreliable. A client might send a request, never get a response (timeout, dropped connection), and retry. Without idempotency, that retry could create a duplicate order, charge a card twice, or double-post a comment. Idempotency makes retries safe.
>
> **HTTP methods and idempotency**
>
> By the HTTP spec, these methods are expected to be idempotent:
>
> - `GET` — reads data, changes nothing.
> - `PUT` — replaces a resource with a given state. Sending it twice leaves the same state.
> - `DELETE` — deleting an already-deleted resource leaves it deleted (the resource is gone either way).
> - `HEAD`, `OPTIONS` — safe/read-only.
>
> And the notable non-idempotent one:
>
> - `POST` — typically creates a new resource each time, so two calls create two resources.
>
> **Idempotency vs. safety**
>
> These are related but distinct:
> - *Safe* = no side effects at all (GET, HEAD).
> - *Idempotent* = side effects, but repeating doesn't add more (PUT, DELETE).
> - All safe methods are idempotent, but not vice versa.
>
> **Making non-idempotent operations idempotent**
>
> For operations like payments, a common pattern is an **idempotency key**: the client generates a unique key (often a UUID) and sends it with the request, usually in a header like `Idempotency-Key`. The server records the key with the result. If a request arrives with a key it has already seen, the server returns the stored result instead of performing the operation again.
>
> ```
> POST /charges
> Idempotency-Key: 7f3a9c2e-1b4d-4e8a-9c1f-2d3e4f5a6b7c
>
> { "amount": 5000, "currency": "usd" }
> ```
>
> Stripe, for example, uses exactly this approach so a retried charge never bills the customer twice.
>
> **Caveats**
>
> - Idempotency is about the *observable result*, not necessarily identical responses. A repeated DELETE might return `204` the first time and `404` after, yet the end state is the same.
> - Server implementations must actually honor these guarantees; the HTTP spec describes expectations, not enforcement.

**Kevin** (44 words)

> Idempotency: same request, called many times, same result. No extra effect past first.
>
> PUT, DELETE, GET idempotent. POST not.
>
> Example: charge card once. Retry on timeout must not double-charge. Idempotency key makes server dedupe.
>
> Why care: networks flaky. Clients retry. Idempotency makes retries safe.

---

## How does OAuth work?

**Normal** (564 words)

> OAuth (specifically OAuth 2.0, the current standard) is a protocol for **delegated authorization**. It lets you grant one application limited access to your data on another service, without sharing your password.
>
> ## The core problem it solves
>
> Say a photo-printing app wants to access your Google Photos. Without OAuth, you'd have to give the app your Google password — which is dangerous (it gets full access, forever, and could leak your credentials). OAuth lets you grant *just* "read my photos" access, revocable at any time, without the app ever seeing your password.
>
> ## The key players
>
> - **Resource Owner** — you, the user who owns the data.
> - **Client** — the app requesting access (the photo printer).
> - **Authorization Server** — issues tokens after authenticating you (e.g., Google's login/consent system).
> - **Resource Server** — holds the protected data and accepts tokens (e.g., the Google Photos API).
>
> ## The typical flow (Authorization Code Grant)
>
> This is the most common and secure flow for web/mobile apps:
>
> 1. **Redirect to authorize** — The client sends you to the authorization server with its `client_id`, the requested `scope` (e.g. `photos.read`), a `redirect_uri`, and a `state` value (anti-CSRF).
>
> 2. **You authenticate and consent** — You log in to the service directly (the client never sees this) and approve the requested permissions.
>
> 3. **Authorization code returned** — The auth server redirects back to the client's `redirect_uri` with a short-lived, one-time **authorization code**.
>
> 4. **Code exchanged for tokens** — The client's backend sends the code *plus* its `client_secret` directly to the auth server's token endpoint (a server-to-server call, not via the browser). It receives:
>    - an **access token** (used to call the API, usually short-lived),
>    - often a **refresh token** (used to get new access tokens without re-prompting you).
>
> 5. **Access the resource** — The client calls the resource server's API, passing the access token (typically `Authorization: Bearer <token>`). The resource server validates it and returns the data.
>
> 6. **Refresh as needed** — When the access token expires, the client uses the refresh token to silently obtain a new one.
>
> ## Why the two-step (code → token) dance?
>
> The authorization code travels through the browser (visible in redirects), but it's useless on its own — exchanging it for a token requires the `client_secret`, which stays on the server. This keeps the actual access token out of the browser/URL history.
>
> ## PKCE (important addition)
>
> For mobile and single-page apps that can't safely store a `client_secret`, **PKCE** (Proof Key for Code Exchange) is used. The client generates a random `code_verifier`, sends a hashed version (`code_challenge`) in the initial request, then proves it owns the verifier when exchanging the code. This prevents an attacker who intercepts the code from using it. PKCE is now recommended for *all* clients.
>
> ## Other grant types
>
> - **Client Credentials** — machine-to-machine, no user involved (the app accesses its own resources).
> - **Device Code** — for devices with limited input (smart TVs); you authorize on your phone using a displayed code.
> - **Implicit** and **Resource Owner Password** — older flows, now discouraged for security reasons.
>
> ## One key clarification
>
> OAuth 2.0 is about **authorization** (what an app may do), not **authentication** (proving who you are). **OpenID Connect (OIDC)** is a thin layer built on top of OAuth 2.0 that adds proper authentication, returning an **ID token** (a JWT) describing the user. "Log in with Google" uses OIDC, not raw OAuth.

**Kevin** (106 words)

> OAuth = let app act for you without your password.
>
> Flow (Authorization Code):
>
> 1. App sends you to provider login (Google, GitHub).
> 2. You log in, approve scopes.
> 3. Provider redirects back with short-lived **code**.
> 4. App swaps code + secret server-side for **access token**.
> 5. App calls API with token. Token scoped, expires.
> 6. **Refresh token** gets new access token, no re-login.
>
> Key bits:
> - App never sees password.
> - Token limited by scope. Read-only stays read-only.
> - Code swap happens back-channel, secret stays hidden.
> - PKCE adds proof for mobile/SPA apps, no secret needed.
>
> OAuth = authorization, not authentication. OIDC layers identity on top.

---

## What is a deadlock?

**Normal** (258 words)

> A deadlock is a situation in concurrent computing where two or more processes (or threads) are each waiting for the other to release a resource, so none of them can ever proceed. They're stuck waiting forever.
>
> A classic example: Thread A holds Lock 1 and wants Lock 2, while Thread B holds Lock 2 and wants Lock 1. Neither will release what it holds until it gets the other's lock, so both wait indefinitely.
>
> Four conditions (the Coffman conditions) must all hold for a deadlock to occur:
>
> 1. **Mutual exclusion** — at least one resource is held in a non-shareable mode.
> 2. **Hold and wait** — a process holds at least one resource while waiting to acquire others.
> 3. **No preemption** — resources can't be forcibly taken away; they must be released voluntarily.
> 4. **Circular wait** — a circular chain of processes exists, each waiting for a resource held by the next.
>
> Common strategies to deal with deadlocks:
>
> - **Prevention** — eliminate one of the four conditions (e.g., always acquire locks in a consistent global order to avoid circular wait).
> - **Avoidance** — use algorithms like the Banker's algorithm to only grant resources when the system stays in a safe state.
> - **Detection and recovery** — let deadlocks happen, detect them (e.g., via a wait-for graph), then recover by killing or rolling back a process.
> - **Timeouts** — give up and retry after waiting too long.
>
> Deadlocks appear not just with locks but also in databases (transactions waiting on each other's row locks), distributed systems, and message-passing systems.

**Kevin** (68 words)

> Deadlock: two+ threads stuck forever, each holding a lock the other needs.
>
> Example: A holds lock1, wants lock2. B holds lock2, wants lock1. Neither lets go. Both wait forever.
>
> Four conditions needed (Coffman):
> - Mutual exclusion. Resource held by one.
> - Hold and wait. Hold one, want more.
> - No preemption. Cannot force release.
> - Circular wait. A waits B, B waits A.
>
> Break any one, no deadlock.

---

## Explain the CAP theorem.

**Normal** (415 words)

> The CAP theorem (also called Brewer's theorem) is a fundamental principle in distributed systems. It states that a distributed data store can provide at most **two** of the following three guarantees simultaneously:
>
> ## The Three Properties
>
> **Consistency (C)**
> Every read receives the most recent write or an error. All nodes see the same data at the same time — there's a single, up-to-date view of the data.
>
> **Availability (A)**
> Every request receives a (non-error) response, without the guarantee that it contains the most recent write. The system always responds, even if the data might be stale.
>
> **Partition Tolerance (P)**
> The system continues to operate despite network partitions — that is, messages being dropped or delayed between nodes. The cluster keeps working even when nodes can't all communicate.
>
> ## The Core Trade-off
>
> The key insight: **network partitions are unavoidable** in any real distributed system (networks fail, packets drop, nodes go offline). So partition tolerance (P) isn't really optional — you must design for it.
>
> This means the *real* choice happens **during a partition**: when nodes can't communicate, you must choose between consistency and availability.
>
> - **CP (Consistency + Partition tolerance):** When a partition occurs, the system refuses to respond (or returns errors) to avoid serving stale/inconsistent data. It sacrifices availability to stay correct.
> - **AP (Availability + Partition tolerance):** When a partition occurs, the system keeps responding from each node, even if some nodes have stale data. It sacrifices consistency to stay available.
> - **CA (Consistency + Availability):** Only achievable if there are no partitions — i.e., a single node or a non-distributed system. Not realistic for true distributed systems.
>
> ## Examples
>
> - **CP systems:** HBase, MongoDB (in default config), traditional RDBMS with synchronous replication, ZooKeeper, etcd.
> - **AP systems:** Cassandra, DynamoDB, CouchDB, Riak — these favor staying online and reconcile data later.
>
> ## Important Nuances
>
> 1. **It's not all-or-nothing.** The trade-off only manifests *during* a partition. When the network is healthy, a system can offer both strong consistency and high availability.
>
> 2. **It's a spectrum, not binary.** Real systems often offer tunable consistency (e.g., Cassandra's quorum settings let you lean toward C or A per-query).
>
> 3. **PACELC extends CAP.** It adds: *if there's a Partition, choose between Availability and Consistency; Else (normal operation), choose between Latency and Consistency.* This captures the latency-vs-consistency trade-off that CAP ignores.
>
> In short: in a distributed system, you can't escape network partitions, so you're really deciding whether to prioritize staying correct (CP) or staying responsive (AP) when things go wrong.

**Kevin** (106 words)

> CAP theorem. Distributed system, pick two of three:
>
> - **Consistency** — every read sees latest write. All nodes agree.
> - **Availability** — every request gets response. No errors.
> - **Partition tolerance** — system survives dropped/delayed messages between nodes.
>
> Network partitions happen. Not optional. So real pick: when partition hits, choose C or A.
>
> - **CP** — refuse requests to stay consistent. (HBase, Zookeeper, etcd.)
> - **AP** — answer anyway, risk stale data. (Cassandra, DynamoDB.)
>
> No partition? Get both C and A.
>
> "Two of three" framing loose. Real tradeoff lives during partitions. See PACELC for fuller picture: partition → C or A; else → latency or consistency.

---

## What does a load balancer do?

**Normal** (136 words)

> A load balancer distributes incoming network traffic across multiple backend servers so no single server gets overwhelmed.
>
> Key functions:
>
> - **Traffic distribution**: Spreads requests across a pool of servers using algorithms like round-robin, least-connections, or weighted distribution.
> - **High availability**: Detects unhealthy servers via health checks and stops routing traffic to them, rerouting to healthy ones.
> - **Scalability**: Lets you add or remove servers behind it without disrupting clients, handling traffic spikes by spreading load.
> - **Performance**: Reduces latency and prevents any one server from becoming a bottleneck.
>
> Common types:
>
> - **Layer 4 (transport)**: Routes based on IP address and TCP/UDP ports, without inspecting content.
> - **Layer 7 (application)**: Routes based on HTTP content like URLs, headers, or cookies, enabling smarter routing decisions.
>
> Additional features often included: SSL/TLS termination, session persistence (sticky sessions), and DDoS mitigation.

**Kevin** (14 words)

> Spreads traffic across many servers.
> Picks server per request. Health checks. Drops dead ones.

---

## What is the difference between a cache and a database?

**Normal** (340 words)

> A cache and a database are both used to store data, but they serve different purposes and have different characteristics.
>
> **Database**
> - Primary, authoritative store for your data — the "source of truth"
> - Designed for durability and persistence; data survives restarts and crashes
> - Optimized for reliable, consistent storage and complex queries (joins, transactions, aggregations)
> - Typically larger capacity, stored on disk (though many cache in memory too)
> - Slower access relative to a cache, but guarantees correctness and integrity (ACID properties in many cases)
> - Examples: PostgreSQL, MySQL, MongoDB
>
> **Cache**
> - A temporary, fast-access layer that stores a *copy* of frequently accessed data
> - Designed for speed; usually kept in memory (RAM) for very low latency
> - Not the source of truth — it can be cleared or lost without losing your real data
> - Typically smaller, holding a "hot" subset of data
> - Often uses eviction policies (e.g., LRU) and expiration (TTL) since it isn't meant to hold everything forever
> - May sacrifice strict consistency for speed (cached data can be stale)
> - Examples: Redis, Memcached
>
> **Key differences at a glance**
>
> | Aspect | Database | Cache |
> |---|---|---|
> | Role | Source of truth | Performance optimization |
> | Durability | Persistent, durable | Temporary, disposable |
> | Speed | Slower | Very fast |
> | Storage | Often disk-based | Usually in-memory |
> | Capacity | Large (all data) | Small (hot subset) |
> | Consistency | Strong/reliable | May be stale |
>
> **How they work together**
>
> A common pattern is to put a cache in front of a database. When an app needs data, it checks the cache first. On a "cache hit," it returns the fast in-memory copy. On a "cache miss," it queries the database, then stores the result in the cache for next time. This reduces load on the database and speeds up responses.
>
> In short: a **database** is where your data permanently lives, while a **cache** is a fast, temporary copy used to avoid repeatedly fetching from the slower database.

**Kevin** (97 words)

> Cache: fast temporary store. Speed over durability.
> Database: durable system of record. Persistence over speed.
>
> Key differences:
> - Persistence. DB survives restarts. Cache can vanish, often in-memory.
> - Truth. DB holds source of truth. Cache holds copy.
> - Speed. Cache faster (RAM, simple key lookup). DB slower, more work.
> - Eviction. Cache expires/evicts entries (TTL, LRU). DB keeps until deleted.
> - Queries. DB rich queries, joins, transactions. Cache mostly key-value.
> - Size. Cache small, hot subset. DB full dataset.
>
> Short: cache speeds reads of data living in database. Lose cache, rebuild from DB. Lose DB, lose data.

---

## What is a webhook?

**Normal** (293 words)

> A webhook is a way for one application to send real-time data to another application automatically when a specific event happens.
>
> Instead of one system repeatedly asking another "has anything changed yet?" (polling), a webhook flips the model: the source system pushes a notification the moment something occurs.
>
> How it works:
>
> 1. **You register a URL** — You tell the source application (e.g., GitHub, Stripe, Slack) an endpoint URL you control where it should send data.
> 2. **An event happens** — Someone pushes code, a payment succeeds, a message is posted, etc.
> 3. **The source sends an HTTP request** — Usually a `POST` to your URL, with a payload (typically JSON) describing what happened.
> 4. **Your server receives and reacts** — Your endpoint processes the data and triggers whatever logic you want.
>
> A simple analogy: polling is like checking your mailbox every five minutes to see if a package arrived. A webhook is like the delivery service texting you the instant it's dropped off.
>
> Common uses:
> - Payment processors notifying you of successful or failed charges
> - Git platforms triggering CI/CD pipelines on a push
> - Chat apps relaying incoming messages
> - Form services forwarding new submissions
>
> Key things to know:
> - **It's just an HTTP endpoint** — you need a publicly reachable URL to receive them.
> - **Security matters** — since anyone could hit your URL, providers usually sign requests (e.g., with an HMAC signature) so you can verify they're authentic.
> - **It should respond quickly** — return a `2xx` status fast and do heavy processing asynchronously; many providers retry if you don't acknowledge in time.
>
> In short: a webhook is a "reverse API" — rather than you calling a service, the service calls you when there's something worth telling you about.

**Kevin** (51 words)

> Webhook: server pings another server when event happens. Reverse of normal request — no polling.
>
> You register a URL. Source fires HTTP POST to that URL when thing occurs. Payload carries event data.
>
> Example: GitHub POSTs to your URL on push. Stripe POSTs on payment.
>
> Key: event-driven, real-time, push not pull.

---

## What is recursion?

**Normal** (225 words)

> Recursion is a technique where a function solves a problem by calling itself on a smaller version of that problem.
>
> A recursive function has two essential parts:
>
> 1. **Base case** — a condition that stops the recursion. Without it, the function would call itself forever.
> 2. **Recursive case** — where the function calls itself with a modified input that moves toward the base case.
>
> A classic example is computing a factorial (n!):
>
> ```python
> def factorial(n):
>     if n <= 1:        # base case
>         return 1
>     return n * factorial(n - 1)   # recursive case
> ```
>
> Calling `factorial(4)` expands like this:
> - `factorial(4)` = 4 × `factorial(3)`
> - = 4 × 3 × `factorial(2)`
> - = 4 × 3 × 2 × `factorial(1)`
> - = 4 × 3 × 2 × 1 = 24
>
> Each call waits for the one beneath it to finish, then the results "unwind" back up.
>
> Recursion is especially natural for problems that are self-similar — structures like trees, nested data, or divide-and-conquer algorithms (e.g., merge sort, traversing a file system, or navigating a graph). Anything you can solve with recursion can also be solved with loops, but recursion often expresses the solution more cleanly.
>
> The main trade-offs: each call consumes stack memory, so very deep recursion can cause a stack overflow, and naive recursion can repeat work (which techniques like memoization address).

**Kevin** (68 words)

> Recursion: thing defines itself by itself.
>
> Function calls itself on smaller input. Stops at base case.
>
> Example: factorial. 5! = 5 × 4!. 4! = 4 × 3!. Down to 1! = 1 (base case). Unwind back up.
>
> Two parts every time:
> - Base case. Stops recursion.
> - Recursive case. Calls self on smaller piece.
>
> No base case = infinite loop. Stack overflow.
>
> See definition? Look up "recursion."

---

## What is the difference between let and var in JavaScript?

**Normal** (422 words)

> In JavaScript, `let` and `var` are both used to declare variables, but they differ in several important ways:
>
> ## 1. Scope
>
> - **`var`** is **function-scoped**. It's accessible anywhere within the function it's declared in (or globally if declared outside a function).
> - **`let`** is **block-scoped**. It only exists within the nearest enclosing block (`{ }`), such as an `if`, `for`, or standalone block.
>
> ```javascript
> function example() {
>   if (true) {
>     var a = 1;
>     let b = 2;
>   }
>   console.log(a); // 1  (var leaks out of the block)
>   console.log(b); // ReferenceError (let is confined to the block)
> }
> ```
>
> ## 2. Hoisting
>
> - Both are hoisted to the top of their scope, but **`var`** is initialized as `undefined`, so you can reference it before its declaration (you just get `undefined`).
> - **`let`** is hoisted but **not initialized**. Accessing it before the declaration throws a `ReferenceError`. The period between the start of the scope and the declaration is called the **Temporal Dead Zone (TDZ)**.
>
> ```javascript
> console.log(x); // undefined
> var x = 5;
>
> console.log(y); // ReferenceError (TDZ)
> let y = 5;
> ```
>
> ## 3. Redeclaration
>
> - **`var`** allows redeclaring the same variable in the same scope.
> - **`let`** does not — it throws a `SyntaxError`.
>
> ```javascript
> var z = 1;
> var z = 2; // OK
>
> let w = 1;
> let w = 2; // SyntaxError
> ```
>
> ## 4. Global object property
>
> - A **`var`** declared at the top level becomes a property of the global object (`window` in browsers).
> - **`let`** does not.
>
> ```javascript
> var foo = 1;
> let bar = 2;
> console.log(window.foo); // 1
> console.log(window.bar); // undefined
> ```
>
> ## 5. Loop behavior (closures)
>
> With **`let`**, each loop iteration gets a fresh binding, which matters in closures. **`var`** shares a single binding across all iterations.
>
> ```javascript
> for (var i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i)); // 3, 3, 3
> }
>
> for (let j = 0; j < 3; j++) {
>   setTimeout(() => console.log(j)); // 0, 1, 2
> }
> ```
>
> ## Summary
>
> | Feature | `var` | `let` |
> |---|---|---|
> | Scope | Function | Block |
> | Hoisting | Yes, initialized `undefined` | Yes, but TDZ |
> | Redeclaration | Allowed | Not allowed |
> | Global object property | Yes | No |
> | Per-iteration binding | No | Yes |
>
> **Recommendation:** Prefer `let` (and `const`) in modern JavaScript. `var`'s function-scoping and hoisting quirks are common sources of bugs. Use `const` by default, `let` when you need to reassign, and avoid `var` unless you have a specific reason.

**Kevin** (123 words)

> `let`: block-scoped. `var`: function-scoped.
>
> Key differences:
>
> - **Scope** — `let` lives in its `{ }` block. `var` ignores blocks, lives in whole function.
> - **Hoisting** — both hoist, but `var` inits to `undefined`. `let` sits in "temporal dead zone" — touch before declare, ReferenceError.
> - **Redeclare** — `var x; var x;` fine. `let x; let x;` throws.
> - **Loops** — `let` makes fresh binding per iteration. `var` shares one. Classic closure-in-loop trap.
> - **Global** — top-level `var` attaches to `window`. `let` no.
>
> ```js
> for (var i = 0; i < 3; i++) setTimeout(() => console.log(i)); // 3 3 3
> for (let j = 0; j < 3; j++) setTimeout(() => console.log(j)); // 0 1 2
> ```
>
> Rule: use `let` (or `const`). Skip `var`.

---

## How does a bloom filter work?

**Normal** (492 words)

> A bloom filter is a space-efficient probabilistic data structure that answers one question: "Is this element possibly in the set, or definitely not?"
>
> ## The core idea
>
> It's a bit array of size *m* (all zeros initially) plus *k* independent hash functions, each of which maps any element to one of the *m* positions.
>
> **Adding an element:**
> 1. Run the element through all *k* hash functions to get *k* positions.
> 2. Set the bit at each of those positions to 1.
>
> **Querying an element:**
> 1. Run the element through the same *k* hash functions.
> 2. Check the bits at those *k* positions.
> 3. If **any** bit is 0 → the element is **definitely not** in the set.
> 4. If **all** bits are 1 → the element is **probably** in the set.
>
> ## Why the asymmetry
>
> A bloom filter can produce **false positives** but never **false negatives**.
>
> - If you added an element, you set its bits to 1, so a later query for it always sees all 1s. No false negatives.
> - But bits are shared across elements. Other insertions may have set exactly the bits your queried element hashes to, making it *look* present when it isn't. That's a false positive.
>
> ## A small example
>
> Say *m* = 10 bits, *k* = 2 hash functions.
>
> - Add `"cat"`: hashes to positions 1 and 4 → set bits 1, 4.
> - Add `"dog"`: hashes to positions 4 and 7 → set bits 4, 7.
> - Bit array now: `0 1 0 0 1 0 0 1 0 0`
> - Query `"cat"`: positions 1, 4 both 1 → probably present. Correct.
> - Query `"fish"`: hashes to 2, 7 → bit 2 is 0 → definitely absent. Correct.
> - Query `"bird"`: hashes to 1, 7 → both happen to be 1 → reports "probably present" even though never added. **False positive.**
>
> ## Key properties
>
> - **No deletions** (in the basic version): clearing bits could break other elements. Variants like *counting bloom filters* use small counters instead of bits to allow removal.
> - **Tunable error rate:** the false-positive probability is roughly `(1 - e^(-kn/m))^k`, where *n* is the number of inserted elements. You trade memory (*m*) and hash count (*k*) against accuracy.
> - **Optimal k:** for a given *m* and *n*, the best number of hash functions is `k = (m/n) · ln 2`.
> - **Very compact:** stores no actual elements, just bits — so it uses far less space than a hash set, at the cost of occasional false positives.
>
> ## Where they're used
>
> - Databases (e.g., Cassandra, HBase, Bigtable) skip disk lookups for rows that definitely don't exist.
> - Web caches and CDNs check whether content is worth caching.
> - Browsers/security tools check URLs against malicious-site lists.
> - Distributed systems reduce expensive network or disk queries.
>
> The pattern is always the same: use the bloom filter as a cheap first-pass filter to avoid an expensive operation when the answer is "definitely not there."

**Kevin** (119 words)

> Bloom filter: probabilistic set membership. "Maybe in set" or "definitely not."
>
> How:
> - Bit array, all zeros. Size m.
> - k hash functions.
> - Add item: hash k times, set those k bits to 1.
> - Check item: hash k times, look at those k bits.
>   - Any bit 0 → definitely not in set.
>   - All bits 1 → probably in set.
>
> Why "probably": other items' bits can collide, flip yours on. False positives possible. False negatives never.
>
> Tradeoff: tiny memory, fast. Pay with false positive rate. More bits, more hashes (tuned) → lower rate.
>
> No delete (bits shared). Counting bloom filter fixes that with counters not bits.
>
> Use: cache miss skip, dedupe, "have I seen this URL."

---

## What is a foreign key in a database?

**Normal** (240 words)

> A foreign key is a column (or set of columns) in one database table that refers to the primary key of another table. It creates a link between the two tables, establishing a relationship between their rows.
>
> Key points:
>
> - **Purpose**: It enforces *referential integrity*, meaning a value in the foreign key column must match an existing value in the referenced table (or be NULL). This prevents "orphaned" records that point to data that doesn't exist.
>
> - **Example**: Suppose you have an `Orders` table and a `Customers` table. The `Orders` table might have a `customer_id` column that is a foreign key referencing the `id` (primary key) of the `Customers` table. This ties each order to a valid customer.
>
> ```
> Customers              Orders
> +----+-------+         +----+-------------+--------+
> | id | name  |         | id | customer_id | total  |
> +----+-------+         +----+-------------+--------+
> | 1  | Alice |         | 10 | 1           | 50.00  |
> | 2  | Bob   |         | 11 | 2           | 75.00  |
> +----+-------+         | 12 | 1           | 20.00  |
>                        +----+-------------+--------+
> ```
>
> - **Cascading actions**: Foreign keys can define what happens when the referenced row is updated or deleted, such as `ON DELETE CASCADE` (delete related rows) or `ON DELETE SET NULL`.
>
> - **Benefits**: They keep data consistent, model relationships (one-to-many, many-to-many via a join table), and prevent invalid references.
>
> In short, a foreign key is the mechanism relational databases use to connect tables and guarantee that those connections stay valid.

**Kevin** (51 words)

> Foreign key: column in one table pointing to primary key of another. Links rows across tables.
>
> Database enforces it. Value must exist in referenced table, or insert/update fails. Stops orphan rows.
>
> Example: `orders.customer_id` points to `customers.id`. Each order ties to real customer.
>
> Gives referential integrity. Can block or cascade deletes too.

---
