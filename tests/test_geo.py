import unittest
import json
import os
import sys
from flask import Flask
from routes.geo import geo, load_data, filter_data, paginate_data, find_by_code

# Add the parent directory to sys.path to import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGeoRoutes(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.register_blueprint(geo)
        self.client = self.app.test_client()
        
        # Define file paths for test data
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.region_file = os.path.join(self.base_dir, 'files', 'geo', 'region.json')
        self.province_file = os.path.join(self.base_dir, 'files', 'geo', 'province.json')
        self.municipality_file = os.path.join(self.base_dir, 'files', 'geo', 'municipality.json')
        self.barangay_file = os.path.join(self.base_dir, 'files', 'geo', 'baranggay.json')
        
        # Load test data
        self.regions = load_data(self.region_file)
        self.provinces = load_data(self.province_file)
        self.municipalities = load_data(self.municipality_file)
        self.barangays = load_data(self.barangay_file)
    
    # Helper function tests
    def test_load_data(self):
        # Test loading valid data
        regions = load_data(self.region_file)
        self.assertIsInstance(regions, list)
        self.assertTrue(len(regions) > 0)
        
        # Test loading invalid file
        invalid_data = load_data('nonexistent_file.json')
        self.assertEqual(invalid_data, [])
    
    def test_filter_data(self):
        # Test filtering with a keyword
        if self.regions:
            keyword = self.regions[0]['name'].lower()[0:3]  # Use first 3 chars of first region name
            filtered = filter_data(self.regions, keyword)
            self.assertTrue(len(filtered) > 0)
        
        # Test filtering with no keyword
        unfiltered = filter_data(self.regions, None)
        self.assertEqual(unfiltered, self.regions)
        
        # Test filtering with non-matching keyword
        non_matching = filter_data(self.regions, 'xyznonexistent')
        self.assertEqual(non_matching, [])
    
    def test_paginate_data(self):
        # Test basic pagination
        if len(self.regions) > 5:
            result = paginate_data(self.regions, 1, 5)
            self.assertEqual(len(result['data']), 5)
            self.assertEqual(result['meta']['page'], 1)
            self.assertEqual(result['meta']['per_page'], 5)
            
            # Test second page
            result = paginate_data(self.regions, 2, 5)
            self.assertEqual(result['meta']['page'], 2)
            
            # Test invalid page number
            result = paginate_data(self.regions, -1, 5)
            self.assertEqual(result['meta']['page'], 1)  # Should default to page 1
            
            # Test invalid per_page
            result = paginate_data(self.regions, 1, 0)
            self.assertEqual(result['meta']['per_page'], 10)  # Should default to 10
            
            # Test large per_page
            result = paginate_data(self.regions, 1, 2000)
            self.assertEqual(result['meta']['per_page'], 10)  # Should default to 10
    
    def test_find_by_code(self):
        # Test finding an existing item
        if self.regions:
            first_region = self.regions[0]
            code = first_region.get('code') or first_region.get('psgc10DigitCode')
            if code:
                found = find_by_code(self.regions, code)
                self.assertEqual(found, first_region)
        
        # Test finding a non-existent item
        not_found = find_by_code(self.regions, 'nonexistent_code')
        self.assertIsNone(not_found)
    
    # API endpoint tests
    def test_geo_home(self):
        response = self.client.get('/geo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Geographical Information Page')
    
    # Region endpoint tests
    def test_get_regions(self):
        # Test basic regions endpoint
        response = self.client.get('/api/regions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
        self.assertIn('meta', data)
        
        # Test pagination
        response = self.client.get('/api/regions?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertLessEqual(len(data['data']), 5)
        
        # Test filtering
        if self.regions:
            keyword = self.regions[0]['name'].lower()[0:3]  # Use first 3 chars of first region name
            response = self.client.get(f'/api/regions?keyword={keyword}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(len(data['data']) > 0)
    
    def test_get_region_by_code(self):
        # Test getting a specific region
        if self.regions:
            first_region = self.regions[0]
            code = first_region.get('code') or first_region.get('psgc10DigitCode')
            if code:
                response = self.client.get(f'/api/regions/{code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertEqual(data, first_region)
        
        # Test getting a non-existent region
        response = self.client.get('/api/regions/nonexistent_code')
        self.assertEqual(response.status_code, 404)
    
    # Province endpoint tests
    def test_get_provinces(self):
        # Test basic provinces endpoint
        response = self.client.get('/api/provinces')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
        self.assertIn('meta', data)
        
        # Test pagination
        response = self.client.get('/api/provinces?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertLessEqual(len(data['data']), 5)
        
        # Test filtering by region code
        if self.provinces and len(self.provinces) > 0:
            region_code = self.provinces[0].get('regionCode')
            if region_code:
                response = self.client.get(f'/api/provinces?region_code={region_code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                if len(data['data']) > 0:
                    self.assertEqual(data['data'][0]['regionCode'], region_code)
        
        # Test filtering by keyword
        if self.provinces and len(self.provinces) > 0:
            keyword = self.provinces[0]['name'].lower()[0:3]  # Use first 3 chars of first province name
            response = self.client.get(f'/api/provinces?keyword={keyword}')
            self.assertEqual(response.status_code, 200)
    
    def test_get_province_by_code(self):
        # Test getting a specific province
        if self.provinces and len(self.provinces) > 0:
            first_province = self.provinces[0]
            code = first_province.get('code') or first_province.get('psgc10DigitCode')
            if code:
                response = self.client.get(f'/api/provinces/{code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertEqual(data, first_province)
        
        # Test getting a non-existent province
        response = self.client.get('/api/provinces/nonexistent_code')
        self.assertEqual(response.status_code, 404)
    
    # Municipality endpoint tests
    def test_get_municipalities(self):
        # Test basic municipalities endpoint
        response = self.client.get('/api/citi_muni')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
        self.assertIn('meta', data)
        
        # Test pagination
        response = self.client.get('/api/citi_muni?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertLessEqual(len(data['data']), 5)
        
        # Test filtering by province code
        if self.municipalities and len(self.municipalities) > 0:
            province_code = self.municipalities[0].get('provinceCode')
            if province_code:
                response = self.client.get(f'/api/citi_muni?province_code={province_code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                if len(data['data']) > 0:
                    self.assertEqual(data['data'][0]['provinceCode'], province_code)
        
        # Test filtering by region code
        if self.municipalities and len(self.municipalities) > 0:
            region_code = self.municipalities[0].get('regionCode')
            if region_code:
                response = self.client.get(f'/api/citi_muni?region_code={region_code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                if len(data['data']) > 0:
                    self.assertEqual(data['data'][0]['regionCode'], region_code)
    
    def test_get_municipality_by_code(self):
        # Test getting a specific municipality
        if self.municipalities and len(self.municipalities) > 0:
            first_municipality = self.municipalities[0]
            code = first_municipality.get('code') or first_municipality.get('psgc10DigitCode')
            if code:
                response = self.client.get(f'/api/citi_muni/{code}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertEqual(data, first_municipality)
        
        # Test getting a non-existent municipality
        response = self.client.get('/api/citi_muni/nonexistent_code')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()