

# ======================= ALGORITHM 1 =======================
from collections import defaultdict

import random
import math
import time   
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def kmeans(points, k, max_iter=10):
    centers = random.sample(points, k)
    
    print("\nInitial Centroids:", centers)

    for iteration in range(max_iter):
        # print(f"\n================ ITERATION {iteration+1} ================")

        clusters = [[] for _ in range(k)]

        # -------- ASSIGNMENT STEP --------
        # print("\n--- Distance Calculation & Assignment ---")
        for i, p in enumerate(points):
            # print(f"\nPoint {p}:")

            dists = []
            for j, c in enumerate(centers):
                d = distance(p, c)
                # print(f"Distance to Centroid {j+1} {c} = √(({p[0]}-{c[0]})² + ({p[1]}-{c[1]})²) = {round(d,3)}")
                dists.append(d)

            min_index = dists.index(min(dists))
            # print(f"→ Assigned to Cluster {min_index+1}")

            clusters[min_index].append(i)

        # -------- PRINT CLUSTERS --------
        # print("\n--- Clusters Formed ---")
        for idx, cl in enumerate(clusters):
            cl_points = [points[i] for i in cl]
            # print(f"Cluster {idx+1}: {cl_points}")

        # -------- UPDATE STEP --------
        # print("\n--- Centroid Update ---")
        new_centers = []

        for idx, cl in enumerate(clusters):
            if cl:
                xs = [points[i][0] for i in cl]
                ys = [points[i][1] for i in cl]

                # print(f"\nCluster {idx+1} Points: {[points[i] for i in cl]}")
                # print(f"New Centroid {idx+1} = (sum(x)/n, sum(y)/n)")

                cx = sum(xs) / len(xs)
                cy = sum(ys) / len(ys)

                # print(f"= ({sum(xs)}/{len(xs)}, {sum(ys)}/{len(ys)})")
                # print(f"= ({round(cx,3)}, {round(cy,3)})")

                new_centers.append((round(cx,3), round(cy,3)))
            else:
                new_center = random.choice(points)
                # print(f"Cluster {idx+1} empty → random centroid {new_center}")
                new_centers.append(new_center)

        # print("\nUpdated Centroids:", new_centers)

        # -------- CONVERGENCE CHECK --------
        if new_centers == centers:
            # print("\n Converged: No change in centroids")
            break

        centers = new_centers

    return clusters, centers


# ------------------ INPUT ------------------
n = int(input("Enter number of points: "))
k = int(input("Enter number of clusters: "))

points = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(n)]

print("\nTotal Location Points:", points)
executors = [f"E{i+1}" for i in range(n)]
clusters, centers = kmeans(points, k)

print("\n================ FINAL RESULT ================\n")
cluster_executors = {}
for idx, cl in enumerate(clusters, start=1):
    cl_points = [points[i] for i in cl]
    cl_execs = [executors[i] for i in cl]
    cluster_executors[idx] = cl_execs
    print(f"Cluster {idx}: {cl_points}")
    print(f"Final Centroid: {centers[idx-1]}\n")
    print(f"Task Executors: {cl_execs}\n")



# ------------------ STRICT TIE BREAK FUNCTION ------------------
def strict_level_tie_break(top_executors, preferences, voters):
    score = {e: 0 for e in top_executors}
    for v in voters:
        pref_list = preferences[v]
        for i, e in enumerate(pref_list):
            if e in score:
                score[e] += (len(pref_list) - i)
    winner = max(score, key=score.get)
    return winner, score



print("\n================ CLUSTER-WISE WINNERS =================\n")
cluster_winners = {}

