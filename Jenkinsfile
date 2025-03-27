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
}
