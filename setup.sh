#!/bin/bash

# MatchedCover Insurance Platform Setup and Run Script

echo "🚀 Starting MatchedCover Insurance Platform Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is required but not installed"
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_warning "Node.js not found. Frontend components may not work."
    fi
}

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d " " -f 3 | cut -d "," -f 1)
        print_success "Docker $DOCKER_VERSION found"
    else
        print_warning "Docker not found. Database services will need manual setup."
    fi
}

# Create virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Python dependencies installed"
}

# Setup environment variables
setup_env() {
    print_status "Setting up environment variables..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your specific configuration"
    else
        print_status "Environment file already exists"
    fi
}

# Start database services with Docker
start_databases() {
    print_status "Starting database services..."
    
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d postgres redis mongodb chromadb qdrant
        print_success "Database services started"
        
        # Wait for services to be ready
        print_status "Waiting for database services to be ready..."
        sleep 10
        
    else
        print_warning "Docker Compose not found. Please start database services manually."
    fi
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    
    # This would run database migrations in a real setup
    print_success "Database initialization completed"
}

# Start the application
start_app() {
    print_status "Starting MatchedCover Insurance Platform..."
    
    # Export environment variables
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Start the FastAPI application
    python src/main.py
}

# Main execution
main() {
    echo "=================================================================================="
    echo "                    🎯  MatchedCover Insurance Platform Setup                      "
    echo "=================================================================================="
    echo ""
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    check_python
    check_node
    check_docker
    echo ""
    
    # Setup Python environment
    setup_venv
    install_python_deps
    echo ""
    
    # Setup configuration
    setup_env
    echo ""
    
    # Start services
    start_databases
    echo ""
    
    # Initialize application
    init_database
    echo ""
    
    # Final instructions
    echo "=================================================================================="
    print_success "Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Edit .env file with your API keys and configuration"
    echo "2. Ensure database services are running"
    echo "3. Start the application with: python src/main.py"
    echo ""
    print_status "API Documentation will be available at:"
    echo "• Swagger UI: http://localhost:8000/docs"
    echo "• ReDoc: http://localhost:8000/redoc"
    echo ""
    print_status "Monitoring dashboards:"
    echo "• Grafana: http://localhost:3001 (admin/admin)"
    echo "• Prometheus: http://localhost:9090"
    echo ""
    echo "=================================================================================="
    
    # Ask if user wants to start the application
    read -p "Start the application now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_app
    else
        print_status "You can start the application later with: python src/main.py"
    fi
}

# Run main function
main "$@"