for cluster_id, cluster_execs in cluster_executors.items():

    print(f"\n******** Cluster {cluster_id} ********")
    print("Executors:", cluster_execs)

    total_votes = {e: 0 for e in cluster_execs}
    final_cluster_winners = []

    if len(cluster_execs) == 1:
        cluster_winners[cluster_id] = [cluster_execs[0]]
        print("Only one executor → Winner:", cluster_execs[0])
        continue

    remaining_executors = cluster_execs.copy()
    iteration = 1

    while remaining_executors:

        if len(remaining_executors) == 1:
            print("\nOnly one remaining → stopping iterations.")
            break

        print(f"\nIteration {iteration}:")

        #  FIX: Always select at least 3 executors
        if len(remaining_executors) >= 3:
            selected = random.sample(remaining_executors, 3)
        else:
            selected = remaining_executors.copy()

        print("Selected Executors:", selected)

        voters = [e for e in cluster_execs if e not in selected]
        preferences = {}

        if not voters:
            print("No voters → stopping iteration and moving to next")
            break

        else:
            print("\nRandom Task Executors Preferences:")
            for v in voters:
                preferences[v] = random.sample(selected, len(selected))
                print(f"{v}: {preferences[v]}")

            votes = {e: 0 for e in selected}
            for v in voters:
                votes[preferences[v][0]] += 1

            max_votes = max(votes.values())
            top_executors = [e for e, c in votes.items() if c == max_votes]

            if len(top_executors) > 1:
                winner, _ = strict_level_tie_break(top_executors, preferences, voters)
            else:
                winner = top_executors[0]

        print("Votes this iteration:", votes)
        print("Iteration winner:", winner)

        if winner not in final_cluster_winners:
            final_cluster_winners.append(winner)

        for e, v in votes.items():
            total_votes[e] += v

        remaining_executors = [e for e in remaining_executors if e not in selected]
        iteration += 1

    cluster_winners[cluster_id] = final_cluster_winners
    print("\nFinal Cluster Winners:", final_cluster_winners)


print("\n================ FINAL WINNERS =================")
for c, w in cluster_winners.items():
    print(f"Cluster {c} Winner → {w}")
    pass


# --------- FINAL EXECUTORS FOR ALGO 2 ----------
final_executors = sorted({e for w in cluster_winners.values() for e in w})

print("\n================ FINAL EXECUTORS PASSED TO ALGO 2 =================")
print(final_executors)

# =====================================================
# ================= ALGORITHM 2 =======================
# =====================================================

num_requesters = int(input("\nEnter number of requesters: "))
num_tasks = int(input("Enter number of tasks: "))

TASKS = [f"T{i}" for i in range(1, num_tasks + 1)]
requesters = [f"R{i}" for i in range(1, num_requesters + 1)]

def gen_req_vals(reqs):
    vals = {}
    for r in reqs:
        chosen = random.sample(TASKS, random.randint(1, min(4, len(TASKS))))
        vals[r] = {t: random.randint(8, 30) for t in chosen}
    return vals


def gen_exe_costs(exs):
    costs = {}
    for e in exs:
        chosen = random.sample(TASKS, random.randint(1, min(4, len(TASKS))))
        costs[e] = {t: random.randint(5, 25) for t in chosen}
    return costs

req_val = gen_req_vals(requesters)
exe_cost = gen_exe_costs(final_executors)

print("\n===== REQUESTERS TASK COSTS =====")
for r, tasks in req_val.items():
    print(f"{r}:")
    for t, cost in tasks.items():
        print(f"  Task {t} -> Cost {cost}")
        pass

print("\n===== EXECUTORS TASK COSTS =====")
for e, tasks in exe_cost.items():
    print(f"{e}:")
    for t, cost in tasks.items():
        print(f"  Task {t} -> Cost {cost}")
        pass

    task_to_r, task_to_e = {}, {}

    for r in requesters:
        for t, v in req_val[r].items():
            task_to_r.setdefault(t, []).append(r)

    for e in final_executors:
        for t, c in exe_cost[e].items():
            task_to_e.setdefault(t, []).append(e)

executable = set(task_to_r) & set(task_to_e)

print("\n--- TASKS READY FOR EXECUTION ---")
for t in executable:
    print(f"Task {t} | Requesters: {task_to_r[t]} | Executors: {task_to_e[t]}")
    pass
# =====================================================
# ================= MCAFEE MECHANISM ==================
# =====================================================

