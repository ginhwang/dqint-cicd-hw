pipeline {
    agent any
    stages {
        stage ('GIT Checkout'){
            steps {
                git branch: 'main', url: 'https://github.com/ginhwang/dqint-cicd-hw.git'
            }
        }
        stage('build') {
            steps {
                sh '''
                python3 -m venv .venv
                source .venv/bin/activate
                python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage ('Test'){
            steps {
                sh '''
                source .venv/bin/activate
                pytest tests.py --html=report.html --capture sys -rP
                '''
            }
        }
    }
}