from utils.database import get_db
from sqlalchemy import text


def get_employer_logo(id):
    db = get_db()
    
    # Check employers table for logo_url
    query = text("SELECT logo_url FROM employers WHERE employer_id = :id")
    result = db.execute_query(query, {'id': id})
    if result['success'] and result['output']:
        for row in result['output']:
            if row['logo_url']:
                return row['logo_url']
            return None


def get_employer_links(id):
    db = get_db()
    file_paths = {}
    query = text("SELECT business_permit_url, supporting_docs_urls, linkedin_profile, facebook_profile FROM employer_verification WHERE employer_id = :id")
    result = db.execute_query(query, {'id': id})
    if result['success'] and result['output']:
        for row in result['output']:
            if row['business_permit_url']:
                file_paths["business_permit"] = row['business_permit_url']
            if row['supporting_docs_urls']:
                 file_paths["supporting_docs"] = row['supporting_docs_urls']
            if row['linkedin_profile']:
                  file_paths["linkedin_profile"] = row['linkedin_profile']
            if row['facebook_profile']:
                file_paths["facebook_profile"] = row['facebook_profile']
    return file_paths


def get_seeker_links(id):
    db = get_db()
    file_paths = {}
    query = text("SELECT resume, linkedin, github, twitter FROM seeker_profiles WHERE user_id = :id")
    result = db.execute_query(query, {'id': id})
    if result['success'] and result['output']:
        for row in result['output']:
           
            if row['resume']:
                 file_paths["resume"] = row['resume']
                 
            if row['linkedin']:
                 file_paths["linkedin"] =row['linkedin']
            if row['github']:
                file_paths["github"] = row['github']
            if row['twitter']:
                file_paths["twitter"] = row['twitter']
    return file_paths