def execute_mcafee(tasks, task_to_r, task_to_e, req_val, exe_cost):

    print("\n================ MCAFEE TRADE EXECUTION =================")

    start_time = time.time()
    
    total_payment_to_executors = 0
    total_payment_by_requesters = 0

    total_req_utility = 0
    total_exe_utility = 0
    completed = 0
    total_remaining_requester_units = 0
    total_remaining_executor_units = 0
    for t in tasks:

        print(f"\n--- Task {t} ---")

        bids = sorted(
            [(r, req_val[r][t]) for r in task_to_r[t]],
            key=lambda x: x[1],
            reverse=True
        )

        asks = sorted(
            [(e, exe_cost[e][t]) for e in task_to_e[t]],
            key=lambda x: x[1]
        )

        print("Sorted Bids :", bids)
        print("Sorted Asks :", asks)

        k = min(len(bids), len(asks))

        if k == 0:
            continue

        m = -1

        # Find efficient trade size
        for i in range(k):
            if bids[i][1] >= asks[i][1]:
                m = i + 1
            else:
                break

        if m <= 0:
            print("No trade possible.")
            continue


        # ================= CASE I =================
        if m < k:

            b_next = bids[m][1]
            s_next = asks[m][1]

            price = (b_next + s_next) / 2

            if price <= bids[m-1][1] and price >= asks[m-1][1]:

                print("McAfee Case I Price:", round(price,2))

                trade_count = m

                for i in range(trade_count):

                    r, bid = bids[i]
                    e, ask = asks[i]

                    ur = bid - price
                    ue = price - ask

                    total_req_utility += ur
                    total_exe_utility += ue
                    total_payment_to_executors += price
                    total_payment_by_requesters += price
                    completed += 1

                    print(f"Matched → {r} ↔ {e} | U({r})={ur:.2f}, U({e})={ue:.2f}")

                continue


        # ================= CASE II =================

        trade_count = m - 1

        if trade_count <= 0:
            print("Price test failed → No trade.")
            total_remaining_requester_units += len(bids)
            total_remaining_executor_units += len(asks)
            continue

        bid_price = bids[m-1][1]
        ask_price = asks[m-1][1]

        print("McAfee Case II Prices:")
        print("Price for buyers :", bid_price)
        print("Price for sellers:", ask_price)

        for i in range(trade_count):

            r, bid = bids[i]
            e, ask = asks[i]

            ur = bid - bid_price
            ue = ask_price - ask

            total_req_utility += ur
            total_exe_utility += ue
            total_payment_to_executors += ask_price
            total_payment_by_requesters += ask_price
            completed += 1

            print(f"Matched → {r} ↔ {e} | U({r})={ur:.2f}, U({e})={ue:.2f}")
        remaining_r_units = len(bids) - trade_count
        remaining_e_units = len(asks) - trade_count

        total_remaining_requester_units += remaining_r_units
        total_remaining_executor_units += remaining_e_units           

    end_time = time.time()

    print("\n=========== MCAFEE SUMMARY ===========")
    # print("Total trades:", completed)
    print("Total requester utility:", round(total_req_utility,2))
    print("Total executor utility :", round(total_exe_utility,2))
    print("Total payment made to executors:", round(total_payment_to_executors,2))
    print("Total payment made by requesters:", round(total_payment_by_requesters,2))
    # print("Total remaining requester units:", total_remaining_requester_units)
    # print("Total remaining executor units :", total_remaining_executor_units)   
    print(f"Execution time: {(end_time-start_time)*1000:.3f} ms")
    
execute_mcafee(executable, task_to_r, task_to_e, req_val, exe_cost)

#----------------MUDA---------------------------#


LSCZ, RSCZ = {"requesters": [], "executors": []}, {"requesters": [], "executors": []}

for r in requesters:
    (LSCZ if random.random() < 0.5 else RSCZ)["requesters"].append(r)
for e in final_executors:
    (LSCZ if random.random() < 0.5 else RSCZ)["executors"].append(e)

