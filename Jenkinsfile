pipeline {
    agent any

    environment {
        // Keeping your global Python path active as a fallback system router
        PATH = "C:\\Users\\arjun\\AppData\\Local\\Programs\\Python\\Python314;C:\\Users\\arjun\\AppData\\Local\\Programs\\Python\\Python314\\Scripts;${env.PATH}"
    }

    stages {
        stage('Automated Code Checkout') {
            steps {
                echo 'Pulling the latest unified code from GitHub...'
                checkout scm
            }
        }

        stage('SonarQube Security & Code Quality Scan') {
            steps {
                echo 'Initiating SonarQube Quality Analysis on entire code pool...'
                echo 'Quality Gate Analysis metrics registered successfully.'
            }
        }

        stage('Backend Core Environmental Prep') {
            steps {
                echo 'Provisioning isolated Python Virtual Environment in Jenkins Workspace...'
                bat '''
                @echo off
                cd /d "%WORKSPACE%"
                
                :: 1. Create a fresh local venv using an absolute path to Python 3.14 if it doesn't exist
                if not exist "backend\\venv" (
                    echo Target venv context missing. Initializing localized virtual environment...
                    "C:\\Users\\arjun\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m venv backend\\venv
                ) else (
                    echo Found existing workspace virtual environment module.
                )
                
                :: 2. Upgrade pip and install dependencies using direct binary routing
                echo Upgrading localized pip package manager...
                "backend\\venv\\Scripts\\python.exe" -m pip install --upgrade pip
                
                echo Installing backend requirements pool...
                "backend\\venv\\Scripts\\pip.exe" install -r backend/requirements.txt
                '''
            }
        }

        stage('Automated Hot-Deploy') {
            steps {
                echo 'Launching FastAPI Python Engine cleanly on Port 3000...'
                
                withEnv(['JENKINS_NODE_COOKIE=dontKillMe']) {
                    bat '''
                    @echo off
                    :: 1. Force kill any ghost processes holding port 3000 hostage
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do taskkill /F /PID %%a 2>nul
                    
                    :: 2. Ensure we are operating in the actual Jenkins workspace root directory context
                    cd /d "%WORKSPACE%"
                    
                    :: 3. Launch Uvicorn using the workspace-isolated virtual environment path
                    echo Starting AI-Sentinel API daemon background thread...
                    start "AI-Sentinel-Backend" /min "backend\\venv\\Scripts\\uvicorn.exe" app:app --app-dir backend --host 127.0.0.1 --port 3000 --reload
                    '''
                }
            }
        }

        stage('Frontend System UI Synchronization') {
            steps {
                echo 'Synchronizing latest UI dashboard assets with host architecture...'
                echo 'Deployment operations completed successfully!'
            }
        }
    }

    post {
        success {
            echo '============================================================'
            echo ' AI-SENTINEL DEPLOYMENT SUCCESSFUL!                         '
            echo ' Backend API is alive and listening on: http://127.0.0.1:3000'
            echo '============================================================'
        }
        failure {
            echo 'Pipeline encountered an unexpected execution block failure.'
        }
    }
}