# Basketball AI Agent

An intelligent agent system designed to analyze basketball game situations and provide optimal decision-making recommendations. The system uses real-time player and ball position data to evaluate game situations and provide tactical insights.

## Project Structure

```
basketball_ai_agent/
├── data/                   # Data storage and processing
│   ├── raw/               # Raw input data
│   └── processed/         # Processed data
├── src/                   # Source code
│   ├── data/             # Data processing modules
│   ├── models/           # AI models and decision making
│   ├── rules/            # Basketball rules implementation
│   │   ├── metrics.py    # Core metrics and position calculations
│   │   ├── rules_engine.py # Rule implementation and evaluation
│   │   └── example.py    # Usage examples
│   └── utils/            # Utility functions
├── tests/                # Test files
├── notebooks/            # Jupyter notebooks for analysis
└── config/              # Configuration files
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Format

The input data should contain:
- Player positions (x1,x2, y1,y2 coordinates) for each team
  - x1,x2: horizontal bounding box coordinates
  - y1,y2: vertical bounding box coordinates
- Ball position (x1,x2, y1,y2 coordinates)
- Timestamp for each position
- Additional game context (score, time remaining, etc.)

## Components

1. **Data Processing**
   - Input data validation and cleaning
   - Position data normalization
   - Feature extraction
   - Bounding box coordinate handling
   - Center point calculations for distance metrics

2. **Rule Engine** (Implemented)
   - Implementation of basketball rules:
     - Attack position rules
     - Defensive position rules
     - Team spacing rules (Dmin = 4m)
     - Ball possession time rules (max 3s)
     - Defensive hole detection (Strou = 4m)
     - Defensive help rules
     - Zone respect rules
     - Defensive positioning rules
   - Situation analysis
   - Context evaluation
   - Real-time rule compliance checking

3. **Decision Making** (In Progress)
   - Strategy selection
   - Action recommendation
   - Performance metrics calculation
   - Real-time tactical suggestions

## Implementation Details

### Position Tracking
- Uses bounding box coordinates (x1,x2, y1,y2) for precise player and ball tracking
- Calculates center points for distance measurements
- Handles player space occupation using bounding box areas

### Rule Evaluation
The system evaluates:
- Team positioning during attack and defense
- Player spacing and formation
- Ball possession time
- Defensive coverage and help
- Zone assignments
- Rebound opportunities

### Metrics
- Distance calculations between players
- Space occupation calculations
- Court position determination
- Defensive positioning evaluation
- Team formation analysis

## Usage

To run the example:
```bash
python -m src.rules.example
```

This will demonstrate the rule engine's evaluation of a sample game state, showing which rules are being followed (✓) and which are being violated (✗).

## Future Development
- [ ] Add visualization tools for game state analysis
- [ ] Implement real-time data processing pipeline
- [ ] Add machine learning models for strategy optimization
- [ ] Develop API for real-time game analysis
- [ ] Add support for different basketball rule sets 