print("\n================ MARKET SPLIT ================")
print("LSCZ Requesters:", LSCZ["requesters"])
print("LSCZ Executors :", LSCZ["executors"])
print("RSCZ Requesters:", RSCZ["requesters"])
print("RSCZ Executors :", RSCZ["executors"])


req_val_L = {r: req_val[r] for r in LSCZ["requesters"]}
exe_cost_L = {e: exe_cost[e] for e in LSCZ["executors"]}


req_val_R = {r: req_val[r] for r in RSCZ["requesters"]}
exe_cost_R = {e: exe_cost[e] for e in RSCZ["executors"]}



if len(LSCZ["requesters"]) < 1 or len(LSCZ["executors"]) < 1:
    raise ValueError("Left market too thin — rerun the program.")

    
if len(RSCZ["executors"]) < 1 or len(RSCZ["requesters"]) < 1:
     raise ValueError("Right market too thin — rerun the program.")

def equilibrium_price(zone, reqs, exs, req_vals, exe_costs):
    print(f"\n--- EQUILIBRIUM PRICE IN {zone} ---")
    prev_p, prev_DL = 0, 0

    for i in range(20):
        p = i * 3
        DL = sum(1 for r in reqs for v in req_vals[r].values() if v >= p)
        SL = sum(1 for e in exs for c in exe_costs[e].values() if c <= p)

        print(f"p={p} | DL={DL} | SL={SL}")

        if DL == SL and DL > 0:
            break
        if SL > DL and prev_DL > 0:
            p = prev_p
            break

        prev_p, prev_DL = p, DL

    print("Equilibrium price:", p)

    task_to_r, task_to_e = {}, {}

    for r in reqs:
        for t, v in req_vals[r].items():
            if v >= p:
                task_to_r.setdefault(t, []).append(r)

    for e in exs:
        for t, c in exe_costs[e].items():
            if c <= p:
                task_to_e.setdefault(t, []).append(e)

    executable = set(task_to_r) & set(task_to_e)

    print("\n--- TASKS READY FOR EXECUTION ---")
    for t in executable:
        print(f"Task {t} | Requesters: {task_to_r[t]} | Executors: {task_to_e[t]}")
        pass

    return p, executable, task_to_r, task_to_e


pL, tasks_L, task_to_r_L, task_to_e_L = equilibrium_price(
    "LSCZ", LSCZ["requesters"], LSCZ["executors"], req_val_L, exe_cost_L
)

pR, tasks_R, task_to_r_R, task_to_e_R = equilibrium_price(
    "RSCZ", RSCZ["requesters"], RSCZ["executors"], req_val_R, exe_cost_R
)


# =====================================================
# ========== TRANSPARENT TRADE EXECUTION ==============
# =====================================================

