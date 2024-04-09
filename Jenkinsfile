pipeline {
    agent any
    stages {
        stage ('GIT Checkout'){
            steps {
                git changelog: false, poll: false, url: 'https://github.com/ginhwang/dqint-cicd-hw.git'
            }
        }
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage ('Test'){
            steps {
                sh 'pytest tests.py --html=report.html --capture sys -rP'
            }
        }
    }
}