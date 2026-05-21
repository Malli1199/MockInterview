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
                echo 'Clearing any stuck ports running on 3000...'
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    bat 'taskkill /F /IM http-server'
                }
                
                echo 'Spawning isolated web thread directly to your local system...'
                bat 'npm install -g http-server'
                
                /* This command bypasses the Windows Service block by launching the server 
                   silently in the background and immediately passing control back to Jenkins */
                bat 'start /B http-server . -p 3000'
                bat 'timeout /t 5 /nobreak'
            }
        }

        stage('3. Functional Testing Via Selenium') {
            steps {
                echo 'Executing Selenium validation assertions against port 3000...'
                bat 'python login_test.py'
            }
        }
    }
    post {
        success {
            echo '======================================================'
            echo 'BUILD SUCCESSFUL: New page running at http://localhost:3000'
            echo '======================================================'
        }
    }
}