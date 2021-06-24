def validate(shared_key, other_shared_key, min_shared_percent):
    if len(shared_key) > 0 and len(shared_key) == len(other_shared_key):
        i = 0
        count = 0
        decision = 0
        while i < len(shared_key):
            if shared_key[i] == other_shared_key[i]:
                count += 1
            i += 1
        if count >= min_shared_percent*len(shared_key):
            decision = 1
        else:
            decision = 0
        return decision    
    else:
        print("Error")
        return -1
