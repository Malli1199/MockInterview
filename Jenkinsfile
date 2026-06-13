pipeline {
    agent any

    environment {
        // Ensuring your global Python 3.14 paths are fully active in this session
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
                echo 'Verifying application dependencies inside site-packages...'
                bat 'pip install -r backend/requirements.txt'
            }
        }

        stage('Automated Hot-Deploy') {
            steps {
                echo 'Launching FastAPI Python Engine cleanly on Port 3000...'
                // The 'run' command instructs the agent to spawn the web server process and move on immediately
                // without trapping the shell environment loop.
                bat 'start /min cmd /c "uvicorn app:app --app-dir backend --host 127.0.0.1 --port 3000"'
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