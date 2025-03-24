pipeline {
  agent any
  stages {
    stage('Set up Master environment') {
      agent {
        node {
          label 'jenkins'
        }

      }
      steps {
        sh '''python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pytest allure-pytest'''
      }
    }

    stage('set up node environment') {
      agent {
        node {
          label 'slave1'
        }

      }
      steps {
        sh '''python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pytest allure-pytest'''
      }
    }

    stage('Run Smoke on Master') {
      parallel {
        stage('Run Smoke on Master') {
          agent {
            node {
              label 'jenkins'
            }

          }
          steps {
            sh '''pytest -m smoke --alluredir=allure-results
deactivate'''
          }
        }

        stage('Run Regression on slave') {
          agent {
            node {
              label 'slave1'
            }

          }
          steps {
            sh '''pytest -m smoke --alluredir=allure-results
deactivate'''
          }
        }

      }
    }

    stage('Generate Allure Report') {
      agent {
        node {
          label 'jenkins'
        }

      }
      steps {
        sh 'allure generate allure-results --clean -o allure-report'
      }
    }

    stage('post Build actions') {
      agent {
        node {
          label 'jenkins'
        }

      }
      steps {
        sh 'archiveArtifacts artifacts: \'allure-report/**\', allowEmptyArchive: true'
      }
    }

  }
}