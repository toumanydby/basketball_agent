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
│   ├── decision/         # Decision making system
│   │   ├── decision_maker.py  # Core decision making logic
│   │   └── example.py    # Usage examples
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

3. **Decision Making** (Implemented)
   - Action generation for both offensive and defensive situations
   - Priority-based action selection
   - Position calculation for optimal player movement
   - Support for multiple action types:
     - Movement actions
     - Passing actions
     - Shooting actions
     - Defensive actions
   - Real-time tactical suggestions based on game state

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

### Decision Making
The system provides:
- Prioritized action recommendations
- Position calculations for optimal spacing
- Defensive hole filling strategies
- Help defense positioning
- Attack position optimization
- Ball possession management

### Metrics
- Distance calculations between players
- Space occupation calculations
- Court position determination
- Defensive positioning evaluation
- Team formation analysis

## Usage

To run the example:
```bash
python -m src.decision.example
```

This will demonstrate the decision-making system's analysis of a sample game state, showing recommended actions for both teams with their respective priorities.

## Future Development
- [ ] Add visualization tools for game state analysis
- [ ] Implement real-time data processing pipeline
- [ ] Add machine learning models for strategy optimization
- [ ] Develop API for real-time game analysis
- [ ] Add support for different basketball rule sets
- [ ] Implement action execution simulation
- [ ] Add performance metrics tracking
- [ ] Develop strategy optimization algorithms 