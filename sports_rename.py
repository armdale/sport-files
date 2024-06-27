import json
import os
import re
import sys

LEAGUE_MAPPINGS_FILE = ''

def sport_file_link(source_file, target_dir):
    print(f'Processing file link from {source_file} to {target_dir}...')

    # get the filename from the full path
    base_path, source_filename = os.path.split(source_file)

    # parse the filename
    print(f'Parsing filename {source_filename}')
    with open(LEAGUE_MAPPINGS_FILE) as fd:
        leagues_mapping = json.load(fd)
    parsed_filename = parse_sport_file(source_filename, leagues_mapping)

    target_file_path = os.path.join(target_dir, parsed_filename)

    # link the file
    print(f'Linking source file {source_file} to {target_file_path}')
    link_file(source_file, target_file_path)

def parse_sport_file(filename, leagues_mapping):
    league = parse_league(filename, leagues_mapping)

    # get the season
    season = parse_season(filename)

    parsed_filename = os.path.join(
        league,
        season,
        filename
    )

    return parsed_filename

def parse_league(filename, leagues_mapping):
    # get the sport league. Go through the leagues and look for a match
    
    # do first pass seeing if the league matches
    for _league, league_mappings in leagues_mapping.items():
        if clean_string(_league) in clean_string(filename):
            league = _league
            break

    if league: 
        return league
    
    # second pass looking at the mapped names
    for _league, league_mappings in leagues_mapping.items():
        for league_mapping in league_mappings:
            if clean_string(league_mapping) in clean_string(filename):
                league = _league

    return league or None

def parse_season(filename):
    year_matches = re.findall(r'(\d{4})', filename)
    year = year_matches[0]
    return year

def clean_string(s):
    cleaned = re.sub(r'[^\w\s]','',s)
    cleaned = re.sub(r"\s+", '', cleaned)
    cleaned = cleaned.strip().lower()
    return cleaned


def link_file(source_file, target_file):
    target_path, target_filename = os.path.split(target_file)

    # create the target dirs if they don't exist
    os.makedirs(target_path, exist_ok=True)

    # link the file to the target
    os.link(source_file, target_file)

if __name__ == "__main__":
    source_file = sys.argv[1]
    target_dir = sys.argv[2] 
    sport_file_link(source_file, target_dir)
