"""
Test suite for the package sorting system.

This module contains comprehensive tests to verify the correct behavior
of the package sorting function under various conditions.
"""

import pytest
from package_sorter import sort, get_package_info


class TestPackageSorting:
    """Test cases for package sorting functionality."""
    
    def test_standard_packages(self):
        """Test packages that should go to STANDARD stack."""
        # Small, light package
        assert sort(50, 50, 50, 10) == "STANDARD"
        # Medium package, light weight (just under volume threshold)
        assert sort(99, 100, 100, 15) == "STANDARD"
        # Large package, light weight
        assert sort(99, 99, 99, 19) == "STANDARD"
        
    def test_special_bulky_packages(self):
        """Test packages that are bulky (but not heavy) - should go to SPECIAL."""
        # Bulky by volume
        assert sort(100, 100, 100, 15) == "SPECIAL"  # 1,000,000 cm³ exactly
        assert sort(101, 100, 100, 15) == "SPECIAL"  # 1,010,000 cm³ > 1,000,000
        
        # Bulky by dimension
        assert sort(150, 50, 50, 15) == "SPECIAL"  # width >= 150
        assert sort(50, 150, 50, 15) == "SPECIAL"  # height >= 150
        assert sort(50, 50, 150, 15) == "SPECIAL"  # length >= 150
        
        # Bulky by volume (large cube)
        assert sort(149, 149, 149, 19) == "SPECIAL"  # 3,307,951 cm³ > 1,000,000
        
    def test_special_heavy_packages(self):
        """Test packages that are heavy (but not bulky) - should go to SPECIAL."""
        # Heavy packages with normal dimensions
        assert sort(50, 50, 50, 20) == "SPECIAL"  # mass exactly 20 kg
        assert sort(50, 50, 50, 25) == "SPECIAL"  # mass > 20 kg
        assert sort(99, 99, 99, 25) == "SPECIAL"  # large but not bulky
        
    def test_rejected_packages(self):
        """Test packages that are both bulky and heavy - should be REJECTED."""
        # Bulky by volume and heavy
        assert sort(200, 100, 100, 25) == "REJECTED"  # 2,000,000 cm³, 25 kg
        assert sort(100, 100, 101, 20) == "REJECTED"  # 1,010,000 cm³, 20 kg
        
        # Bulky by dimension and heavy
        assert sort(150, 50, 50, 20) == "REJECTED"  # width >= 150, 20 kg
        assert sort(50, 150, 50, 25) == "REJECTED"  # height >= 150, 25 kg
        assert sort(50, 50, 150, 30) == "REJECTED"  # length >= 150, 30 kg
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Exact volume threshold
        assert sort(100, 100, 100, 10) == "SPECIAL"  # 1,000,000 cm³ exactly
        assert sort(100, 100, 100.1, 10) == "SPECIAL"  # slightly over volume threshold
        
        # Exact dimension threshold
        assert sort(149.9, 50, 50, 10) == "STANDARD"  # just under dimension threshold
        assert sort(150, 50, 50, 10) == "SPECIAL"  # exactly at dimension threshold
        
        # Exact mass threshold
        assert sort(50, 50, 50, 19.9) == "STANDARD"  # just under mass threshold
        assert sort(50, 50, 50, 20) == "SPECIAL"  # exactly at mass threshold
        
    def test_zero_values(self):
        """Test packages with zero dimensions or mass."""
        # Zero volume package
        assert sort(0, 50, 50, 10) == "STANDARD"
        # Zero mass package
        assert sort(50, 50, 50, 0) == "STANDARD"
        # Both zero volume and mass
        assert sort(0, 0, 0, 0) == "STANDARD"
        
    def test_very_small_values(self):
        """Test packages with very small dimensions and mass."""
        assert sort(0.1, 0.1, 0.1, 0.1) == "STANDARD"
        assert sort(1, 1, 1, 1) == "STANDARD"
        
    def test_very_large_values(self):
        """Test packages with very large dimensions and mass."""
        assert sort(1000, 1000, 1000, 1000) == "REJECTED"
        assert sort(200, 200, 200, 100) == "REJECTED"
        
    def test_input_validation(self):
        """Test input validation and error handling."""
        # Negative values should raise ValueError
        with pytest.raises(ValueError):
            sort(-1, 50, 50, 10)
        with pytest.raises(ValueError):
            sort(50, -1, 50, 10)
        with pytest.raises(ValueError):
            sort(50, 50, -1, 10)
        with pytest.raises(ValueError):
            sort(50, 50, 50, -1)
            
        # Non-numeric values should raise ValueError
        with pytest.raises(ValueError):
            sort("50", 50, 50, 10)
        with pytest.raises(ValueError):
            sort(50, [50], 50, 10)
        with pytest.raises(ValueError):
            sort(50, 50, 50, None)
            
    def test_get_package_info(self):
        """Test the helper function that provides detailed package information."""
        info = get_package_info(150, 100, 100, 25)
        
        assert info["dimensions"] == {"width": 150, "height": 100, "length": 100}
        assert info["volume_cm3"] == 1_500_000
        assert info["mass_kg"] == 25
        assert info["is_bulky"] is True
        assert info["is_heavy"] is True
        assert info["stack"] == "REJECTED"


class TestIntegrationScenarios:
    """Integration test scenarios that might occur in real warehouse operations."""
    
    def test_typical_ecommerce_packages(self):
        """Test typical e-commerce package sizes."""
        # Small electronics box
        assert sort(30, 20, 10, 2) == "STANDARD"
        
        # Medium clothing box
        assert sort(40, 30, 20, 5) == "STANDARD"
        
        # Large appliance box
        assert sort(120, 80, 60, 35) == "SPECIAL"
        
        # Oversized but light item
        assert sort(200, 50, 50, 10) == "SPECIAL"
        
        # Heavy but compact item
        assert sort(50, 50, 50, 50) == "SPECIAL"
        
    def test_industrial_packages(self):
        """Test industrial-sized packages."""
        # Large machinery part
        assert sort(300, 200, 150, 500) == "REJECTED"
        
        # Long pipe
        assert sort(500, 10, 10, 100) == "REJECTED"
        
        # Heavy equipment
        assert sort(100, 100, 100, 100) == "REJECTED"


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
