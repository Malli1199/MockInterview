pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_PROJECT_KEY = 'pure-web-mock-portal'
    }

    stages {
        stage('1. Quality Assurance Analysis') {
            steps {
                echo 'Firing up SonarQube quality engine structural checks...'
                withSonarQubeEnv('SonarQube-Server-Config-Name') {
                    bat '"' + SCANNER_HOME + '\\bin\\sonar-scanner.bat" \
                    -Dsonar.projectKey=' + SONAR_PROJECT_KEY + ' \
                    -Dsonar.sources=. \
                    -Dsonar.exclusions=node_modules/**'
                }
            }
        }

        stage('2. Continuous Local Hosting Setup') {
            steps {
                echo 'Clearing any active ports running on 3000...'
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    bat 'taskkill /F /IM http-server'
                }
                echo 'Spawning isolated production web thread...'
                bat 'npm install -g http-server'
                // This starts the server directly as a silent background daemon process
                bat 'start /B http-server . -p 3000'
                bat 'timeout /t 3 /nobreak'
            }
        }

        stage('3. Functional Testing Via Selenium') {
            steps {
                echo 'Injecting automated test cases against live system port...'
                bat 'python login_test.py'
            }
        }
    }
    post {
        success {
            echo '======================================================'
            echo 'BUILD PERFECT: New page running at http://localhost:3000'
            echo '======================================================'
        }
    }
}