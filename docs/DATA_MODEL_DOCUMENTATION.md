# ESPN NFL Data Model Documentation

## Overview

This document describes the normalized data model created from ESPN NFL API JSON response data. The data has been extracted into a series of CSV files representing lookup tables (dimension tables) and fact tables for analytical purposes.

## Data Processing Summary

- **Source**: ESPN NFL API JSON response (26,148 lines)
- **Output**: 12 normalized CSV files
- **Processing Date**: October 8, 2025
- **Season Data**: 2025 NFL Season

## File Summary

### Lookup Tables (Dimension Tables)

| File                    | Records | Description                          |
| ----------------------- | ------- | ------------------------------------ |
| `leagues.csv`           | 1       | League information (NFL)             |
| `teams.csv`             | 28      | NFL team details                     |
| `venues.csv`            | 13      | Stadium/venue information            |
| `players.csv`           | 81      | Player information from game leaders |
| `positions.csv`         | 4       | Player position types                |
| `game_status_types.csv` | 1       | Game status classifications          |

### Fact Tables (Transaction Tables)

| File                      | Records | Description                         |
| ------------------------- | ------- | ----------------------------------- |
| `games.csv`               | 14      | Game/event master records           |
| `competitions.csv`        | 14      | Competition details for each game   |
| `team_game_stats.csv`     | 28      | Team performance in each game       |
| `player_game_leaders.csv` | 84      | Player statistical leaders per game |
| `game_broadcasts.csv`     | 14      | Broadcasting information            |
| `team_records.csv`        | 84      | Team win/loss records               |

## Table Schemas

### Lookup Tables

#### leagues.csv

Primary dimension table for league information.

```
Columns:
- league_id (PK): Unique league identifier
- league_uid: ESPN unique identifier
- name: Full league name
- abbreviation: League abbreviation (NFL)
- slug: URL-friendly identifier
- season_year: Current season year
- season_start_date: Season start date
- season_end_date: Season end date
- season_display_name: Human-readable season name
- season_type_id: Season type identifier
- season_type_name: Season type description
- calendar_type: Calendar type
- calendar_start_date: Calendar start date
- calendar_end_date: Calendar end date
```

#### teams.csv

Master team information table.

```
Columns:
- team_id (PK): Unique team identifier
- team_uid: ESPN unique identifier
- location: Team city/location
- name: Team name
- abbreviation: Team abbreviation (3-letter code)
- display_name: Full display name
- short_display_name: Short display name
- color: Primary team color (hex)
- alternate_color: Secondary team color (hex)
- is_active: Whether team is active
- venue_id (FK): References venues.venue_id
- logo_url: Team logo URL
```

#### venues.csv

Stadium and venue information.

```
Columns:
- venue_id (PK): Unique venue identifier
- full_name: Complete venue name
- city: Venue city
- state: Venue state
- country: Venue country
- is_indoor: Whether venue is indoor
```

#### players.csv

Player information extracted from game leader statistics.

```
Columns:
- player_id (PK): Unique player identifier
- full_name: Player's full name
- display_name: Player's display name
- short_name: Player's short name
- jersey_number: Player's jersey number
- position_abbreviation (FK): References positions.position_abbreviation
- team_id (FK): References teams.team_id
- is_active: Whether player is active
- headshot_url: Player headshot image URL
```

#### positions.csv

Player position reference table.

```
Columns:
- position_abbreviation (PK): Position abbreviation (QB, RB, etc.)
- position_name: Full position name
```

#### game_status_types.csv

Game status classifications.

```
Columns:
- status_type_id (PK): Unique status type identifier
- status_name: Status name
- status_state: Status state
- is_completed: Whether status indicates completion
- description: Status description
```

### Fact Tables

#### games.csv

Master game/event table containing high-level game information.

```
Columns:
- event_id (PK): Unique event identifier
- event_uid: ESPN unique identifier
- event_date: Game date and time
- event_name: Full game name
- short_name: Short game name
- season_year: Season year
- season_type: Season type
- season_slug: Season slug
- week_number: Week number
```

#### competitions.csv

Detailed competition information for each game.

```
Columns:
- competition_id (PK): Unique competition identifier
- competition_uid: ESPN unique identifier
- event_id (FK): References games.event_id
- competition_date: Competition date
- attendance: Game attendance
- venue_id (FK): References venues.venue_id
- is_neutral_site: Whether played at neutral site
- is_conference_competition: Whether conference game
- status_clock: Game clock
- status_display_clock: Display clock
- status_period: Game period
- status_type_id (FK): References game_status_types.status_type_id
- is_tbd_flex: Whether TBD/flex scheduled
```

