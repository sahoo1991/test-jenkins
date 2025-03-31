pipeline {
    agent none
    stages {
        stage('Checkout Repository') {
            agent {
                docker {
                    image 'jenkins-agent' // Replace with the name of your custom Jenkins agent image
                }
            }
            steps {
                echo 'Checking out the repository...'
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            agent {
                docker {
                    image 'jenkins-agent' // Replace with the name of your custom Jenkins agent image
                }
            }
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                if [ -d "venv" ]; then
                    rm -rf venv
                fi
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install pytest pytest-html
                '''
            }
        }
        stage('Run Tests') {
            agent {
                docker {
                    image 'jenkins-agent' // Replace with the name of your custom Jenkins agent image
                }
            }
            steps {
                echo 'Running Tests...'
                script {
                    def testResult = sh(returnStatus: true, script: '''
                        . venv/bin/activate
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
        stage('Generate Report') {
            agent {
                docker {
                    image 'jenkins-agent' // Replace with the name of your custom Jenkins agent image
                }
            }
            steps {
                echo 'Generating ZIP report...'
                sh '''
                zip -r regression_report.zip regression_report.html
                '''
            }
            post {
                always {
                    echo 'Archiving ZIP report...'
                    archiveArtifacts artifacts: 'regression_report.zip', allowEmptyArchive: true
                }
            }
        }
        stage('SonarQube Analysis') {
            agent {
                docker {
                    image 'sonarsource/sonar-scanner-cli:latest'
                }
            }
            steps {
                withSonarQubeEnv('mySonar') { // Ensure 'mySonar' matches the name of your SonarQube server in Jenkins
                    echo 'Running SonarQube analysis...'
                    sh '''
                    if [ -z "$SONAR_HOST_URL" ] || [ -z "$SONAR_AUTH_TOKEN" ]; then
                        echo "Error: SONAR_HOST_URL or SONAR_AUTH_TOKEN is not set."
                        exit 1
                    fi
                    sonar-scanner \
                        -Dsonar.projectKey=my_project_key \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }
        stage('Quality Gate') {
            agent {
                docker {
                    image 'jenkins-agent' // Replace with the name of your custom Jenkins agent image
                }
            }
            steps {
                echo 'Checking SonarQube Quality Gate status...'
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qualityGate = waitForQualityGate()
                        if (qualityGate.status != 'OK') {
                            error "Pipeline failed due to SonarQube Quality Gate failure: ${qualityGate.status}"
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
            emailext(
                subject: "Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                <p>The build was successful!</p>
                <p>Pipeline: ${env.JOB_NAME}</p>
                <p>Build Number: ${env.BUILD_NUMBER}</p>
                <p>Reports:</p>
                <ul>
                    <li><a href="${env.BUILD_URL}artifact/regression_report.html">Regression Report</a></li>
                    <li><a href="${env.BUILD_URL}artifact/regression_report.zip">Combined Report (ZIP)</a></li>
                </ul>
                """,
                to: 'sahoosbautomation@gmail.com',
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext(
                subject: "Build Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                <p>The build failed!</p>
                <p>Pipeline: ${env.JOB_NAME}</p>
                <p>Build Number: ${env.BUILD_NUMBER}</p>
                <p>Check the Jenkins logs for more details.</p>
                """,
                to: 'sahoosbautomation@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}
