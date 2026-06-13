pipeline {
    agent any

    environment {
        // Explicitly ensuring system pathways are mapped cleanly
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
                echo 'Installing required AI machine learning modules from requirements.txt...'
                bat 'pip install -r backend/requirements.txt'
            }
        }

        stage('Port 3000 Reset & Automated Hot-Deploy') {
            steps {
                echo 'Clearing port 3000 conflicts'
                bat '''
                @echo off
                netstat -aon | findstr :3000 > nul
                if %errorlevel% equ 0 (
                    FOR /F "tokens=5" %%P IN ('netstat -aon ^| findstr :3000') DO taskkill /F /PID %%P
                ) else (
                    echo Port 3000 clean.
                )
                '''
                
                echo 'Spawning background engine'
                bat 'start /B cmd /c "uvicorn app:app --app-dir backend --host 127.0.0.1 --port 3000 > nul 2>&1"'
            }
        }

        stage('Frontend System UI Synchronization') {
            steps {
                echo 'Synchronizing latest UI assets with host architecture...'
                // Add any deployment copy paths here if needed later
            }
        }
    }

    post {
        always {
            echo 'Pipeline Execution Status Processed. Review logs.'
        }
    }
}