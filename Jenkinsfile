pipeline {
    agent none
    stages {
        stage('Checkout Repository') {
            agent { label 'master' }
            steps {
                echo 'Checking out the repository...'
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            agent { label 'master' }
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
            agent { label 'master' }
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
        stage('Generate Report') {
            agent { label 'master' }
            steps {
                echo 'Generating ZIP report...'
                sh '''
                zip regression_report.zip regression_report.html
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
            agent { label 'master' }
            steps {
                withSonarQubeEnv('mySonar') {
                    sh '''
                    sonar-scanner
                    '''
                }
            }
        }
        stage('Quality Gate') {
            agent { label 'master' }
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
    // post {
        // success {
        //     echo 'Pipeline completed successfully!'
        //     emailext(
        //         subject: "Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        //         body: """
        //         <p>The build was successful!</p>
        //         <p>Pipeline: ${env.JOB_NAME}</p>
        //         <p>Build Number: ${env.BUILD_NUMBER}</p>
        //         <p>Reports:</p>
        //         <ul>
        //             <li><a href="${env.BUILD_URL}artifact/regression_report.html">Regression Report</a></li>
        //             <li><a href="${env.BUILD_URL}artifact/regression_report.zip">Combined Report (ZIP)</a></li>
        //         </ul>
        //         """,
        //         to: 'sahoosbautomation@gmail.com',
        //         mimeType: 'text/html'
        //     )
        // }
        // failure {
        //     echo 'Pipeline failed!'
        //     emailext(
        //         subject: "Build Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        //         body: """
        //         <p>The build failed!</p>
        //         <p>Pipeline: ${env.JOB_NAME}</p>
        //         <p>Build Number: ${env.BUILD_NUMBER}</p>
        //         <p>Check the Jenkins logs for more details.</p>
        //         """,
        //         to: 'sahoosbautomation@gmail.com',
        //         mimeType: 'text/html'
        //     )
        // }
    // }
}