def execute_MUDA(zone, price, tasks, task_to_r, task_to_e, req_vals, exe_costs):
    
    start_time = time.time() 
    total_payment_to_executors = 0
    total_payment_by_requesters = 0
    print(f"\n================ MUDA TRADE EXECUTION IN {zone} =================")
    print(f"Market price used (opposite market): p = {price}")

    completed = 0
    util_r, util_e = {}, {}
    rem_r, rem_e = {}, {}
  
    # # ---------------------------------------------
    req_pool = {r: list(req_vals[r].items()) for r in req_vals}
    exe_pool = {e: list(exe_costs[e].items()) for e in exe_costs}


    for t in tasks:

        print(f"\n--- Task {t} ---")
                # ---------- BUILD ELIGIBLE REQUESTER UNITS ----------
        rq_units = []
        for r in task_to_r[t]:
            eligible = [(task, val) for (task, val) in req_pool[r] if task == t and val >= price]

            for pair in eligible:
                rq_units.append((r, pair[1]))
                req_pool[r].remove(pair)

        # ---------- BUILD ELIGIBLE EXECUTOR UNITS ----------
        ex_units = []
        for e in task_to_e[t]:
            eligible = [(task, cost) for (task, cost) in exe_pool[e] if task == t and cost <= price]

            for pair in eligible:
                ex_units.append((e, pair[1]))
                exe_pool[e].remove(pair)

                
        print("Eligible Requester Units:", [r for r,_ in rq_units])
        print("Eligible Executor Units :", [e for e,_ in ex_units])

        # ---------- MATCHING ----------
        while rq_units and ex_units:

            rq_units.sort(key=lambda x: -x[1])   # highest value first
            ex_units.sort(key=lambda x: x[1])    # lowest cost first

            r, v = rq_units.pop(0)
            e, c = ex_units.pop(0)

            # SAFETY CHECK (very important in MUDA)
            if v < price or c > price:
                break

            ur = v - price
            ue = price - c
            total_payment_to_executors += price
            total_payment_by_requesters += price

            util_r[r] = util_r.get(r, 0) + ur
            util_e[e] = util_e.get(e, 0) + ue

            print(f"Matched → {r} ↔ {e} | U({r})={ur}, U({e})={ue}")
            completed += 1

        # ---------- REMAINING ----------
        for r, _ in rq_units:
            rem_r[r] = rem_r.get(r, 0) + 1
        for e, _ in ex_units:
            rem_e[e] = rem_e.get(e, 0) + 1
            
    end_time = time.time()     #  end timing
    elapsed_ms = (end_time - start_time) * 1000
    # ---------- TOTAL UTILITIES ----------
    total_req_utility = sum(util_r.values()) if util_r else 0
    total_exe_utility = sum(util_e.values()) if util_e else 0
    # ---------- TOTAL REMAINING UNITS ----------
    total_remaining_requester_units = sum(rem_r.values()) if rem_r else 0
    total_remaining_executor_units  = sum(rem_e.values()) if rem_e else 0

    print("\n=========== MUDA EXECUTION SUMMARY ===========")
    # print("Remaining requester units:", rem_r if rem_r else "None")
    # print("Remaining executor units :", rem_e if rem_e else "None")
    # print("Task units completed:", completed)
    print("Total Requester utilities:", total_req_utility)
    print("Total Executor utilities :", total_exe_utility)
    print("Total payment made to executors :", total_payment_to_executors)
    print("Total payment made by requesters :", total_payment_by_requesters)
    # print("Total remaining requester units :", total_remaining_requester_units)
    # print("Total remaining executor units  :", total_remaining_executor_units)
    print(f" Execution time ({zone}) : {elapsed_ms:.3f} milliseconds")


if pL == 0 or pR == 0:
    print("Markets too thin — cannot run MUDA.")
    exit()
print("\n\n================ RUNNING MUDA =================") 
execute_MUDA("LSCZ", pR, tasks_L, task_to_r_L, task_to_e_L, req_val_L, exe_cost_L) 


# # ======================= TMUDA =======================

 # ---------------- BUILD TASK MAPS (FIXED INDENTATION) ----------------

task_to_r = {}
task_to_e = {}

for r in requesters:
    for t in req_val[r]:
        task_to_r.setdefault(t, []).append(r)

for e in final_executors:
    for t in exe_cost[e]:
        task_to_e.setdefault(t, []).append(e)

executable = set(task_to_r.keys()) & set(task_to_e.keys())

print("\n--- TASKS READY FOR EXECUTION IN TMUDA ---")
for t in executable:
    print(f"Task {t} | Requesters: {task_to_r[t]} | Executors: {task_to_e[t]}")

# ---------------- EQUILIBRIUM FUNCTION ----------------

def equilibrium_price(zone, task, reqs, exs):

    print(f"\n--- EQUILIBRIUM PRICE IN {zone} ---")

    prev_p, prev_DL = 0, 0

    for i in range(20):
        p = i * 3

        DL = sum(
            1 for r in reqs
            if task in req_val[r] and req_val[r][task] >= p
        )

        SL = sum(
            1 for e in exs
            if task in exe_cost[e] and exe_cost[e][task] <= p
        )

        print(f"p={p} | DL={DL} | SL={SL}")

        if DL == SL and DL > 0:
            break
        if SL > DL and prev_DL > 0:
            p = prev_p
            break

        prev_p, prev_DL = p, DL

    print("Equilibrium price:", p)
    return p

