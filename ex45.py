from sys import exit
from random import randint
from textwrap import dedent

# --- Shared Game State ---
class GameState:
    def __init__(self):
        self.has_bow = False
        self.dead = False

game_state = GameState()

# --- Base Scene ---
class Scene:
    def enter(self):
        print("This scene is not yet configured.")
        exit(1)

# --- Engine ---
class Engine:
    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()

        while True:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

# --- Death Scene ---
class Death(Scene):
    def enter(self):
        quips = [
            "You were the last hope for humanity, but you failed.",
            "Your journey ends here, you were not strong enough.",
            "You better pray for your friends, they will need it.",
            "You were always destined to fail!",
        ]
        print(dedent(f"\n{quips[randint(0, len(quips)-1)]}"))
        exit(1)

# --- Village Scene ---
class Village(Scene):
    def enter(self):
        print(dedent("""
            --- Village of Eldermire ---

            You step into the heart of Eldermire. The market bustles, but something feels off.

            Where do you want to go?
            1. Your family’s farm
            2. The town elder’s house
            3. Anna’s home near the southern treeline
        """))
        choice = input("> ")

        if choice == "1":
            return 'farm'
        elif choice == "2":
            return 'elder_house'
        elif choice == "3":
            return 'anna_home'
        else:
            return 'village'

# --- Farm Scene ---
class Farm(Scene):
    def enter(self):
        print(dedent("""
            --- Aneemas’s Family Farm ---

            Dinner ends quietly. Then the quake hits. Sven shoves you toward the back door.
            A monstrous growl shakes the house.

            What do you do?
            1. Help Sven fight
            2. Run to John's farm
            3. Run to the barn and grab your bow
        """))

        choice = input("> ")

        if choice == "1":
            print(dedent("""
                You grab a knife and join Sven. You’re brave, but not strong enough.

                The beast crushes you both.
            """))
            game_state.dead = True
            return 'death'
        elif choice == "2":
            print(dedent("""
                You escape into the swamp and sprint to John's farm.

                Behind you, your home burns.
            """))
            return 'johns_farm'
        elif choice == "3":
            print(dedent("""
                You grab your bow and a quiver of arrows from the barn.

                Then you run into the swamp toward John's farm.
            """))
            game_state.has_bow = True
            return 'johns_farm'
        else:
            return 'death'

# --- John's Farm ---
class JohnsFarm(Scene):
    def enter(self):
        print(dedent("""
            --- John's Farm ---

            You collapse at John's porch. The beasts are attacking the pigs.

            John grabs an axe made for war.
        """))

        if game_state.has_bow:
            print("John sees the bow. 'Cover me from the porch.'")
        else:
            print("John hands you the axe. 'We fight side by side.'")

        print(dedent("""
            What do you do?
            1. Fight the beast with John
            2. Let the pigs out to distract them
            3. Get Anna and John's wife to safety
        """))
        choice = input("> ")

        if choice == "1":
            return 'death'
        elif choice == "2":
            return 'death'
        elif choice == "3":
            print("You escape through the swamp with Anna and John.")
            return 'village_two'
        else:
            return 'death'

# --- Elder House ---
class ElderHouse(Scene):
    def enter(self):
        print(dedent("""
            --- Town Elder’s House ---

            The elder is gone. Notes say the beasts weaken at sunrise.

            You find no help here.

            You head back toward the village.
        """))
        return 'village_two'

# --- Anna's House ---
class AnnaHome(Scene):
    def enter(self):
        print(dedent("""
            --- Anna’s Home ---

            Anna's father is already gone. She grabs her lantern and joins you.

            Together, you head back toward the village to help.
        """))
        return 'village_two'

# --- Village Defense ---
class VillageTwo(Scene):
    def enter(self):
        print(dedent("""
            --- Eldermire: Final Stand ---

            Smoke and screams fill the air. Beasts swarm in from the swamp.

            What do you do?
            1. Climb the chapel roof with your bow
            2. Fight in the streets beside John
            3. Rally the villagers and hold the line
        """))

        choice = input("> ")

        if choice == "1":
            if game_state.has_bow:
                print(dedent("""
                    You rain arrows from the rooftop as the sun rises.

                    The beasts turn to ash.

                    Eldermire is saved.
                """))
                return 'finished'
            else:
                print(dedent("""
                    You climb up, but have no weapon.

                    The beasts tear you down before the sun can rise.
                """))
                return 'death'
        elif choice == "2":
            print(dedent("""
                You fight shoulder to shoulder with John.

                When the sun rises, you are still alive.

                Eldermire is saved.
            """))
            return 'finished'
        elif choice == "3":
            print(dedent("""
                You shout orders. The villagers rally.

                The barricade holds just long enough — until the first light of dawn.

                You have become a leader.
            """))
            return 'finished'
        else:
            return 'death'

# --- Finished Scene ---
class Finished(Scene):
    def enter(self):
        print(dedent("""
            --- Dawn ---

            The beasts are gone. Smoke rises. Survivors gather in silence.

            You’ve saved Eldermire.

            But war is coming.

            Your story is just beginning.
        """))
        exit(0)

# --- Map ---
class Map:
    scenes = {
        'village': Village(),
        'farm': Farm(),
        'johns_farm': JohnsFarm(),
        'elder_house': ElderHouse(),
        'anna_home': AnnaHome(),
        'village_two': VillageTwo(),
        'death': Death(),
        'finished': Finished()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return self.scenes.get(scene_name)

    def opening_scene(self):
        return self.next_scene(self.start_scene)

# --- Run Game ---
a_map = Map('village')
a_game = Engine(a_map)
a_game.play()
