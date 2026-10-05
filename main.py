import datetime
from locator import ConstellationLocator
from config import COUNTRY_GEO_DB

def run_tracker():
    print("=== STARGAZER CONSTELLATION LOCATOR ===")
    
    engine = ConstellationLocator()
    
    print("\nAvailable Countries:")
    for country in COUNTRY_GEO_DB.keys():
        print(f" - {country}")
        
    target_country = input("\nEnter country name: ").strip()
    
    if target_country not in COUNTRY_GEO_DB:
        print("Error: Selected country is not in the database.")
        return
        
    try:
        results, exact_time = engine.get_visible_constellations(target_country)
        
        print(f"\nVisible Constellations ({exact_time.utc_strftime()} UTC):")
        print("-" * 65)
        print(f"{'Constellation':<15} | {'Altitude (Elevation)':<20} | {'Azimuth (Direction)':<15}")
        print("-" * 65)
        
        sorted_constellations = sorted(results.items(), key=lambda x: x['highest_altitude'], reverse=True)
        
        for code, metrics in sorted_constellations:
            print(f"{code:<15} | {metrics['highest_altitude']:>6.2f}° degrees       | {metrics['sample_azimuth']:>6.2f}° degrees")
            
        print("-" * 65)
        print(f"Total visible constellations: {len(sorted_constellations)}")
        
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    run_tracker()
