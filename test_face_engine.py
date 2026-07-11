from src.ai.face.face_engine import FaceEngine


def main():

    engine = FaceEngine()

    print(engine)

    engine.load()

    print(engine)

    print()

    print(engine.dataset.summary())

    engine.unload()

    print()

    print(engine)


if __name__ == "__main__":
    main()