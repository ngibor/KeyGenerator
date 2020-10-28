from generator.generator_factory import instantiate_drgb

if __name__ == "__main__":

    generator = instantiate_drgb(256, "string")
    for i in range(10):
        number = int(generator.generate(128), 2)
        print(number)




