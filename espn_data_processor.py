#!/usr/bin/env python3
"""
ESPN NFL API Data Processor
Converts ESPN NFL API JSON response(s) into normalized CSV files for data warehouse/analytics use

Multi-Week Processing Support:
- Process single JSON files (original behavior)
- Process multiple specific JSON files
- Process all JSON files in a directory
- Automatically appends data to existing CSV files instead of overwriting
- Maintains unique lookup data across all processed weeks
"""

import json
import csv
import os
import glob
from datetime import datetime
from typing import Dict, List, Set, Any, Optional, Union

class ESPNDataProcessor:
    def __init__(self, json_input: Union[str, List[str]], output_dir: str = "csv_output"):
        """Initialize the processor with input file(s) and output directory
        
        Args:
            json_input: Either a single JSON file path, a list of JSON file paths, 
                       or a directory path containing multiple JSON files
            output_dir: Directory where CSV files will be written
        """
        self.json_files = self._resolve_json_files(json_input)
        self.output_dir = output_dir
        self.data: Dict[str, Any] = {}
        
        # Create output directory if it doesn't exist
        if os.path.exists(output_dir):
            # Backup existing directory if it has data
            os.rename(output_dir, output_dir + datetime.now().strftime("%Y%m%d%H%M%S"))
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize data containers
        self.leagues = []
        self.teams = []
        self.venues = []
        self.players = []
        self.positions = []
        self.season_types = []
        self.game_status_types = []
        self.games = []
        self.competitions = []
        self.team_game_stats = []
        self.player_game_leaders = []
        self.game_broadcasts = []
        self.team_records = []
        
        # Sets to track unique items and avoid duplicates
        self.team_ids = set()
        self.league_ids = set()
        self.venue_ids = set()
        self.player_ids = set()
        self.position_names = set()
        self.status_type_ids = set()

    def _resolve_json_files(self, json_input: Union[str, List[str]]) -> List[str]:
        """Resolve input to a list of JSON file paths"""
        if isinstance(json_input, list):
            return json_input
        elif os.path.isdir(json_input):
            # If it's a directory, find all JSON files
            pattern = os.path.join(json_input, "*.json")
            return glob.glob(pattern)
        else:
            # Single file path
            return [json_input]

    def load_json_data(self, file_path: str):
        """Load JSON data from a specific file"""
        print(f"Loading data from {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        print("✓ JSON data loaded successfully")

    def process_multiple_files(self):
        """Process all JSON files and accumulate data"""
        print(f"Processing {len(self.json_files)} JSON files...")
        
        for i, file_path in enumerate(self.json_files, 1):
            print(f"\n--- Processing file {i}/{len(self.json_files)}: {os.path.basename(file_path)} ---")
            
            # Load current file's data
            self.load_json_data(file_path)
            
            # Extract all data from this file
            self.extract_leagues()
            self.extract_teams_from_events()
            self.extract_venues_from_events()
            self.extract_players_and_positions()
            self.extract_game_status_types()
            self.extract_games_and_competitions()
            
            # Clear transactional data for next file (but keep lookup data)
            self._clear_transactional_data()
            
        print(f"\n✓ Completed processing all {len(self.json_files)} files")

    def _clear_transactional_data(self):
        """Clear data that should be fresh for each file, keep lookup data accumulated"""
        # Clear fact/transactional tables but keep lookup tables (teams, venues, players, etc.)
        # This prevents duplicate game records while allowing new lookup entries
        pass  # Games, competitions, etc. are meant to accumulate across files

    def extract_leagues(self):
        """Extract league information"""
        print("Extracting league data...")
        
        for league in self.data.get('leagues', []):
            league_id = league.get('id')
            if league_id and league_id not in self.league_ids:
                self.league_ids.add(league_id)
                league_record = {
                    'league_id': league.get('id'),
                    'league_uid': league.get('uid'),
                    'name': league.get('name'),
                    'abbreviation': league.get('abbreviation'),
                    'slug': league.get('slug'),
                    'season_year': league.get('season', {}).get('year'),
                    'season_start_date': league.get('season', {}).get('startDate'),
                    'season_end_date': league.get('season', {}).get('endDate'),
                    'season_display_name': league.get('season', {}).get('displayName'),
                    'season_type_id': league.get('season', {}).get('type', {}).get('id'),
                    'season_type_name': league.get('season', {}).get('type', {}).get('name'),
                    'calendar_type': league.get('calendarType'),
                    'calendar_start_date': league.get('calendarStartDate'),
                    'calendar_end_date': league.get('calendarEndDate')
                }
                self.leagues.append(league_record)
        
        print(f"✓ Extracted {len(self.leagues)} league records")

    def extract_teams_from_events(self):
        """Extract team information from events"""
        print("Extracting team data from events...")
        
        for event in self.data.get('events', []):
            for competition in event.get('competitions', []):
                for competitor in competition.get('competitors', []):
                    team = competitor.get('team', {})
                    team_id = team.get('id')
                    
                    if team_id and team_id not in self.team_ids:
                        self.team_ids.add(team_id)
                        
                        team_record = {
                            'team_id': team_id,
                            'team_uid': team.get('uid'),
                            'location': team.get('location'),
                            'name': team.get('name'),
                            'abbreviation': team.get('abbreviation'),
                            'display_name': team.get('displayName'),
                            'short_display_name': team.get('shortDisplayName'),
                            'color': team.get('color'),
                            'alternate_color': team.get('alternateColor'),
                            'is_active': team.get('isActive'),
                            'venue_id': team.get('venue', {}).get('id'),
                            'logo_url': team.get('logo', '')
                        }
                        self.teams.append(team_record)
        
        print(f"✓ Extracted {len(self.teams)} unique teams")

    def extract_venues_from_events(self):
        """Extract venue information from events"""
        print("Extracting venue data...")
        
        for event in self.data.get('events', []):
            for competition in event.get('competitions', []):
                venue = competition.get('venue', {})
                venue_id = venue.get('id')
                
                if venue_id and venue_id not in self.venue_ids:
                    self.venue_ids.add(venue_id)
                    
                    address = venue.get('address', {})
                    venue_record = {
                        'venue_id': venue_id,
                        'full_name': venue.get('fullName'),
                        'city': address.get('city'),
                        'state': address.get('state'),
                        'country': address.get('country'),
                        'is_indoor': venue.get('indoor')
                    }
                    self.venues.append(venue_record)
        
        print(f"✓ Extracted {len(self.venues)} unique venues")

    def extract_players_and_positions(self):
        """Extract player and position information from game leaders"""
        print("Extracting player and position data...")
        
        for event in self.data.get('events', []):
            for competition in event.get('competitions', []):
                # Extract from competitors
                for competitor in competition.get('competitors', []):
                    for leader_category in competitor.get('leaders', []):
                        for leader in leader_category.get('leaders', []):
                            athlete = leader.get('athlete', {})
                            self._process_athlete(athlete)
                
                # Extract from competition leaders
                for leader_category in competition.get('leaders', []):
                    for leader in leader_category.get('leaders', []):
                        athlete = leader.get('athlete', {})
                        self._process_athlete(athlete)
        
        print(f"✓ Extracted {len(self.players)} unique players")
        print(f"✓ Extracted {len(self.positions)} unique positions")

    def _process_athlete(self, athlete: Dict):
        """Process individual athlete data"""
        if not athlete:
            return
            
        player_id = athlete.get('id')
        if player_id and player_id not in self.player_ids:
            self.player_ids.add(player_id)
            
            position = athlete.get('position', {})
            position_abbr = position.get('abbreviation')
            
            # Add position if new
            if position_abbr and position_abbr not in self.position_names:
                self.position_names.add(position_abbr)
                self.positions.append({
                    'position_abbreviation': position_abbr,
                    'position_name': position_abbr  # We only have abbreviation from the data
                })
            
            player_record = {
                'player_id': player_id,
                'full_name': athlete.get('fullName'),
                'display_name': athlete.get('displayName'),
                'short_name': athlete.get('shortName'),
                'jersey_number': athlete.get('jersey'),
                'position_abbreviation': position_abbr,
                'team_id': athlete.get('team', {}).get('id'),
                'is_active': athlete.get('active'),
                'headshot_url': athlete.get('headshot', '')
            }
            self.players.append(player_record)

    def extract_game_status_types(self):
        """Extract game status types from events"""
        print("Extracting game status types...")
        
        for event in self.data.get('events', []):
            for competition in event.get('competitions', []):
                status = competition.get('status', {})
                status_type = status.get('type', {})
                status_id = status_type.get('id')
                
                if status_id and status_id not in self.status_type_ids:
                    self.status_type_ids.add(status_id)
                    
                    status_record = {
                        'status_type_id': status_id,
                        'status_name': status_type.get('name'),
                        'status_state': status_type.get('state'),
                        'is_completed': status_type.get('completed'),
                        'description': status_type.get('description')
                    }
                    self.game_status_types.append(status_record)
        
        print(f"✓ Extracted {len(self.game_status_types)} game status types")

    def extract_games_and_competitions(self):
        """Extract game and competition data"""
        print("Extracting games and competitions...")
        
        for event in self.data.get('events', []):
            # Game record
            game_record = {
                'event_id': event.get('id'),
                'event_uid': event.get('uid'),
                'event_date': event.get('date'),
                'event_name': event.get('name'),
                'short_name': event.get('shortName'),
                'season_year': event.get('season', {}).get('year'),
                'season_type': event.get('season', {}).get('type'),
                'season_slug': event.get('season', {}).get('slug'),
                'week_number': event.get('week', {}).get('number')
            }
            self.games.append(game_record)
            
            # Competition records
            for competition in event.get('competitions', []):
                status = competition.get('status', {})
                
                competition_record = {
                    'competition_id': competition.get('id'),
                    'competition_uid': competition.get('uid'),
                    'event_id': event.get('id'),
                    'competition_date': competition.get('date'),
                    'attendance': competition.get('attendance'),
                    'venue_id': competition.get('venue', {}).get('id'),
                    'is_neutral_site': competition.get('neutralSite'),
                    'is_conference_competition': competition.get('conferenceCompetition'),
                    'status_clock': status.get('clock'),
                    'status_display_clock': status.get('displayClock'),
                    'status_period': status.get('period'),
                    'status_type_id': status.get('type', {}).get('id'),
                    'is_tbd_flex': status.get('isTBDFlex')
                }
                self.competitions.append(competition_record)
                
                # Extract team game stats and broadcasts
                self._extract_team_game_stats(competition, event.get('id'))
                self._extract_game_broadcasts(competition, event.get('id'))

    def _extract_team_game_stats(self, competition: Dict, event_id: str):
        """Extract team statistics for each game"""
        for competitor in competition.get('competitors', []):
            team_id = competitor.get('team', {}).get('id')
            
            team_stat_record = {
                'event_id': event_id,
                'competition_id': competition.get('id'),
                'team_id': team_id,
                'home_away': competitor.get('homeAway'),
                'score': competitor.get('score'),
                'order': competitor.get('order')
            }
            self.team_game_stats.append(team_stat_record)
            
            # Extract team records
            for record in competitor.get('records', []):
                record_data = {
                    'event_id': event_id,
                    'team_id': team_id,
                    'record_name': record.get('name'),
                    'record_abbreviation': record.get('abbreviation'),
                    'record_type': record.get('type'),
                    'record_summary': record.get('summary')
                }
                self.team_records.append(record_data)
            
            # Extract player leaders
            self._extract_player_leaders(competitor, event_id, team_id)

    def _extract_player_leaders(self, competitor: Dict, event_id: str, team_id: str):
        """Extract player statistical leaders"""
        for leader_category in competitor.get('leaders', []):
            category_name = leader_category.get('name')
            
            for leader in leader_category.get('leaders', []):
                athlete = leader.get('athlete', {})
                
                leader_record = {
                    'event_id': event_id,
                    'team_id': team_id,
                    'player_id': athlete.get('id'),
                    'category_name': category_name,
                    'display_name': leader_category.get('displayName'),
                    'abbreviation': leader_category.get('abbreviation'),
                    'display_value': leader.get('displayValue'),
                    'numeric_value': leader.get('value')
                }
                self.player_game_leaders.append(leader_record)

    def _extract_game_broadcasts(self, competition: Dict, event_id: str):
        """Extract broadcasting information"""
        for broadcast in competition.get('broadcasts', []):
            broadcast_record = {
                'event_id': event_id,
                'competition_id': competition.get('id'),
                'market': broadcast.get('market'),
                'network_names': ', '.join(broadcast.get('names', []))
            }
            self.game_broadcasts.append(broadcast_record)

    def write_csv_files(self):
        """Write all data to CSV files (append mode for subsequent runs)"""
        print("Writing CSV files...")
        
        # Define all tables and their data
        tables = {
            # Lookup Tables
            'leagues': self.leagues,
            'teams': self.teams,
            'venues': self.venues,
            'players': self.players,
            'positions': self.positions,
            'game_status_types': self.game_status_types,
            
            # Fact Tables
            'games': self.games,
            'competitions': self.competitions,
            'team_game_stats': self.team_game_stats,
            'player_game_leaders': self.player_game_leaders,
            'game_broadcasts': self.game_broadcasts,
            'team_records': self.team_records
        }
        
        for table_name, data in tables.items():
            if data:  # Only write if we have data
                file_path = os.path.join(self.output_dir, f"{table_name}.csv")
                file_exists = os.path.exists(file_path)
                
                # Use append mode if file exists, otherwise create new
                mode = 'a' if file_exists else 'w'
                
                with open(file_path, mode, newline='', encoding='utf-8') as csvfile:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    # Only write header if this is a new file
                    if not file_exists:
                        writer.writeheader()
                    
                    writer.writerows(data)
                
                action = "appended" if file_exists else "created"
                print(f"✓ {table_name}.csv: {action} {len(data)} records")
            else:
                print(f"⚠ {table_name}: No data to write")

    def process_all(self):
        """Main processing method - runs all extraction steps for multiple files"""
        print("Starting ESPN NFL data processing...")
        print("=" * 50)
        
        try:
            # Process all JSON files and accumulate data
            self.process_multiple_files()
            
            # Write all accumulated data to CSV files
            self.write_csv_files()
            
            print("=" * 50)
            print("✓ Processing completed successfully!")
            print(f"CSV files written to: {os.path.abspath(self.output_dir)}")
            print(f"Total files processed: {len(self.json_files)}")
            
        except Exception as e:
            print(f"❌ Error during processing: {str(e)}")
            raise

def main():
    """Main entry point
    
    Examples:
    # Process a single file
    processor = ESPNDataProcessor("week1-espn-response.json")
    
    # Process multiple files
    processor = ESPNDataProcessor(["week1.json", "week2.json", "week3.json"])
    
    # Process all JSON files in a directory
    processor = ESPNDataProcessor("json_files_directory/")
    """
    
    # Configuration - modify these paths as needed
    # Example 1: Single file (original behavior)
    # json_input = "espn-api-response-full.json"
    
    # Example 2: Multiple specific files
    # json_input = ["week1-espn-response.json", "week2-espn-response.json", "week3-espn-response.json"]
    
    # Example 3: All JSON files in a directory
    # json_input = "weekly_json_files/"

    json_input = "data/json_data/"
    
    output_directory = "data/csv_output"
    
    # Process the data
    processor = ESPNDataProcessor(json_input, output_directory)
    processor.process_all()

if __name__ == "__main__":
    main()