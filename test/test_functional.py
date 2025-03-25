"""
Test functional implementation of the timestamp operations.
"""
import pytest
from datetime import datetime
import pytz
from current_timezone_timestamp_converter import get_current_utc_time, get_current_time_in_timezone, convert_timezone, format_timestamp, calculate_time_difference
from test.TestUtils import TestUtils

class TestFunctional:
    """Test cases for timestamp processor functionality."""
    
    def test_get_current_utc_time(self):
        """Test current UTC time retrieval functionality."""
        try:
            # Test function returns a datetime with timezone
            utc_time = get_current_utc_time()
            assert isinstance(utc_time, datetime), "Should return a datetime object"
            assert utc_time.tzinfo is not None, "Should include timezone information"
            assert "UTC" in str(utc_time.tzinfo), "Timezone should be UTC"
            
            TestUtils.yakshaAssert("test_get_current_utc_time", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_get_current_utc_time", False, "functional")
            raise e
    
    def test_get_current_time_in_timezone(self):
        """Test current time in timezone functionality."""
        try:
            # Test with specific timezone
            ny_time = get_current_time_in_timezone("America/New_York")
            assert isinstance(ny_time, datetime), "Should return a datetime object"
            assert ny_time.tzinfo is not None, "Should include timezone information"
            assert "New_York" in str(ny_time.tzinfo), "Should have correct timezone"
            
            # Test with another timezone
            tokyo_time = get_current_time_in_timezone("Asia/Tokyo")
            assert isinstance(tokyo_time, datetime), "Should return a datetime object"
            assert tokyo_time.tzinfo is not None, "Should include timezone information"
            assert "Tokyo" in str(tokyo_time.tzinfo), "Should have correct timezone"
            
            # Test time difference logic
            # This checks that the function correctly applies timezone offsets
            hour_diff = (tokyo_time.hour - ny_time.hour) % 24
            assert hour_diff > 0, "Tokyo should be ahead of New York"
            
            # Test with invalid timezone
            invalid_time = get_current_time_in_timezone("Invalid/Zone")
            assert invalid_time is None, "Should handle invalid timezone gracefully"
            
            TestUtils.yakshaAssert("test_get_current_time_in_timezone", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_get_current_time_in_timezone", False, "functional")
            raise e
    
    def test_convert_timezone(self):
        """Test timezone conversion functionality."""
        try:
            # Create a datetime with timezone info
            ny_tz = pytz.timezone("America/New_York")
            dt = datetime(2025, 3, 19, 14, 0).replace(tzinfo=ny_tz)
            
            # Test conversion to another timezone
            tokyo_time = convert_timezone(dt, "Asia/Tokyo")
            assert isinstance(tokyo_time, datetime), "Should return a datetime object"
            assert "Tokyo" in str(tokyo_time.tzinfo), "Should convert to Tokyo timezone"
            
            # Test that the time is correctly shifted
            # New York to Tokyo is approximately +14 hours
            # But we need to account for day changes, so use modulo
            hour_diff = (tokyo_time.hour - dt.hour) % 24
            assert 13 <= hour_diff <= 15, "Should shift time correctly between NY and Tokyo"
            
            # Test conversion to UTC
            utc_time = convert_timezone(dt, "UTC")
            assert "UTC" in str(utc_time.tzinfo), "Should convert to UTC"
            # NY to UTC is +5 hours (or +4 during DST)
            hour_diff = (utc_time.hour - dt.hour) % 24
            assert 4 <= hour_diff <= 5, "Should shift time correctly between NY and UTC"
            
            # Test with None input
            none_result = convert_timezone(None, "UTC")
            assert none_result is None, "Should handle None input gracefully"
            
            # Test with naive datetime
            naive_dt = datetime(2025, 3, 19, 14, 0)  # No tzinfo
            naive_result = convert_timezone(naive_dt, "UTC")
            assert naive_result is None, "Should handle naive datetime gracefully"
            
            TestUtils.yakshaAssert("test_convert_timezone", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_convert_timezone", False, "functional")
            raise e
    
    def test_format_timestamp(self):
        """Test timestamp formatting functionality."""
        try:
            # Create a datetime with timezone info
            dt = datetime(2025, 3, 19, 14, 30, tzinfo=pytz.UTC)
            
            # Test default format
            default_format = format_timestamp(dt, "%Y-%m-%d %H:%M:%S %Z")
            assert "2025-03-19" in default_format, "Should include date in format"
            assert "14:30:00" in default_format, "Should include time in format"
            assert "UTC" in default_format, "Should include timezone in format"
            
            # Test custom format for US style
            us_format = format_timestamp(dt, "%B %d, %Y %I:%M %p %Z")
            assert "March 19, 2025" in us_format, "Should format date in US style"
            assert "02:30 PM" in us_format, "Should format time in 12-hour format"
            
            # Test custom format for UK style
            uk_format = format_timestamp(dt, "%d %B %Y %H:%M %Z")
            assert "19 March 2025" in uk_format, "Should format date in UK style"
            assert "14:30" in uk_format, "Should format time in 24-hour format"
            
            # Test with None input
            none_result = format_timestamp(None, "%Y-%m-%d")
            assert none_result is None, "Should handle None input gracefully"
            
            # Test with invalid format string
            invalid_format = format_timestamp(dt, "%Q")  # Invalid directive
            assert invalid_format is None, "Should handle invalid format gracefully"
            
            TestUtils.yakshaAssert("test_format_timestamp", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_format_timestamp", False, "functional")
            raise e
    
    def test_calculate_time_difference(self):
        """Test time difference calculation functionality."""
        try:
            # Test time difference between New York and Tokyo
            diff_ny_tokyo = calculate_time_difference("America/New_York", "Asia/Tokyo")
            assert isinstance(diff_ny_tokyo, dict), "Should return a dictionary"
            assert "hours" in diff_ny_tokyo, "Should include hours in result"
            assert "minutes" in diff_ny_tokyo, "Should include minutes in result"
            assert diff_ny_tokyo["hours"] >= 13, "NY to Tokyo should be about +14 hours"
            
            # Test time difference between London and Sydney
            diff_london_sydney = calculate_time_difference("Europe/London", "Australia/Sydney")
            assert isinstance(diff_london_sydney, dict), "Should return a dictionary"
            assert diff_london_sydney["hours"] >= 9, "London to Sydney should be about +10-11 hours"
            
            # Test time difference between same timezone
            same_tz = calculate_time_difference("UTC", "UTC")
            assert same_tz["hours"] == 0, "Same timezone should have 0 hour difference"
            assert same_tz["minutes"] == 0, "Same timezone should have 0 minute difference"
            
            # Test with invalid timezones
            invalid_diff = calculate_time_difference("Invalid/Zone", "UTC")
            assert invalid_diff is None, "Should handle invalid timezone gracefully"
            
            # Test with non-string inputs
            non_string_diff = calculate_time_difference(123, "UTC")
            assert non_string_diff is None, "Should handle non-string input gracefully"
            
            TestUtils.yakshaAssert("test_calculate_time_difference", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_calculate_time_difference", False, "functional")
            raise e
    
    def test_main_function_exists(self):
        """Test that the main function exists and runs without errors."""
        try:
            # We can't easily test the interactive main function directly
            # But we can import it to verify it exists
            from current_timezone_timestamp_converter import main
            assert callable(main), "main function should be callable"
            
            TestUtils.yakshaAssert("test_main_function_exists", True, "functional")
        except ImportError:
            TestUtils.yakshaAssert("test_main_function_exists", False, "functional")
            raise Exception("main function is not defined")
        except Exception as e:
            TestUtils.yakshaAssert("test_main_function_exists", False, "functional")
            raise e