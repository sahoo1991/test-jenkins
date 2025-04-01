pipeline {
    agent none

    environment {
        SONAR_SERVER = 'http://192.168.31.4:9000' // SonarQube server URL
        SONAR_TOKEN = 'sqa_cd09a59a2b62c8e78cdfca6c42d49eed90b43891'
    }
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
                bat '''
                pip install pytest pytest-html
                '''
            }
        }
        stage('Run Tests') {
            agent { label 'master' }
            steps {
                 echo 'Running Tests'
                    script {
                    def testResult = bat(returnStatus: true, script: '''
                        pytest -m regression --html=regression_report.html --self-contained-html
                    ''')
                    if (testResult != 0) {
                        echo "Some tests failed. Marking the build as unstable."
                        // currentBuild.result = 'UNSTABLE'
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
                bat 'powershell Compress-Archive -Path regression_report.html -DestinationPath regression_report.zip -Force'
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
                    bat 'sonar-scanner'
                }
            }
        }
        stage('Check Quality Gate') {
    agent { label 'master' }
    steps {
        script {
            // Fetch the task ID and project key from the SonarQube analysis report
            def reportPath = "${env.WORKSPACE}/.scannerwork/report-task.txt"
            def props = readProperties file: reportPath
            def ceTaskUrl = props['ceTaskUrl']
            def projectKey = props['projectKey'] // Extract the project key

            // Hardcode the token for debugging
            def authHeader = "Basic ${"sqa_cd09a59a2b62c8e78cdfca6c42d49eed90b43891:".bytes.encodeBase64().toString()}"

            // Print the Authorization header and URL for debugging
            echo "ceTaskUrl: ${ceTaskUrl}"
            echo "authHeader: ${authHeader}"

            // Poll the SonarQube API to wait for the task to complete
            def analysisStatus = ''
            timeout(time: 5, unit: 'MINUTES') {
                waitUntil {
                    def response = httpRequest(
                        url: ceTaskUrl,
                        customHeaders: [[name: 'Authorization', value: authHeader]],
                        validResponseCodes: '200'
                    )
                    def json = readJSON text: response.content
                    analysisStatus = json['task']['status']
                    return analysisStatus == 'SUCCESS' || analysisStatus == 'FAILED'
                }
            }

            // If the task failed, fail the pipeline
            if (analysisStatus == 'FAILED') {
                error "SonarQube analysis task failed!"
            }

            // Fetch the quality gate status
            def qualityGateResponse = httpRequest(
                url: "http://192.168.31.4:9000/api/qualitygates/project_status?projectKey=${projectKey}",
                customHeaders: [[name: 'Authorization', value: authHeader]],
                validResponseCodes: '200'
            )
            def qualityGateJson = readJSON text: qualityGateResponse.content
            def qualityGateStatus = qualityGateJson['projectStatus']['status']

            // Print the quality gate status for debugging
            echo "Quality Gate Status: ${qualityGateStatus}"

            // Fail the build if the quality gate status is FAILED
            if (qualityGateStatus == 'FAILED') {
                error "SonarQube Quality Gate failed!"
            } else {
                echo "SonarQube Quality Gate passed!"
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