# ================= GLOBAL TRACKERS =================

requester_payment = {r: 0 for r in requesters}
executor_payment  = {e: 0 for e in final_executors}

ur = defaultdict(int)
ue = defaultdict(int)

rem_r = defaultdict(int)
rem_e = defaultdict(int)

completed = 0

total_payment_to_executors_LSCZ = 0
total_payment_to_executors_RSCZ = 0
total_payment_by_requesters_LSCZ = 0
total_payment_by_requesters_RSCZ = 0

start_time = time.time()
# ===================== TMUDA =====================


print("\n================= Market Splitting and Equilibrium =========================")
total_req_util_LSCZ = 0
total_req_util_RSCZ = 0
total_exe_util_LSCZ = 0
total_exe_util_RSCZ = 0

for task in executable:   # only tasks that exist on both sides
# Zone-wise payment trackers
 
    
    task_requesters = task_to_r[task]
    task_executors  = task_to_e[task]

    print(f"\nFor task {task}:")

    # -------- SPLIT FOR THIS TASK ONLY --------
    LSCZ = {"requesters": [], "executors": []}
    RSCZ = {"requesters": [], "executors": []}

    for r in task_requesters:
        (LSCZ if random.random() < 0.5 else RSCZ)["requesters"].append(r)

    for e in task_executors:
        (LSCZ if random.random() < 0.5 else RSCZ)["executors"].append(e)

    # Ensure no side empty
    if not LSCZ["requesters"] and RSCZ["requesters"]:
        LSCZ["requesters"].append(RSCZ["requesters"].pop())
    if not RSCZ["requesters"] and LSCZ["requesters"]:
        RSCZ["requesters"].append(LSCZ["requesters"].pop())
    if not LSCZ["executors"] and RSCZ["executors"]:
        LSCZ["executors"].append(RSCZ["executors"].pop())
    if not RSCZ["executors"] and LSCZ["executors"]:
        RSCZ["executors"].append(LSCZ["executors"].pop())

    print("LSCZ Requesters:", LSCZ["requesters"])
    print("LSCZ Executors :", LSCZ["executors"])
    print("RSCZ Requesters:", RSCZ["requesters"])
    print("RSCZ Executors :", RSCZ["executors"])

    # -------- EQUILIBRIUM --------
    pL = equilibrium_price(
        "LSCZ", task,
        LSCZ["requesters"],
        LSCZ["executors"]
    )

    pR = equilibrium_price(
        "RSCZ", task,
        RSCZ["requesters"],
        RSCZ["executors"]
    )

    print("\n================ TRADE EXECUTION =================")
    print(f"\n--- Task {task} ---")
    
   
    # ================= LSCZ =================
    print(f"\nLSCZ Trades at price = {pR} (RSCZ price)")

    eligible_req_L = sorted(
        [r for r in LSCZ["requesters"]
         if task in req_val[r] and req_val[r][task] >= pR],
        key=lambda r: req_val[r][task],
        reverse=True
    )

    eligible_exe_L = sorted(
        [e for e in LSCZ["executors"]
         if task in exe_cost[e] and exe_cost[e][task] <= pR],
        key=lambda e: exe_cost[e][task]
    )

    print("Eligible Requesters:", eligible_req_L)
    print("Eligible Executors :", eligible_exe_L)

    trades_L = min(len(eligible_req_L), len(eligible_exe_L))

    if trades_L == 0:
        print("No trades executed in LSCZ.")
    else:
        for i in range(trades_L):
            r = eligible_req_L[i]
            e = eligible_exe_L[i]

            u_r = req_val[r][task] - pR
            u_e = pR - exe_cost[e][task]
            total_req_util_LSCZ += u_r
            total_exe_util_LSCZ += u_e
            requester_payment[r] += pR
            executor_payment[e]  += pR
            total_payment_to_executors_LSCZ += pR
            total_payment_by_requesters_LSCZ += pR
            ur[r] += u_r
            ue[e] += u_e

            completed += 1

            print(f"Matched → {r} ↔ {e} | U({r})={u_r}, U({e})={u_e}")

    # ================= RSCZ =================
    print(f"\nRSCZ Trades at price = {pL} (LSCZ price)")

    eligible_req_R = sorted(
        [r for r in RSCZ["requesters"]
         if task in req_val[r] and req_val[r][task] >= pL],
        key=lambda r: req_val[r][task],
        reverse=True
    )

    eligible_exe_R = sorted(
        [e for e in RSCZ["executors"]
         if task in exe_cost[e] and exe_cost[e][task] <= pL],
        key=lambda e: exe_cost[e][task]
    )

    print("Eligible Requesters:", eligible_req_R)
    print("Eligible Executors :", eligible_exe_R)

    trades_R = min(len(eligible_req_R), len(eligible_exe_R))

    if trades_R == 0:
        print("No trades executed in RSCZ.")
    else:
        for i in range(trades_R):
            r = eligible_req_R[i]
            e = eligible_exe_R[i]

            u_r = req_val[r][task] - pL
            u_e = pL - exe_cost[e][task]
            total_req_util_RSCZ += u_r
            total_exe_util_RSCZ += u_e
            requester_payment[r] += pL
            executor_payment[e]  += pL
            total_payment_to_executors_RSCZ += pL
            ur[r] += u_r
            ue[e] += u_e

            completed += 1
            print(f"Matched → {r} ↔ {e} | U({r})={u_r}, U({e})={u_e}")
            
           

