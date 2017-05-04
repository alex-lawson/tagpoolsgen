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
        choice = random.choice(pools[key])
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

def replace_tags(string):
    result = re.subn('\[([a-zA-Z0-9 ]*)\]({([([a-zA-Z0-9 ^]*)})?', handle_match, string)
    if result[1] > 0:
        return replace_tags(result[0])
    else:
        return result[0]

def generate(targetcount, startstring):
    results = []
    while len(results) < targetcount:
        result = replace_tags(startstring)
        result = result[0].upper() + result[1:]
        # result = namify(result)
        print result
        results.append(result)
    return results

def load_pools():
    global pools
    pools={}

    cwd = os.getcwd()
    dirfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

    for fname in dirfiles:
        fbasename, fext = os.path.splitext(fname)
        if fext == '.tagpools':
            poolsfile=open(fname,'r')
            curkey=""
            for line in poolsfile:
                line=line.rstrip("\n")
                if line[0:1]=="$":
                    curkey = line[1:]
                    if not curkey in pools:
                        pools[curkey] = []
                elif len(line) > 0:
                    pools[curkey].append(line)
            poolsfile.close()

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
