# Geo API Tests

This directory contains tests for the geographical API endpoints in the Flask application.

## Running the Tests

To run the tests, navigate to the project root directory and use the following command:

```
python -m unittest discover tests
```

Or to run a specific test file:

```
python -m unittest tests.test_geo
```

## Test Coverage

The tests cover the following functionality:

### Helper Functions
- `load_data`: Tests loading valid and invalid JSON files
- `filter_data`: Tests filtering data with keywords
- `paginate_data`: Tests pagination functionality with various parameters
- `find_by_code`: Tests finding items by their code

### API Endpoints
- `/geo`: Tests the home endpoint
- `/api/regions`: Tests listing regions with pagination and filtering
- `/api/regions/<code>`: Tests retrieving a specific region by code
- `/api/provinces`: Tests listing provinces with pagination and filtering by region code
- `/api/provinces/<code>`: Tests retrieving a specific province by code
- `/api/citi_muni`: Tests listing municipalities with pagination and filtering by province/region code
- `/api/citi_muni/<code>`: Tests retrieving a specific municipality by code

## Adding More Tests

To add more tests, create a new test file in this directory following the pattern `test_*.py`.