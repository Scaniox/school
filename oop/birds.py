birdName = ["robin",
            "blackbird",
            "pigeon",
            "magpie",
            "bluetit",
            "thrush",
            "wren",
            "starling"]


bird = input("enter bird name: ")
birdFound = False
numSpecies = len(birdName)
for count in range(numSpecies-1):
    if bird == birdName[count]:
        birdIndex = count
        birdFound = True

if not birdFound:
    print("Bird species not in array")
else:
    print(f"Bird found at: {birdindex}")

bird_count = [0 for i in range(numSpecies)]
bird = "blank"
while bird != x:
    bird = input("enter bird name (x to end): ")
    birdFound = False
    for count in range(8):
        if bird == birdName[count]:
            birdFound = True
            birdsObserved = input("number observed: ")
            birdCount[count] += birdsObserved

    if not birdFound:
        print("Bird species not in array")