elapsed_ms = (time.time() - start_time) * 1000

total_requester_utility = sum(ur.values())
total_executor_utility  = sum(ue.values())

total_payment_by_requesters = sum(requester_payment.values())
total_payment_to_executors  = sum(executor_payment.values())

total_remaining_requester_units = sum(rem_r.values())
total_remaining_executor_units  = sum(rem_e.values())

print("=================TMUDA FINAL SUMMARY =================")
# print("Requester utilities:", dict(ur) if ur else "None")
# print("Executor utilities :", dict(ue) if ue else "None")
# print("Remaining requester units:", dict(rem_r) if rem_r else "None")
# print("Remaining executor units :", dict(rem_e) if rem_e else "None")
# print("Task units completed:", completed)
# print(f"\nUtility for Task {task}:")
# print("Total requester utility        :", total_requester_utility)
print("Total Utility of task requesters in LSCZ :", total_req_util_LSCZ)
# print("Total Utility of task requesters in RSCZ :", total_req_util_RSCZ)
# print("Total executor utility         :", total_executor_utility)
print("Total Utility of task executors  in LSCZ :", total_exe_util_LSCZ)
# print("Total Utility of task executors  in RSCZ :", total_exe_util_RSCZ)
# print("Total payment made to executors :", total_payment_to_executors)
# print("Total payment by requesters     :", total_payment_by_requesters)
print("Total payment made to executors (LSCZ) :", total_payment_to_executors_LSCZ)
print("Total payment made by requesters (LSCZ) :", total_payment_by_requesters_LSCZ)
# print("Total payment made to executors (RSCZ) :", total_payment_to_executors_RSCZ)
# print("Remaining requester units    :", total_remaining_requester_units)
# print("Remaining executor units     :", total_remaining_executor_units)
print(f" Execution time : {elapsed_ms:.3f} milliseconds")


#==================PPM======================
total_payment_to_executors = 0

print("\n--- EQUILIBRIUM PRICE ---")
# ---- SAFETY: Convert executor costs to integers ----
for e in exe_cost:
    for t in exe_cost[e]:
        exe_cost[e][t] = int(exe_cost[e][t])


price_jump = 3
p = 0
prev_p = 0
prev_DL = 0

# Flatten requester valuations properly

all_req_units = [(r, t, v) for r in req_val for t, v in req_val[r].items()]
all_exe_units = [(e, c) for e, units in exe_cost.items() for _, c in units.items()]

