from flask import Blueprint, jsonify, request, abort
import json
import os
from math import ceil

# Create a Blueprint
geo = Blueprint('geo', __name__)

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGION_FILE = os.path.join(BASE_DIR, 'files', 'geo', 'region.json')
PROVINCE_FILE = os.path.join(BASE_DIR, 'files', 'geo', 'province.json')
MUNICIPALITY_FILE = os.path.join(BASE_DIR, 'files', 'geo', 'municipality.json')
BARANGAY_FILE = os.path.join(BASE_DIR, 'files', 'geo', 'baranggay.json')

# Helper functions
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return []

def paginate_data(data, page, per_page):
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 10
        
        # Ensure valid pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 1000:
            per_page = 10
            
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = data[start_idx:end_idx]
        total_items = len(data)
        total_pages = ceil(total_items / per_page)
        
        return {
            "data": paginated_data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "page_count": len(paginated_data),
                "total_count": total_items,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        print(f"Error paginating data: {e}")
        return {"data": [], "meta": {}}

def filter_data(data, keyword):
    if not keyword:
        return data
    
    keyword = keyword.lower()
    filtered_data = []
    
    for item in data:
        # Check if keyword is in any string value of the item
        for value in item.values():
            if isinstance(value, str) and keyword in value.lower():
                filtered_data.append(item)
                break
    
    return filtered_data

def find_by_code(data, code):
    for item in data:
        if item.get('code') == code or item.get('psgc10DigitCode') == code:
            return item
    return None

# Define your routes using the Blueprint
@geo.route('/geo')
def home():
    return 'Geographical Information Page'

# Region endpoints
@geo.route('/api/regions')
def get_regions():
    try:
        regions = load_data(REGION_FILE)
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        per_page = request.args.get('per_page')
        
        # Filter data if keyword is provided
        if keyword:
            regions = filter_data(regions, keyword)
        
        # Paginate the results
        result = paginate_data(regions, page, per_page)
        
        return jsonify(result), 200
    except Exception as e:
        return str(e), 500

@geo.route('/api/regions/<string:psgc_code>')
def get_region(psgc_code):
    try:
        regions = load_data(REGION_FILE)
        region = find_by_code(regions, psgc_code)
        
        if not region:
            return "Region not found", 404
        
        return jsonify(region), 200
    except Exception as e:
        return str(e), 500

# Province endpoints
@geo.route('/api/provinces')
def get_provinces():
    try:
        provinces = load_data(PROVINCE_FILE)
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        per_page = request.args.get('per_page')
        region_code = request.args.get('region_code')
        
        # Filter by region code if provided
        if region_code:
            provinces = [p for p in provinces if p.get('regionCode') == region_code]
        
        # Filter data if keyword is provided
        if keyword:
            provinces = filter_data(provinces, keyword)
        
        # Paginate the results
        result = paginate_data(provinces, page, per_page)
        
        return jsonify(result), 200
    except Exception as e:
        return str(e), 500

@geo.route('/api/provinces/<string:psgc_code>')
def get_province(psgc_code):
    try:
        provinces = load_data(PROVINCE_FILE)
        province = find_by_code(provinces, psgc_code)
        
        if not province:
            return "Province not found", 404
        
        return jsonify(province), 200
    except Exception as e:
        return str(e), 500

# City/Municipality endpoints
@geo.route('/api/citi_muni')
def get_cities_municipalities():
    try:
        municipalities = load_data(MUNICIPALITY_FILE)
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        per_page = request.args.get('per_page')
        province_code = request.args.get('province_code')
        region_code = request.args.get('region_code')
        
        # Filter by province code if provided
        if province_code:
            municipalities = [m for m in municipalities if m.get('provinceCode') == province_code]
        
        # Filter by region code if provided
        if region_code:
            municipalities = [m for m in municipalities if m.get('regionCode') == region_code]
        
        # Filter data if keyword is provided
        if keyword:
            municipalities = filter_data(municipalities, keyword)
        
        # Paginate the results
        result = paginate_data(municipalities, page, per_page)
        
        return jsonify(result), 200
    except Exception as e:
        return str(e), 500

@geo.route('/api/citi_muni/<string:psgc_code>')
def get_city_municipality(psgc_code):
    try:
        municipalities = load_data(MUNICIPALITY_FILE)
        municipality = find_by_code(municipalities, psgc_code)
        
        if not municipality:
            return "City/Municipality not found", 404
        
        return jsonify(municipality), 200
    except Exception as e:
        return str(e), 500