f = open("timetable.log","r")
lines = f.read()
stats= {"methods":{},"users":{}, "endpoints":{},"statuses":{}}
unique_users = set()
timetables_generated=timetable_generate_count= iterative_count=heuristic_count = 0

for line in lines.split("\n"):

    parts = line.split(" ")

    if(len(parts) > 3):
        date = parts[0]
        date_time = parts[1]
        ip = parts[2]

        request_type = parts[3]
        if(request_type in ["GET", "POST", "router:"]):
            endpoint = parts[4]

            stats["methods"][request_type] = stats["methods"].get(request_type,0)+1

            if(request_type in ["GET", "POST"]):
                status = parts[5]
                time = parts[6]

                division_factor=1000
                if(time[-2:]== "ms"):
                    division_factor=1
                stats["endpoints"].setdefault(endpoint, []).append(float(time[0:-2])/division_factor)
                stats["statuses"][status] = stats["statuses"].get(status,0)+1



            elif (request_type == "router:" and len(parts)>5):
                user = parts[5]
                year = user[1:5]

                if(user not in unique_users):
                    stats["users"][year] = stats["users"].get(year, 0) + 1
                    unique_users.add(user)
        else:

            if("Generation" in line):
                timetables_generated += int(parts[7])
                timetable_generate_count +=1
            elif("Heuristic" in line):
                heuristic_count+=1
            elif("Iterative" in line):
                iterative_count+=1

for endpoint in stats["endpoints"]:
    endpoint_data = stats["endpoints"][endpoint]
    count = len(endpoint_data)
    max_time = max(endpoint_data)
    avg = sum(endpoint_data)/count

    stats["endpoints"][endpoint]=[count,max_time,avg]

f.close()

# done using ai vvvv didnt want to manually do it
def print_report(stats):
    total_requests = sum(stats["methods"].get(m, 0) for m in ["GET", "POST"])

    print("\n📊 Traffic & Usage Analysis")
    print("-" * 40)
    print(f"Total API Requests Logged: {total_requests}\n")

    # Endpoint Popularity
    print("Endpoint Popularity:")
    total_endpoint_hits = sum(v[0] if isinstance(v, list) else 0 for v in stats["endpoints"].values())
    for endpoint, data in stats["endpoints"].items():
        # data is [count, max_time, avg]
        count = data[0] if isinstance(data, list) else 0
        percent = (count / total_endpoint_hits) * 100 if total_endpoint_hits else 0
        print(f" - {endpoint}: {count} requests ({percent:.1f}%)")
    print()

    # HTTP Status Codes
    print("HTTP Status Codes:")
    for code, count in stats["statuses"].items():
        print(f" - {code}: {count} times")
    print("-" * 40)

    # Performance Metrics
    print("\n🚀 Performance Metrics")
    print("-" * 40)
    for endpoint, data in stats["endpoints"].items():
        # data: [count, max_time, avg]
        count, max_time, avg_time = data
        print(f"Endpoint: {endpoint}")
        print(f" - Average Response Time: {avg_time:.2f} ms")
        print(f" - Max Response Time: {max_time:.2f} ms")

    # --- Application-Specific Insights ---
    print("\n-------------------------------")
    print("⚙️ Application-Specific Insights")
    print("-------------------------------")
    print("Timetable Generation Strategy Usage:")
    print(f"  - Heuristic Backtracking: {heuristic_count} times")
    print(f"  - Iterative Random Sampling: {iterative_count} times")
    avg_per_call = round(timetables_generated / timetable_generate_count, 2) if timetable_generate_count else 0
    print(f"\nAverage Timetables Found per /generate call: {avg_per_call}")
    print(f"Total number of timetables generated: {timetables_generated}")

    # --- Unique ID Analysis ---
    print("-------------------------------")
    print("🧑‍💻 Unique ID Analysis")
    print("-------------------------------")
    print(f"Total Unique IDs found: {len(unique_users)}")
    for year in sorted(stats["users"].keys()):
        print(f"Batch of {year}: {stats['users'][year]} unique IDs")


print_report(stats)
