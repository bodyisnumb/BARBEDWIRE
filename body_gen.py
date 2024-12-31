from planet_type import PlanetType
import random

class BodyGen:
    @staticmethod
    def generate_colors(avg_temperature, planet_config):
        """
        Generates water and land color maps based on the average temperature
        and the planet configuration.
        """
        ocean_colors = planet_config["ocean"]
        land_colors = planet_config["land"]

        # Example logic to create color maps based on the selected colors
        water_map = {}
        land_map = {}

        # Generate water color map from ocean colors
        for i, color in enumerate(ocean_colors):
            water_map[(i/len(ocean_colors), (i+1)/len(ocean_colors))] = color  # Use ranges for mapping

        # Generate land color map from land colors
        for i, color in enumerate(land_colors):
            land_map[(i/len(land_colors), (i+1)/len(land_colors))] = color  # Use ranges for mapping

        return water_map, land_map

    @staticmethod
    def generate_clouds():
        """
        Generates a cloud map.
        """
        # Define cloud map ranges and colors
        cloud_map = {
            (0, 0.2): (255, 255, 255, 160),  # Light clouds
            (0.2, 0.4): (220, 220, 255, 150),  # Slightly darker clouds
            (0.4, 0.6): (200, 200, 200, 140),  # Gray clouds
            (0.6, 0.8): (180, 180, 255, 130),  # Darker clouds
            (0.8, 1.0): (255, 255, 255, 100),  # Almost transparent
        }
        return cloud_map

# Example usage (not necessary when importing)
if __name__ == "__main__":
    planet_type = PlanetType()
    random_planet = planet_type.generate_random_planet_type()
    print("Randomly generated planet configuration:")
    print(random_planet)

    # Generate colors based on the random planet configuration
    avg_temperature = 15  # Example temperature, adjust as needed
    water_map, land_map = BodyGen.generate_colors(avg_temperature, random_planet)
    print("Generated water map:", water_map)
    print("Generated land map:", land_map)