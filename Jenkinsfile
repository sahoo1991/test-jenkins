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
                echo 'Setting up Python virtual environment and installing pytest...'
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install pytest pytest-html
                '''
            }
        }
        stage('Run Tests') {
                    agent { label 'master' }
                    steps {
                        echo 'Running regression tests on master node...'
                        sh '''
                        source venv/bin/activate
                        pytest -m regression --html=regression_report.html --self-contained-html
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'regression_report.html', allowEmptyArchive: true
                        }
                    }
        }
        stage('Generate Report') {
            agent { label 'master' }
            steps {
                echo 'Generating report...'
                sh '''
                zip regression_report.zip regression_report.html
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_reports.zip', allowEmptyArchive: true
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
                    <li><a href="${env.BUILD_URL}artifact/test_reports.zip">Combined Report (ZIP)</a></li>
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
