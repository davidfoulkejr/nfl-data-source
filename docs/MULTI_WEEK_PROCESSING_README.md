# ESPN Data Processor - Multi-Week Support

This updated version of the ESPN NFL API Data Processor now supports processing multiple JSON files representing different NFL weeks, automatically appending data to existing CSV files instead of overwriting them.

## Key Features

### Multi-Input Support

- **Single File**: Process one JSON file (original behavior)
- **Multiple Files**: Process a list of specific JSON files
- **Directory Processing**: Process all JSON files in a directory

### Append Mode

- Automatically detects existing CSV files
- Appends new data instead of overwriting
- Adds CSV headers only for new files
- Maintains data integrity across multiple processing runs

### Duplicate Prevention

- Prevents duplicate teams, venues, players, and other lookup data
- Maintains unique IDs across all processed weeks
- Accumulates game and statistical data from all weeks

## Usage Examples

### 1. Single File (Original Behavior)

```python
from espn_data_processor import ESPNDataProcessor

processor = ESPNDataProcessor("week1-espn-response.json")
processor.process_all()
```

### 2. Multiple Specific Files

```python
week_files = [
    "week1-espn-response.json",
    "week2-espn-response.json",
    "week3-espn-response.json"
]
processor = ESPNDataProcessor(week_files)
processor.process_all()
```

### 3. All Files in Directory

```python
processor = ESPNDataProcessor("path/to/weekly/json/files/")
processor.process_all()
```

## Typical Weekly Workflow

1. **Initial Setup**: Run processor with Week 1 data

   - Creates all CSV files with headers
   - Populates initial data

2. **Weekly Updates**: Add new week data

   - Download new week's JSON file
   - Run processor with new file
   - Data automatically appended to existing CSVs

3. **Bulk Processing**: Process multiple weeks at once
   - Place all JSON files in a directory
   - Run processor on the directory
   - All data consolidated into single CSV set

## Output Files

The processor creates/updates these CSV files:

**Lookup Tables** (deduplicated):

- `leagues.csv` - League information
- `teams.csv` - Team details
- `venues.csv` - Stadium/venue information
- `players.csv` - Player information
- `positions.csv` - Position types
- `game_status_types.csv` - Game status definitions

**Fact Tables** (accumulated):

- `games.csv` - Game events
- `competitions.csv` - Competition details
- `team_game_stats.csv` - Team statistics per game
- `player_game_leaders.csv` - Player statistical leaders
- `game_broadcasts.csv` - Broadcasting information
- `team_records.csv` - Team records

## File Processing Order

When processing multiple files, the processor:

1. Processes files in the order provided (or alphabetical for directories)
2. Accumulates lookup data (teams, players, etc.) without duplicates
3. Appends all fact data (games, stats, etc.)
4. Writes all data to CSV files in append mode

## Error Handling

- Validates that input files exist before processing
- Gracefully handles missing or malformed JSON data
- Provides detailed progress reporting during processing
- Maintains data integrity if processing is interrupted

## Migration from Original Version

The updated processor is fully backward compatible:

- Original single-file usage works unchanged
- Existing CSV files are preserved and extended
- No data loss when upgrading

Simply replace your existing processor calls with the new version and optionally take advantage of multi-file capabilities.
