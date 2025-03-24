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
                pip install pytest
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
                        pip install pytest
                        pytest -m smoke
                        '''
                    }
                }
                stage('Regression Tests on Master') {
                    agent { label 'master' }
                    steps {
                        echo 'Running regression tests on master node...'
                        sh '''
                        source venv/bin/activate
                        pytest -m regression
                        '''
                    }
                }
            }
        }
    }
}
