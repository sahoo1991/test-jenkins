pipeline {
    agent any
    environment {
        SONAR_AUTH_TOKEN = credentials('sonarCred') // Store SonarQube token in Jenkins credentials
    }
    stages {
        stage('Checkout Repository') {
            steps {
                echo 'Checking out the repository...'
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install pytest pytest-html
                '''
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running Tests'
                script {
                    def testResult = sh(returnStatus: true, script: '''
                        source venv/bin/activate
                        pytest -m regression --html=regression_report.html --self-contained-html
                    ''')
                    if (testResult != 0) {
                        echo "Some tests failed. Marking the build as unstable."
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    echo 'Archiving regression test report...'
                    archiveArtifacts artifacts: 'regression_report.html', allowEmptyArchive: true
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Use the correct path to SonarScanner
                    def scannerHome = '/opt/homebrew/bin'
        
                    // Run SonarQube analysis
                    withSonarQubeEnv('mySonar') {
                        sh '''
                        export PATH=$PATH:${scannerHome}
                        sonar-scanner
                        '''
                    }
                }
                // script {
                    // Use the correct path to SonarScanner
                    // def scannerHome = '/opt/homebrew/bin'

                    // // Run SonarQube analysis securely
                    // withSonarQubeEnv('mySonar') {
                    //     sh '''
                    //     export PATH=$PATH:${scannerHome}
                    //     export SONAR_TOKEN=$SONAR_AUTH_TOKEN
                    //     sonar-scanner \
                    //       -Dsonar.projectKey=test-jenkins \
                    //       -Dsonar.sources=. \
                    //       -Dsonar.host.url=$SONAR_HOST_URL
                    //     '''
                    // }
                // }
            }
        }
        stage('Quality Gate') {
            steps {
                echo 'Checking SonarQube Quality Gate status...'
                script {
                    def qualityGate = waitForQualityGate()
                    if (qualityGate.status != 'OK') {
                        error "Pipeline failed due to SonarQube Quality Gate failure: ${qualityGate.status}"
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
