pipeline {
  agent any
  stages {
    stage('Set up Master environment') {
      steps {
        sh '''python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pytest allure-pytest'''
      }
    }

  }
}