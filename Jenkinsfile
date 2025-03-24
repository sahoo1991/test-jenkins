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
        stage('Run Tests in Parallel') {
            parallel {
                stage('Smoke Tests on Slave') {
                    agent { label 'slave1' }
                    steps {
                        echo 'Running smoke tests on slave node...'
                        sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install pytest pytest-html
                        pytest -m smoke --html=smoke_report.html --self-contained-html
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'smoke_report.html', allowEmptyArchive: true
                        }
                    }
                }
                stage('Regression Tests on Master') {
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
            }
        }
        stage('Generate Combined Report') {
            agent { label 'master' }
            steps {
                echo 'Combining reports into a single ZIP file...'
                sh '''
                zip test_reports.zip smoke_report.html regression_report.html
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
