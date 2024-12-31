import random
import os
from PIL import Image
from itertools import product
import noise_gen as ng
import body_gen as bg
from planet_type import PlanetType  # Import the PlanetType class

class PlanetGenerator:
    planet_count = 0  # Initialize the planet count

    def __init__(self):
        self.output_image = None
        self.resolution = 2048  # resolution
        self.avg_temperature = random.randint(-50, 50)  # Random average temperature
        self.star_type = random.choice(["m", "k", "g"])  # Random star type
        
        # Create an instance of PlanetType to generate a random planet configuration
        self.planet_type = PlanetType()
        self.planet_config = self.planet_type.generate_random_planet_type()  # Generate random planet configuration

        # Create an instance of NoiseGen
        self.noise_gen = ng.NoiseGen()
        self.noise_gen.set_avg_temperature(self.avg_temperature)  # Set initial temperature

        self.generate_planet()  # Generate the planet immediately

    def generate_planet(self):
        water_normalized_noise, land_normalized_noise = self.noise_gen.generate_noise(self.resolution)
        clouds_noise_map = self.noise_gen.generate_clouds_noise(self.resolution)
        water_map, land_map = bg.BodyGen.generate_colors(self.avg_temperature, self.planet_config)  # Pass the planet config here
        cloud_map = bg.BodyGen.generate_clouds()  # Ensure this method exists

        land_image = Image.new("RGBA", (self.resolution, self.resolution))
        clouds_image = Image.new("RGBA", (self.resolution, self.resolution))
        water_image = Image.new("RGBA", (self.resolution, self.resolution))

        land_array = land_image.load()
        clouds_array = clouds_image.load()
        water_array = water_image.load()

        for y, x in product(range(self.resolution), repeat=2):
            planet_noise_value = land_normalized_noise[y, x]
            land_array[x, y] = self.find_color(planet_noise_value, land_map)

            cloud_noise_value = clouds_noise_map[y, x]
            clouds_array[x, y] = self.find_color(cloud_noise_value, cloud_map)

            water_noise_value = water_normalized_noise[y, x]
            water_array[x, y] = self.find_color(water_noise_value, water_map)

        # Load shadow image
        shadow_image_path = os.path.join(os.path.dirname(__file__), "resources", "shadow.png")
        shadow_image = Image.open(shadow_image_path).resize((self.resolution, self.resolution), Image.LANCZOS)
        
        self.output_image = Image.alpha_composite(water_image, land_image)
        self.output_image = Image.alpha_composite(self.output_image, clouds_image)
        self.output_image = Image.alpha_composite(self.output_image, shadow_image)

#        self.save_planet()  # Save the planet image after generation

    @staticmethod
    def find_color(noise_value, color_map):
        for (lower, upper), color in color_map.items():
            if lower <= noise_value <= upper:
                return color
        return 0, 0, 0, 0

if __name__ == "__main__":
    generator = PlanetGenerator()