# First Incident Responder - AI-Powered Emergency Response

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/Powered%20by-CrewAI-orange)](https://crewai.com)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io)

First Incident Responder is a comprehensive AI-powered platform that uses emergency incident response systems. Built using CrewAI's multi-agent framework, this system demonstrates the power of collaborative AI agents working together to solve complex, real-world problems.

## 🌟 Key Features

### 🚨 Emergency Response System
- **Multi-Category Incident Handling**: Fire, Medical, Police, and Accident response crews
- **Intelligent Classification**: Automatic incident categorization and severity assessment using Google's Gemini AI
- **Real-time Communication**: Automated email notifications to relevant authorities
- **Interactive Web Interface**: Streamlit-based UI with real-time chat assistance
- **Geographic Integration**: Browser-based location services for precise incident reporting
- **Comprehensive Logging**: CSV-based incident tracking and reporting


## 🏗️ Architecture

The system is built around specialized AI agent crews:

### Emergency Response Crews
- **FireCrew**: Specialized fire incident response and safety guidance
- **MedicalCrew**: Medical emergency handling and first-aid coordination
- **PoliceCrew**: Law enforcement incident management
- **AccidentCrew**: Traffic and general accident response


## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Google API credentials (for Gmail and Gemini AI integration)
- UV package manager (recommended) or pip

### Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd mentormindflows
```

2. **Install UV package manager** (if not already installed)
```bash
pip install uv
```

3. **Install dependencies**
```bash
uv sync
# OR using pip
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file in the root directory:
```bash
# AI Model API Keys
GEMINI_KEY=your_google_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional

# Gmail Integration (for automated notifications)
GMAIL_CREDENTIALS_PATH=src/mentormindflows/crews/gmailcrew/tools/credentials.json

# Optional: Default incident response settings
FIRE_USERNAME=System_Admin
FIRE_LOCATION=Default_Location
FIRE_SEVERITY=medium
```

5. **Gmail API Setup** (for email notifications)
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable the Gmail API
- Create OAuth 2.0 credentials
- Download the credentials file as `credentials.json`
- Place it in `src/mentormindflows/crews/gmailcrew/tools/`

## 🎯 Usage

### Emergency Response Web Application

Launch the Streamlit web interface:
```bash
streamlit run app.py
```

Features:
- **Incident Reporting**: Fill out incident details with optional image upload
- **Automatic Classification**: AI determines incident type and severity
- **Real-time Chat**: Get immediate guidance while authorities are contacted
- **Report Generation**: Comprehensive incident reports
- **Download Reports**: Export reports in Markdown format

### Educational Mentoring System

#### Command Line Interface
```bash
# Run the complete mentoring flow
crewai run

# Generate study plans only
python src/mentormindflows/crews/main_crew/studyplanner_crew.py

# Peer comparison analysis
python src/mentormindflows/crews/main_crew/peercomparision_crew.py
```

## 📁 Project Structure

```
mentormindflows/
├── app.py                          # Main Streamlit application
├── pyproject.toml                  # Project configuration
├── README.md                       # This file
├── outputs/                        # Generated reports and logs
├── src/mentormindflows/
│   ├── main.py                     # Core flow orchestration
│   ├── crews/                      # AI agent crews
│   │   ├── main_crew/              # Emergency & educational crews
│   │   │   ├── fire_crew.py        # Fire incident response
│   │   │   ├── medical_crew.py     # Medical emergency handling
│   │   │   ├── police_crew.py      # Police incident management
│   │   │   ├── accident_crew.py    # Accident response
│   │   │   ├── studyplanner_crew.py # Agent and task configurations
│   │   └── gmailcrew/              # Email communication crew
│   ├── tools/                      # Custom tools and utilities
│   │   ├── csv_logger_tool.py      # Incident logging
│   │   ├── writeFile_tool.py       # File operations
│   │   └── custom_tool.py          # 
│   └── outputs/                    # System-generated outputs
└── tests/                          # Test files and sample data
```

## 🛠️ Configuration

### Agent Configuration
Agents are configured via YAML files in `src/mentormindflows/crews/main_crew/config/`:
- `*_agents.yaml`: Define agent roles, goals, and backstories
- `*_tasks.yaml`: Specify tasks, descriptions, and expected outputs

### LLM Models
The system supports multiple AI models:
- **Google Gemini 2.0 Flash** (Primary for emergency response)

### Customization Options
- **Modify Agent Behavior**: Edit YAML configuration files
- **Add New Incident Types**: Create new crew classes and configurations
- **Extend Educational Features**: Add new analysis tools and report types
- **Custom Tools**: Implement additional CrewAI tools in the `tools/` directory

## 📊 Output Formats

### Emergency Response
- **Incident Reports**: Comprehensive Markdown reports with incident details
- **CSV Logs**: Structured data for analysis and record-keeping
- **Email Notifications**: HTML-formatted alerts to authorities


## 🔧 Development

### Adding New Crews
1. Create a new crew class inheriting from `CrewBase`
2. Define agents and tasks in corresponding YAML files
3. Implement custom tools if needed
4. Register the crew in the main flow orchestration

### Testing
```bash
# Run specific crew tests
python -m pytest tests/

# Test individual components
python src/mentormindflows/tools/custom_tool.py
```

## 📋 Requirements

### Core Dependencies
- `crewai[tools]>=0.114.0,<1.0.0` - Multi-agent AI framework
- `streamlit>=1.36` - Web interface
- `google-api-python-client>=2.137.0` - Gmail integration
- `google-generativeai>=0.7.0` - Gemini AI integration
- `python-dotenv>=1.0.1` - Environment management

### Optional Dependencies
- `streamlit-markmap>=0.1.7` - Mind map visualization
- `streamlit-js-eval>=0.1.7` - JavaScript integration
- `markdown>=3.5` - Markdown processing

## 🔒 Security Considerations

- **API Keys**: Store securely in environment variables, never commit to version control
- **Gmail Credentials**: Use OAuth 2.0 flow, regularly rotate credentials  
- **Input Validation**: All user inputs are validated before processing
- **Data Privacy**: Student data and incident reports are handled according to privacy best practices


## Acknowledgments

- **Google**: For Gemini AI and Gmail API integration
- **Streamlit**: For the intuitive web application framework

### Upcoming Features
- [ ] Advanced analytics and reporting
- [ ] Mobile application support
- [ ] Integration with more AI models
- [ ] Enhanced visualization capabilities
- [ ] Advanced security features