#### team_game_stats.csv

Team performance statistics for each game.

```
Columns:
- event_id (FK): References games.event_id
- competition_id (FK): References competitions.competition_id
- team_id (FK): References teams.team_id
- home_away: Home or away designation
- score: Team score
- order: Team order in competition
```

#### player_game_leaders.csv

Player statistical leaders for each game and category.

```
Columns:
- event_id (FK): References games.event_id
- team_id (FK): References teams.team_id
- player_id (FK): References players.player_id
- category_name: Statistical category (passingLeader, etc.)
- display_name: Category display name
- abbreviation: Category abbreviation
- display_value: Formatted statistical value
- numeric_value: Numeric statistical value
```

#### game_broadcasts.csv

Broadcasting information for each game.

```
Columns:
- event_id (FK): References games.event_id
- competition_id (FK): References competitions.competition_id
- market: Broadcast market (national, local)
- network_names: Broadcasting networks (comma-separated)
```

#### team_records.csv

Team win/loss records for different contexts.

```
Columns:
- event_id (FK): References games.event_id
- team_id (FK): References teams.team_id
- record_name: Record type name
- record_abbreviation: Record abbreviation
- record_type: Record type (total, home, road)
- record_summary: Record summary (W-L format)
```

## Relationships and Foreign Keys

The data model follows a star schema pattern with the following key relationships:

1. **games** ← **competitions** (1:1)
2. **competitions** → **venues** (N:1)
3. **competitions** ← **team_game_stats** (1:2)
4. **teams** ← **team_game_stats** (1:N)
5. **teams** ← **players** (1:N)
6. **positions** ← **players** (1:N)
7. **games** ← **player_game_leaders** (1:N)
8. **players** ← **player_game_leaders** (1:N)
9. **games** ← **game_broadcasts** (1:N)
10. **games** ← **team_records** (1:N)

## Data Quality Notes

### Coverage

- **Games**: 14 games from NFL Week 5, 2025 season
- **Teams**: 28 unique teams (not all 32 NFL teams represented in this dataset)
- **Players**: 81 players (only statistical leaders included)
- **Venues**: 13 unique venues

### Limitations

1. **Player Data**: Only includes players who are statistical leaders in games
2. **Incomplete Team Roster**: Full team rosters are not included
3. **Historical Data**: This dataset represents a snapshot of current season games
4. **Game Status**: All games in this dataset appear to be scheduled (pre-game)

### Data Types

- **Dates**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- **IDs**: String identifiers
- **Boolean**: True/False values
- **URLs**: Full HTTP/HTTPS URLs for images and links

## Usage Examples

### SQL Query Examples (if importing to database)

```sql
-- Get all games for a specific week
SELECT g.event_name, g.event_date, g.week_number
FROM games g
WHERE g.week_number = 5;

-- Get team statistics for a specific game
SELECT t.display_name, tgs.home_away, tgs.score
FROM team_game_stats tgs
JOIN teams t ON tgs.team_id = t.team_id
WHERE tgs.event_id = '401772939';

-- Get top passing leaders
SELECT p.display_name, pgl.display_value, t.abbreviation
FROM player_game_leaders pgl
JOIN players p ON pgl.player_id = p.player_id
JOIN teams t ON pgl.team_id = t.team_id
WHERE pgl.category_name = 'passingLeader'
ORDER BY pgl.numeric_value DESC;
```

### Analytics Use Cases

1. **Fantasy Football Analysis**: Player performance tracking
2. **Team Performance**: Win/loss records and statistics
3. **Venue Analysis**: Home field advantage studies
4. **Broadcast Analysis**: Network coverage patterns
5. **Season Tracking**: Game scheduling and results

## File Formats

- **Encoding**: UTF-8
- **Delimiter**: Comma (,)
- **Quote Character**: Double quotes (") when needed
- **Headers**: First row contains column names
- **Line Endings**: Windows CRLF

## Processing Information

- **Script**: `espn_data_processor.py`
- **Language**: Python 3
- **Dependencies**: Standard library only (json, csv, os, datetime)
- **Processing Time**: < 1 second for 26K line JSON file
- **Memory Usage**: Minimal (all data held in memory during processing)
