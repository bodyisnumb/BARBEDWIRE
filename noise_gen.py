import random
import noise
import numpy as np

class NoiseGen:
    def __init__(self):
        self.avg_temperature = None  # Initialize avg_temperature

    @staticmethod
    def generate_clouds_noise(resolution):
        center = resolution // 2
        scale = 0.3 * resolution
        octaves = 6
        persistence = 0.45
        lacunarity = 2.0
        seed = random.randint(0, 100)
        noise_array = np.zeros((resolution, resolution))
        for y in range(resolution):
            for x in range(resolution):
                squared_distance_to_center = (x - center) ** 2 + (y - center) ** 2
                if squared_distance_to_center <= center ** 2:
                    noise_value = noise.pnoise2(x / scale,
                                                y / scale,
                                                octaves=octaves,
                                                persistence=persistence,
                                                lacunarity=lacunarity,
                                                repeatx=resolution,
                                                repeaty=resolution,
                                                base=seed)
                    noise_array[y, x] = noise_value

        normalized_cloud_noise = (noise_array - np.min(noise_array)) / \
                                 (np.max(noise_array) - np.min(noise_array))
        return normalized_cloud_noise

    def generate_noise(self, resolution):  # Removed temperature argument
        center = resolution // 2
        scale = 0.2 * resolution
        octaves = 8
        persistence = 0.55
        lacunarity = 2.0
        seed = random.randint(0, 100)

        noise_array = np.zeros((resolution, resolution))
        water_noise_array = np.zeros((resolution, resolution))
        land_noise_array = np.zeros((resolution, resolution))

        # Use self.avg_temperature from the PlanetGeneratorApp instance
        sea_level = abs((1 / (1.6 * 10 ** 8)) * self.avg_temperature * (self.avg_temperature + 30) *
                        (self.avg_temperature - 60) * (self.avg_temperature - 50) * (self.avg_temperature + 60))

        for y in range(resolution):
            for x in range(resolution):
                squared_distance_to_center = (x - center) ** 2 + (y - center) ** 2
                if squared_distance_to_center <= center ** 2:
                    noise_value = noise.pnoise2(x / scale,
                                                y / scale,
                                                octaves=octaves,
                                                persistence=persistence,
                                                lacunarity=lacunarity,
                                                repeatx=resolution,
                                                repeaty=resolution,
                                                base=seed)
                    noise_array[y, x] = noise_value

        normalized_noise = (noise_array - np.min(noise_array)) / \
                           (np.max(noise_array) - np.min(noise_array))

        background = normalized_noise[0, 0]
        for y in range(resolution):
            for x in range(resolution):
                if normalized_noise[y, x] == background:
                    normalized_noise[y, x] = -0.1

        for y in range(resolution):
            for x in range(resolution):
                if normalized_noise[y, x] <= sea_level:
                    water_noise_array[y, x] = normalized_noise[y, x]
                else:
                    land_noise_array[y, x] = normalized_noise[y, x]

        water_normalized = (water_noise_array - np.min(water_noise_array)) / \
                           (np.max(water_noise_array) - np.min(water_noise_array))
        land_normalized = (land_noise_array - np.min(land_noise_array)) / \
                          (np.max(land_noise_array) - np.min(land_noise_array))

        for y in range(resolution):
            for x in range(resolution):
                if land_normalized[y, x] > 0:
                    z = abs(y - center)  # Distance from center
                    land_normalized[y, x] += (z/(resolution//2)) - 3*abs(self.avg_temperature)/100  # Use instance avg_temperature
                    land_normalized[y, x] = min(0.98, land_normalized[y, x])
                    land_normalized[y, x] = max(0.1, land_normalized[y, x])

        return water_normalized, land_normalized

    def set_avg_temperature(self, temperature):
        self.avg_temperature = temperature  # Method to set the average temperature