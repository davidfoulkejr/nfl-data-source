```mermaid
erDiagram
    LEAGUES {
        string league_id PK
        string league_uid
        string name
        string abbreviation
        string slug
        int season_year
        string season_start_date
        string season_end_date
        string season_display_name
        string season_type_id
        string season_type_name
        string calendar_type
        string calendar_start_date
        string calendar_end_date
    }

    TEAMS {
        string team_id PK
        string team_uid
        string location
        string name
        string abbreviation
        string display_name
        string short_display_name
        string color
        string alternate_color
        boolean is_active
        string venue_id FK
        string logo_url
    }

    VENUES {
        string venue_id PK
        string full_name
        string city
        string state
        string country
        boolean is_indoor
    }

    PLAYERS {
        string player_id PK
        string full_name
        string display_name
        string short_name
        string jersey_number
        string position_abbreviation FK
        string team_id FK
        boolean is_active
        string headshot_url
    }

    POSITIONS {
        string position_abbreviation PK
        string position_name
    }

    GAME_STATUS_TYPES {
        string status_type_id PK
        string status_name
        string status_state
        boolean is_completed
        string description
    }

    GAMES {
        string event_id PK
        string event_uid
        string event_date
        string event_name
        string short_name
        int season_year
        int season_type
        string season_slug
        int week_number
    }

    COMPETITIONS {
        string competition_id PK
        string competition_uid
        string event_id FK
        string competition_date
        int attendance
        string venue_id FK
        boolean is_neutral_site
        boolean is_conference_competition
        int status_clock
        string status_display_clock
        int status_period
        string status_type_id FK
        boolean is_tbd_flex
    }

    TEAM_GAME_STATS {
        string event_id FK
        string competition_id FK
        string team_id FK
        string home_away
        string score
        int order
    }

    PLAYER_GAME_LEADERS {
        string event_id FK
        string team_id FK
        string player_id FK
        string category_name
        string display_name
        string abbreviation
        string display_value
        float numeric_value
    }

    GAME_BROADCASTS {
        string event_id FK
        string competition_id FK
        string market
        string network_names
    }

    TEAM_RECORDS {
        string event_id FK
        string team_id FK
        string record_name
        string record_abbreviation
        string record_type
        string record_summary
    }

    %% Relationships
    TEAMS ||--o{ VENUES : "plays at"
    PLAYERS }o--|| TEAMS : "belongs to"
    PLAYERS }o--|| POSITIONS : "has position"

    GAMES ||--|| COMPETITIONS : "has"
    COMPETITIONS }o--|| VENUES : "held at"
    COMPETITIONS }o--|| GAME_STATUS_TYPES : "has status"

    GAMES ||--o{ TEAM_GAME_STATS : "includes"
    TEAMS ||--o{ TEAM_GAME_STATS : "participates in"
    COMPETITIONS ||--o{ TEAM_GAME_STATS : "contains"

    GAMES ||--o{ PLAYER_GAME_LEADERS : "features"
    TEAMS ||--o{ PLAYER_GAME_LEADERS : "has leaders from"
    PLAYERS ||--o{ PLAYER_GAME_LEADERS : "leads in"

    GAMES ||--o{ GAME_BROADCASTS : "broadcast on"
    COMPETITIONS ||--o{ GAME_BROADCASTS : "broadcast details"

    GAMES ||--o{ TEAM_RECORDS : "affects"
    TEAMS ||--o{ TEAM_RECORDS : "maintains"
```

# ESPN NFL Data Model - Entity Relationship Diagram

This diagram shows the relationships between all tables in the normalized ESPN NFL dataset.

## Key Relationships

### Core Game Structure

- **GAMES** (1) ←→ (1) **COMPETITIONS**: Each game has one competition
- **COMPETITIONS** (N) → (1) **VENUES**: Multiple games can be at same venue
- **COMPETITIONS** (N) → (1) **GAME_STATUS_TYPES**: Games have status types

### Team Structure

- **TEAMS** (N) → (1) **VENUES**: Teams have home venues
- **PLAYERS** (N) → (1) **TEAMS**: Players belong to teams
- **PLAYERS** (N) → (1) **POSITIONS**: Players have positions

### Game Statistics

- **GAMES** (1) → (N) **TEAM_GAME_STATS**: Each game has 2 team stats records
- **TEAMS** (1) → (N) **TEAM_GAME_STATS**: Teams play multiple games
- **GAMES** (1) → (N) **PLAYER_GAME_LEADERS**: Games have multiple stat leaders
- **PLAYERS** (1) → (N) **PLAYER_GAME_LEADERS**: Players can lead in multiple categories

### Supporting Data

- **GAMES** (1) → (N) **GAME_BROADCASTS**: Games have broadcast info
- **GAMES** (1) → (N) **TEAM_RECORDS**: Games affect team records

## Table Types

### Dimension Tables (Lookup)

- LEAGUES, TEAMS, VENUES, PLAYERS, POSITIONS, GAME_STATUS_TYPES

### Fact Tables (Transactions)

- GAMES, COMPETITIONS, TEAM_GAME_STATS, PLAYER_GAME_LEADERS, GAME_BROADCASTS, TEAM_RECORDS
