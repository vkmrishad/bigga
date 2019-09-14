import os

CMD = 'docker ps'

os.system(CMD)
ls = os.popen(CMD).read().split('\n')[1:-1]
zombies = []
for line in ls:
    container, image = line.split()[:2]
    if 'bigga' not in image and ':' not in image:
        print(container, image)
        zombies.append(container)

print("Zombies: ", " ".join(zombies))
# docker kill <zombies>
# docker system prune
