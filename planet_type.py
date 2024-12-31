import random

class PlanetType:
    # Biome Colors
    # Water layers
    __deep_ocean = (0, 0, 70)
    __warm_deep_ocean = (0, 160, 190)
    __ocean = (0, 0, 80)
    __warm_ocean = (0, 170, 210)
    __coastal = (0, 10, 90)
    __warm_coastal = (0, 190, 230)
    __coast = (190, 180, 70)
    __cold_coast = (80, 75, 50)
    __frozen_coast = (190, 255, 250)
    __frozen = (225, 255, 245)
    __frozen2 = (225, 220, 245)
    __frozen3 = (210, 230, 230)
    
    # Vegetation layers
    __m_tundra = (105, 90, 90)
    __k_tundra = (140, 110, 80)
    __g_tundra = (0, 100, 90)
    __m_taiga = (56, 20, 20)
    __k_taiga = (70, 40, 0)
    __g_taiga = (0, 80, 60)
    __m_continental_forest = (105, 10, 20)
    __k_continental_forest = (110, 55, 0)
    __g_continental_forest = (0, 105, 60)
    __m_continental_steppe = (135, 20, 25)
    __k_continental_steppe = (130, 60, 0)
    __g_continental_steppe = (90, 180, 80)
    __m_mediterranean = (150, 35, 25)
    __k_mediterranean = (130, 50, 10)
    __g_mediterranean = (135, 200, 20)
    __m_subtropical = (70, 2, 30)
    __k_subtropical = (150, 50, 0)
    __g_subtropical = (50, 110, 20)
    __m_tropical = (110, 10, 50)
    __k_tropical = (175, 65, 10)
    __g_tropical = (20, 80, 20)
    __m_savanna = (130, 70, 50)
    __k_savanna = (120, 80, 15)
    __g_savanna = (115, 130, 40)
    
    # Land layers
    __semi_arid = (190, 140, 36)
    __arid_desert = (174, 155, 36)
    __snow_biome = (255, 255, 255)
    __mountains = (20, 30, 45)
    
    # Clouds
    __cloud_body = (255, 255, 255, 160)
    __cloud_shape = (220, 255, 255, 150)
    
    clouds = [
        (255, 255, 255, 190),
        (255, 255, 235, 200),
    ]
    
    # Water maps
    standard_ocean = [
        __deep_ocean,
        __ocean,
        __coastal,
        __coast,
    ]

    frozen_ocean = [
        __frozen,
        __frozen2,
        __frozen3,
        __frozen_coast,
    ]

    warm_ocean = [
        __warm_deep_ocean,
        __warm_ocean,
        __warm_coastal,
        __coast,
    ]

    # Land Maps
    m_boreal_world = [
        __frozen,
        __m_taiga,
        __m_tundra,
        __m_taiga,
        __m_tundra,
        __mountains,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
    ]

    k_boreal_world = [
        __frozen,
        __k_taiga,
        __k_tundra,
        __k_taiga,
        __k_tundra,
        __mountains,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
    ]

    g_boreal_world = [
        __frozen,
        __g_taiga,
        __g_tundra,
        __g_taiga,
        __g_tundra,
        __mountains,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
        __frozen,
    ]

    m_cold_temperate_world = [
        __m_mediterranean,
        __m_savanna,
        __m_continental_steppe,
        __m_continental_forest,
        __m_continental_forest,
        __m_taiga,
        __m_taiga,
        __m_taiga,
        __m_tundra,
        __m_tundra,
        __mountains,
        __frozen,
    ]

    k_cold_temperate_world = [
        __k_mediterranean,
        __k_savanna,
        __k_continental_steppe,
        __k_continental_forest,
        __k_continental_forest,
        __k_taiga,
        __k_taiga,
        __k_taiga,
        __k_tundra,
        __k_tundra,
        __mountains,
        __frozen,
    ]

    g_cold_temperate_world = [
        __g_mediterranean,
        __g_savanna,
        __g_continental_steppe,
        __g_continental_forest,
        __g_continental_forest,
        __g_taiga,
        __g_taiga,
        __g_taiga,
        __g_tundra,
        __g_tundra,
        __mountains,
        __frozen,
    ]

    m_temperate_world = [
        __m_tropical,
        __arid_desert,
        __semi_arid,
        __m_subtropical,
        __m_savanna,
        __m_mediterranean,
        __m_continental_steppe,
        __m_continental_forest,
        __m_taiga,
        __m_tundra,
        __mountains,
        __frozen,
    ]

    k_temperate_world = [
        __k_tropical,
        __arid_desert,
        __semi_arid,
        __k_subtropical,
        __k_savanna,
        __k_mediterranean,
        __k_continental_steppe,
        __k_continental_forest,
        __k_taiga,
        __k_tundra,
        __mountains,
        __frozen,
    ]

    g_temperate_world = [
        __g_tropical,
        __arid_desert,
        __semi_arid,
        __g_subtropical,
        __g_savanna,
        __g_mediterranean,
        __g_continental_steppe,
        __g_continental_forest,
        __g_taiga,
        __g_tundra,
        __mountains,
        __frozen,
    ]

    def generate_random_planet_type(self):
        """Randomly generates a planet type configuration."""
        selected_ocean = random.choice([self.standard_ocean, self.frozen_ocean, self.warm_ocean])
        selected_land = random.choice([
            self.m_boreal_world, self.k_boreal_world, self.g_boreal_world,
            self.m_cold_temperate_world, self.k_cold_temperate_world, self.g_cold_temperate_world,
            self.m_temperate_world, self.k_temperate_world, self.g_temperate_world
        ])
        selected_clouds = random.choice(self.clouds)

        return {
            "ocean": selected_ocean,
            "land": selected_land,
            "clouds": selected_clouds,
        }

# Example usage:
if __name__ == "__main__":
    planet_type = PlanetType()
    random_planet = planet_type.generate_random_planet_type()
    print("Randomly generated planet configuration:")
    print(random_planet)