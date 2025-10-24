#!/usr/bin/env python3
"""
Demo script for the Robotic Package Sorting System

This script demonstrates the functionality of the package sorting system
with various real-world examples.
"""

from package_sorter import sort, get_package_info


def demo_package_sorting():
    """Demonstrate the package sorting system with various examples."""
    
    print("Robotic Package Sorting System Demo")
    print("=" * 50)
    
    # Test cases with different scenarios
    test_cases = [
        # (width, height, length, mass, description)
        (30, 20, 10, 2, "Small electronics box"),
        (40, 30, 20, 5, "Medium clothing box"),
        (100, 100, 100, 10, "Exact volume threshold (1,000,000 cm³)"),
        (101, 100, 100, 10, "Just over volume threshold"),
        (150, 50, 50, 10, "Oversized but light item"),
        (50, 50, 50, 20, "Heavy but compact item"),
        (200, 100, 100, 25, "Both bulky and heavy (rejected)"),
        (120, 80, 60, 35, "Heavy appliance box"),
        (500, 10, 10, 100, "Long industrial pipe"),
        (0.1, 0.1, 0.1, 0.1, "Very small package"),
    ]
    
    for width, height, length, mass, description in test_cases:
        result = sort(width, height, length, mass)
        
        # Get detailed info for display
        info = get_package_info(width, height, length, mass)
        
        print(f"\nPackage: {description}")
        print(f"   Dimensions: {width} x {height} x {length} cm")
        print(f"   Volume: {info['volume_cm3']:,} cm3")
        print(f"   Mass: {mass} kg")
        print(f"   Classification: {'Bulky' if info['is_bulky'] else 'Not bulky'}, {'Heavy' if info['is_heavy'] else 'Not heavy'}")
        print(f"   Stack: {result}")
        
        # Add status for visual clarity
        if result == "STANDARD":
            print("   Status: Can be handled automatically")
        elif result == "SPECIAL":
            print("   Status: Requires special handling")
        elif result == "REJECTED":
            print("   Status: Package rejected - too large and heavy")
    
    print("\n" + "=" * 50)
    print("Summary:")
    
    # Count results
    results = [sort(w, h, l, m) for w, h, l, m, _ in test_cases]
    standard_count = results.count("STANDARD")
    special_count = results.count("SPECIAL")
    rejected_count = results.count("REJECTED")
    
    print(f"   Standard packages: {standard_count}")
    print(f"   Special packages: {special_count}")
    print(f"   Rejected packages: {rejected_count}")
    print(f"   Total packages: {len(test_cases)}")


def interactive_demo():
    """Interactive demo where users can input their own package dimensions."""
    
    print("\nInteractive Demo")
    print("=" * 30)
    print("Enter package dimensions to see how they would be sorted.")
    print("Press Enter with empty input to exit.")
    
    while True:
        try:
            print("\nEnter package dimensions:")
            width_input = input("Width (cm): ").strip()
            if not width_input:
                break
                
            height_input = input("Height (cm): ").strip()
            if not height_input:
                break
                
            length_input = input("Length (cm): ").strip()
            if not length_input:
                break
                
            mass_input = input("Mass (kg): ").strip()
            if not mass_input:
                break
            
            width = float(width_input)
            height = float(height_input)
            length = float(length_input)
            mass = float(mass_input)
            
            result = sort(width, height, length, mass)
            info = get_package_info(width, height, length, mass)
            
            print(f"\nPackage Analysis:")
            print(f"   Dimensions: {width} x {height} x {length} cm")
            print(f"   Volume: {info['volume_cm3']:,} cm3")
            print(f"   Mass: {mass} kg")
            print(f"   Classification: {'Bulky' if info['is_bulky'] else 'Not bulky'}, {'Heavy' if info['is_heavy'] else 'Not heavy'}")
            print(f"   Stack: {result}")
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    demo_package_sorting()
    interactive_demo()