itr = 0
while True:
    itr += 1
    p = price_jump * (itr - 1)

    DL = sum(1 for _, _, v in all_req_units if v >= p)
    SL = sum(1 for _, c in all_exe_units if c <= p)

    print(f"p={p} | DL={DL} | SL={SL}")

    if DL == SL and DL != 0:
        break

    if SL > DL and prev_DL > 0:
        p = prev_p
        break

    prev_p = p
    prev_DL = DL

# =====================================================
# ========== PPM TASKS READY FOR EXECUTION ================
# =====================================================
print(f"Equilibrium price: {p}")

task_to_r = defaultdict(list)
task_to_e = defaultdict(list)

for r, units in req_val.items():
    for t, v in units.items():   
        if v >= p:
            task_to_r[t].append(r)

for e, units in exe_cost.items():
    for t, c in units.items():   
        if c <= p:
            task_to_e[t].append(e)


tasks = [t for t in task_to_r if t in task_to_e]

print("\n--- PPM TASKS READY FOR EXECUTION ---")

for t in tasks:
    print(f"Task {t} | Requesters: {task_to_r[t]} | Executors: {task_to_e[t]}")
    pass
# =====================================================
# ================= TRADE EXECUTION ==================
# =====================================================
start_time = time.time()
print("\n================ PPM TRADE EXECUTION =================")
print(f"Equilibrium price: {p}")

completed = 0
ur = defaultdict(int)
ue = defaultdict(int)
rem_r = defaultdict(int)
rem_e = defaultdict(int)

total_payment_by_requesters = 0
for t in tasks:
    print(f"\n--- Task {t} ---")

    rq = task_to_r[t].copy()
    ex = task_to_e[t].copy()

    print("Eligible Requester Units:", rq)
    print("Eligible Executor Units :", ex)

    while rq and ex:
        r = rq.pop(0)
        e = ex.pop(0)

        # v = next(v for tt, v in req_val[r] if tt == t and v >= p)
        # c = next(c for tt, c in exe_cost[e] if tt == t and c <= p)
        v = req_val[r][t]
        c = exe_cost[e][t]



        ur[r] += v - p
        ue[e] += p - c
        total_payment_to_executors += p
        total_payment_by_requesters += p
        
        print(f"Matched → {r} ↔ {e} | U({r})={v-p}, U({e})={p-c}")
        completed += 1

    for r in rq:
        rem_r[r] += 1
    for e in ex:
        rem_e[e] += 1
end_time = time.time()
elapsed_ms = (end_time - start_time) * 1000
        # ---------- TOTAL UTILITIES ----------
total_requester_utility = sum(ur.values()) if ur else 0
total_executor_utility  = sum(ue.values()) if ue else 0

# ---------- TOTAL REMAINING UNITS ----------
total_remaining_requester_units = sum(rem_r.values()) if rem_r else 0
total_remaining_executor_units  = sum(rem_e.values()) if rem_e else 0
# ---------- TOTAL TASK UNITS FROM REQUESTERS ----------
total_requester_tasks = sum(len(tasks) for tasks in req_val.values())

print("\n=========== PPM EXECUTION SUMMARY ===========")
# print("Total number of task requester's task units :", total_requester_tasks)
# print("Requester utilities:", dict(ur) if ur else "None")
# print("Executor utilities :", dict(ue) if ue else "None")
# print("Remaining requester units:", dict(rem_r) if rem_r else "None")
# print("Remaining executor units :", dict(rem_e) if rem_e else "None")
#print("Task units completed:", completed)
print("Total requester utility        :", total_requester_utility)
print("Total executor utility         :", total_executor_utility)
print("Total payment made to executors :", total_payment_to_executors)
print("Total payment made by requesters :", total_payment_by_requesters)
# print("Remaining requester units    :", total_remaining_requester_units)
# print("Remaining executor units     :", total_remaining_executor_units)
print(f" Execution time : {elapsed_ms:.3f} milliseconds")


