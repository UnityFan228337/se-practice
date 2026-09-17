inp = input().split(",")
inpn = []
avg, pr = 0, 0
for i in inp:
    try:
        inti = int(i)
        if(inti < 0 or inti > 100): continue
        if(inti >= 50): pr+=1
        inpn.append(inti)
        avg += inti
    except:
        continue

valid = len(inpn)

if valid == 0: 
    print("No valid")
else:
    avg /= valid
    pr = str(pr / valid * 100) + "%"

    high = max(inpn)
    low = min(inpn)



    print("Valid: " + str(valid))
    print("Average: " + str(avg))
    print("Highest: " + str(high))
    print("Lowest: " + str(low))
    print("Pass rate: " + pr)