import random, sys, inflect, re, os

inf = inflect.engine()

# def namify(string):
#     string=string.title()
#     string=string.replace(" The "," the ")
#     string=string.replace(" Of "," of ")
#     string=string.replace(" In "," in ")
#     string=string.replace(" From "," from ")
#     string=string.replace(" At "," at ")
#     string=string.replace(" And "," and ")
#     string=string.replace("-Chan","-chan")
#     string=string.replace("lll","ll-l")
#     string=string.replace("ttt","tt-t")
#     string=string.replace("fff","ff-f")
#     string=string.replace("rrr","rr-r")
#     string=string.replace("eee","ee-e")
#     string=string.replace("sss","ss-s")
#     string=string.replace("aa","a-a")
#     string=string.replace("'S ","'s ")
#     string=string.replace("s's ","s' ")
#     return string

def handle_match(match):
    key = match.group(1)
    if key in pools:
        choice = pick_from_pool(key)
        choice = replace_tags(choice)
        if match.group(3):
            op = match.group(3)
            if op == 'nia':
                choice = inf.a(choice)
            if op == 'np':
                choice = inf.plural_noun(choice)
            elif op == 'vpp':
                choice = inf.present_participle(choice)
            elif op == 'vp':
                choice = inf.plural_verb(choice)
        return choice
    return "KEY '" + key + "' MISSING"

def replace_tags(flavors, string):
    def handler(match):
        key = match.group(1)
        choice = replace_tags(flavors, pick_from_pool(flavors, key))
        if match.group(3):
            op = match.group(3)
            if op == 'nia':
                choice = inf.a(choice)
            if op == 'np':
                choice = inf.plural_noun(choice)
            elif op == 'vpp':
                choice = inf.present_participle(choice)
            elif op == 'vp':
                choice = inf.plural_verb(choice)
        return choice

    result = re.subn('\[([a-zA-Z0-9 ]*)\]({([([a-zA-Z0-9 ^]*)})?', handler, string)
    return result[0]

def generate(targetcount, startstring):
    results = []
    while len(results) < targetcount:
        flavors = choose_flavors(2)
        result = replace_tags(flavors, startstring)
        result = result[0].upper() + result[1:]
        result = '{}    {}'.format(result, flavors)
        # result = namify(result)
        print result
        results.append(result)
    return results

def choose_flavors(targetcount):
    targetcount = min(targetcount, len(pools.keys()))
    flavors = ["base"]
    while len(flavors) < targetcount:
        f = random.choice(pools.keys())
        if not f in flavors:
            flavors.append(f)
    return flavors

def load_pools():
    global pools
    pools={}

    global poolsums
    poolsums = {}

    cwd = os.getcwd()
    dirfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

    for fname in dirfiles:
        fbasename, fext = os.path.splitext(fname)
        if fext == '.tagpools':
            fnameparts = fbasename.split('_')
            flavor = fnameparts[0]
            if not flavor in pools:
                pools[flavor] = {}
                poolsums[flavor] = {}

            poolsfile=open(fname,'r')
            curkey=""
            for line in poolsfile:
                line=line.rstrip("\n")
                if line[0:1]=="$":
                    curkey = line[1:]
                    if not curkey in pools[flavor]:
                        pools[flavor][curkey] = []
                        poolsums[flavor][curkey] = 0
                elif len(line) > 0:
                    lineparts = line.split(' ')
                    try:
                        itemweight = float(lineparts[0])
                        pools[flavor][curkey].append([itemweight, str.join(' ', lineparts[1:])])
                        poolsums[flavor][curkey] += itemweight
                    except ValueError:
                        pools[flavor][curkey].append([1.0, line])
                        poolsums[flavor][curkey] += 1
            poolsfile.close()

    for flavor, flavorpools in pools.iteritems():
        for poolname, pool in flavorpools.iteritems():
            if not poolsums[flavor][poolname]:
                poolsums[flavor][poolname] = 0

            # curweight = 1.0
            # poolsum = poolsums[flavor][poolname]
            # for i, item in enumerate(pool):
                # poolsums[flavor][poolname] += item[0]
                # itemweight = item[0] / poolsum
                # curweight -= itemweight
                # pool[i][0] = curweight

def pick_from_pool(flavors, poolname):
    # print("Trying to choose from pool {} with flavors {}".format(poolname, flavors))

    totalsum = 0
    for flavor in flavors:
        if poolname in poolsums[flavor]:
            totalsum += poolsums[flavor][poolname]

    randchoice = random.random() * float(totalsum)

    # print('random choice is {} total sum is {}'.format(randchoice, totalsum))

    weightcounter = 0
    for flavor in flavors:
        for poolitem in pools[flavor][poolname]:
            weightcounter += poolitem[0]
            # print('weightcounter {} item {}'.format(weightcounter, poolitem))
            if randchoice <= weightcounter:
                # print('selected {}'.format(poolitem[1]))
                return poolitem[1]

    # print("FAILED to choose from pool {} with flavors {}".format(poolname, flavors))

def main(argv):
    targetcount = 10
    if len(argv) > 0:
        targetcount = int(argv[0])

    startstring = "[GAME]"
    if len(argv) > 1:
        startstring = int(argv[1])

    load_pools()

    results = generate(targetcount, startstring)

    outfile=open("output.txt","w")
    for item in results:
        outfile.write(item+"\n")
    outfile.close()

if __name__ == "__main__":
   main(sys.argv[1:])
