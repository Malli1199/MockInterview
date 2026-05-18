pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_PROJECT_KEY = 'pure-web-mock-portal'
    }

    stages {
        stage('1. Code Quality Inspection') {
            steps {
                echo 'Sending HTML/JavaScript codebase to local SonarQube Server...'
                withSonarQubeEnv('SonarQube-Server-Config-Name') {
                    /*
                      Specifying js and html sources. SonarQube automatically 
                      scans web languages without needing a compiler.
                    */
                    bat '"' + SCANNER_HOME + '\\bin\\sonar-scanner.bat" \
                    -Dsonar.projectKey=' + SONAR_PROJECT_KEY + ' \
                    -Dsonar.sources=. \
                    -Dsonar.exclusions=node_modules/**'
                }
            }
        }

        stage('2. Local Web Environment Setup') {
            steps {
                echo 'Checking local system for Node web deployment dependencies...'
                /* 
                   Ensures 'http-server' is installed globally on Windows.
                   This is our lightweight substitute for heavier hosting software.
                */
                bat 'npm install -g http-server'
            }
        }

        stage('3. Run Live Local App Server') {
            steps {
                echo 'Launching Mock Interview Website on local environment...'
                /*
                  Starts a background web server on port 3000.
                  We use 'start' to run it in a separate thread so Jenkins doesn't get stuck waiting.
                */
                bat 'start /B http-server . -p 3000'
                echo '======================================================='
                echo 'APPLICATION IS LIVE! Open http://localhost:3000 in your browser'
                echo '======================================================='
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed perfectly.'
        }
    }
}