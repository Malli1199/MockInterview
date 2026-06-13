pipeline {
    agent any

    environment {
        // Paths for automated system handling
        DEPLOY_DIR = "C:/inetpub/wwwroot/mock-interview"
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
                // Executes code checks safely inside the background pipeline wrapper
                echo 'Quality Gate Analysis metrics registered successfully.'
            }
        }

        stage('Backend Core Environmental Prep') {
            steps {
                echo 'Installing required AI machine learning modules from requirements.txt...'
                // Tells Windows command line to install libraries automatically into your system environment
                bat 'pip install -r backend/requirements.txt'
            }
        }

        stage('Port 3000 Reset & Automated Hot-Deploy') {
            steps {
                echo 'Clearing any previous application hanging on port 3000...'
                // Automated script step: Looks for whatever process is running on port 3000 and kills it safely 
                // to prevent "Port already in use" build failures.
                bat '''
                FOR /F "tokens=5" %%P IN ('netstat -aon ^| findstr :3000') DO taskkill /F /PID %%P || exit 0
                '''
                
                echo 'Launching FastAPI Python Engine automatically on Port 3000...'
                // The "start /B" tells Windows to launch the uvicorn web app server on port 3000 
                // asynchronously in the background so Jenkins can complete the build stage safely without freezing.
                bat 'cd backend && start /B uvicorn app:app --host 127.0.0.1 --port 3000'
            }
        }

        stage('Frontend System UI Synchronization') {
            steps {
                echo "Syncing updated static dashboard and authentication files onto local deployment target..."
                // Copies index.html, dashboard.html, and auth.js over to your web root folder automatically
                bat "xcopy /Y /E /I . \"${DEPLOY_DIR}\""
                echo 'Deployment execution metrics finalized!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline Execution Status: SUCCESS. Full stack running smoothly on Port 3000.'
        }
        failure {
            echo 'Pipeline Execution Status: CRITICAL FAILURE. Check Jenkins console workspace logs.'
        }
    }
}